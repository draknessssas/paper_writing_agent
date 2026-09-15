"""Isolated behavioral regressions for changed local helpers; no network access."""
from pathlib import Path
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import profile_config
from profile_config import safe_load as _safe_load

_NEEDS_YAML = unittest.skipUnless(profile_config.HAS_YAML,
    'profile writing needs pyyaml; run in the venv (pip install -r requirements.txt)')
import profile_status
import check_parity
import prose_gate
import term_check
import check_bib

class ToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='writing-tools-',dir='/tmp')
        self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def file(self,name,text):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);return p
    def cli(self,script,*args):
        return subprocess.run([sys.executable,'-B',str(ROOT/'scripts'/script),*map(str,args)],capture_output=True,text=True)
    def test_prose_novel_is_contextual(self):
        hits,_=prose_gate.scan('This novel model estimates the field.')
        self.assertTrue(any(h['tier']=='AUDIT' for h in hits))
        self.assertFalse(any(h['tier']=='BAN' for h in hits))
    def test_prose_long_sentence_is_reported_without_failure(self):
        p=self.file('long.txt','The model uses '+' '.join(['input']*40)+'.')
        result=self.cli('prose_gate.py',p,'--json')
        self.assertEqual(result.returncode,0)
        self.assertTrue(json.loads(result.stdout)['stats']['over_40'])
    def test_prose_existing_ban_still_fails(self):
        p=self.file('draft.txt','It is worth noting that the model estimates the field.')
        self.assertEqual(self.cli('prose_gate.py',p).returncode,1)
    @_NEEDS_YAML
    def test_profile_preserves_custom_yaml_and_is_idempotent(self):
        p=self.file('profiles/active_profile.yml','paper_type: regular\ncurrent_manuscript: "paper #1/main.tex"\ncustom:\n  values: [a, b]\n')
        before=p.read_bytes()
        result=profile_config.update_profile(self.root,{})
        data=profile_config.load_profile(p)
        self.assertEqual(data['current_manuscript'],'paper #1/main.tex')
        self.assertEqual(data['custom'],{'values':['a','b']})
        self.assertEqual(Path(result['backup']).read_bytes(),before)
        after=p.read_bytes()
        self.assertFalse(profile_config.update_profile(self.root,{})['changed'])
        self.assertEqual(p.read_bytes(),after)
    @_NEEDS_YAML
    def test_profile_empty_override_clears_without_erasing_other_keys(self):
        self.file('profiles/active_profile.yml','paper_type: regular\nvenue: tpel\nvenue_conventions: custom.md\ncurrent_manuscript: old.tex\ncustom: yes\n')
        profile_config.update_profile(self.root,{'IEEE_MANUSCRIPT_PATH':'','IEEE_VENUE':''})
        d=profile_config.load_profile(self.root/'profiles/active_profile.yml')
        self.assertEqual(d['current_manuscript'],'');self.assertEqual(d['venue_conventions'],'');self.assertIn('custom',d)
    def test_profile_invalid_venue_does_not_write(self):
        p=self.file('profiles/active_profile.yml','paper_type: regular\ncustom: keep\n');before=p.read_bytes()
        with self.assertRaises(ValueError):profile_config.update_profile(self.root,{'IEEE_VENUE':'unknown'})
        self.assertEqual(p.read_bytes(),before)
    def registry(self):
        return self.file('manuscript_state.md','## Terminology registry\n\n| Canonical | Variants |\n|---|---|\n| digital twin | virtual replica |\n')
    def test_registry_two_parent_discovery(self):
        state=self.registry();text=self.file('sections/sub/paragraph.tex','text')
        self.assertEqual(term_check.resolve_registry(None,[text]),state)
        self.assertEqual(profile_status.resolve_state(text,root=self.root),state)
    def test_terms_dry_run_write_backup_and_remaining_findings(self):
        state=self.registry();text=self.file('draft.tex',r'The virtual replica works. \cite{virtual replica}'+'\n')
        before=text.read_bytes()
        res=self.cli('term_check.py',text,'--registry',state,'--fix','--json','--fail-on-findings')
        self.assertEqual(res.returncode,1);self.assertEqual(text.read_bytes(),before)
        res=self.cli('term_check.py',text,'--registry',state,'--fix','--write','--json','--fail-on-findings')
        self.assertEqual(res.returncode,0,res.stdout+res.stderr)
        self.assertEqual(text.read_text(),r'The digital twin works. \cite{virtual replica}'+'\n')
        self.assertEqual(text.with_suffix('.tex.bak').read_bytes(),before)
    def test_terms_write_requires_fix(self):
        text=self.file('draft.tex','text')
        self.assertEqual(self.cli('term_check.py',text,'--write').returncode,2)
    def test_terms_multiple_different_length_replacements(self):
        text=self.file('draft.tex','The Twin and electric drive operate.\n')
        rows=[{'canonical':'electrical drive system','variants':['electric drive']},
              {'canonical':'digital twin','variants':['Twin']}]
        term_check.apply_fix([text],rows,write=True)
        self.assertEqual(text.read_text(),'The digital twin and electrical drive system operate.\n')
    def bib_run(self,key='real',extra_args=(),online=None):
        bib=self.file('refs.bib',f'@misc{{{key}, title={{Source title}}, year={{2020}}}}')
        tex=self.file('main.tex',f'Finding \\cite{{{key}}}.')
        out=io.StringIO()
        with patch.object(sys,'argv',['check_bib','--bib',str(bib),'--tex',str(tex),'--json',*extra_args]),contextlib.redirect_stdout(out),patch.object(check_bib,'check_online',return_value=online or []):
            code=check_bib.main()
        return code,json.loads(out.getvalue())
    def test_placeholder_existing_in_bib_still_fails(self):
        code,data=self.bib_run('PLACEHOLDER_x')
        self.assertEqual(code,1);self.assertTrue(data['placeholders'])
    def test_online_mismatch_fails(self):
        code,data=self.bib_run(extra_args=['--online'],online=[{'key':'real','status':'mismatch','detail':'different title'}])
        self.assertEqual(code,1)
    def test_online_unresolved_is_reported_without_fake_paper_claim(self):
        row={'key':'real','status':'unresolved','detail':'network unavailable'}
        code,data=self.bib_run(extra_args=['--online'],online=[row])
        self.assertEqual(code,0);self.assertEqual(data['online'][0]['status'],'unresolved')
        code,_=self.bib_run(extra_args=['--require-online'],online=[row]);self.assertEqual(code,1)
    def test_require_online_without_doi_is_incomplete(self):
        code,data=self.bib_run(extra_args=['--require-online'])
        self.assertEqual(code,1);self.assertEqual(data['online'][0]['status'],'unresolved')
    def test_bib_missing_input_fails(self):
        bib=self.file('refs.bib','@misc{x,title={t}}')
        self.assertEqual(self.cli('check_bib.py','--bib',bib,'--tex',self.root/'absent.tex').returncode,2)
    @_NEEDS_YAML
    def test_bootstrap_local_preserves_profile_and_links(self):
        target=self.root/'toolkit'
        shutil.copytree(ROOT,target,symlinks=True,ignore=shutil.ignore_patterns('.venv','.git','processed','corpora','refs','working','__pycache__'))
        profile=target/'profiles/active_profile.yml';profile.write_text(profile.read_text()+'custom_nested:\n  enabled: true\n')
        env=dict(os.environ);env['IEEE_PYTHON']=sys.executable;env['PYTHONDONTWRITEBYTECODE']='1'
        for key in profile_config.OVERRIDES:env.pop(key,None)
        for _ in range(2):
            result=subprocess.run(['bash',str(target/'scripts/bootstrap.sh'),'local'],env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(profile_config.load_profile(profile)['custom_nested'],{'enabled':True})
        for name in check_parity.SKILLS:
            self.assertEqual((target/'.agents/skills'/name).resolve(),target/'skills'/name)
            self.assertEqual((target/'.claude/skills'/name).resolve(),target/'skills'/name)
        bad=subprocess.run(['bash',str(target/'scripts/bootstrap.sh'),'invalid'],env=env,capture_output=True)
        self.assertEqual(bad.returncode,2)
    def test_missing_installation_is_not_reported_as_installed(self):
        report=check_parity.inspect_source(ROOT,installed=True,user_root=self.root)
        self.assertTrue(any('installed:' in f for f in report['failures']))

if __name__=='__main__':unittest.main()
