#!/usr/bin/env python3
"""Check source/adapters and optionally installed links; not a behavior evaluator."""
from __future__ import annotations
import argparse
import importlib.util
import re
from pathlib import Path
import sys
import tomllib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from profile_config import YAMLError, safe_load  # pyyaml if installed, stdlib fallback otherwise

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ['writing-skill', 'style-profiler', 'citation-verifier', 'manuscript-reviewer']
PAIRS = [('writing-agent', 'writer', 'writer', 'workspace-write'),
         ('corpus-analyst', 'corpus-analyst', 'corpus-analyst', 'read-only')]
REQUIRED = ['VERSION', 'AGENTS.md', 'CLAUDE.md', 'profiles/index.md', 'profiles/active_profile.yml',
            'knowledge/prose_quality.md', 'knowledge/prose_patterns.md',
            'knowledge/ieee_editorial_conventions.md',
            'scripts/bootstrap.sh', 'scripts/bootstrap.ps1', 'scripts/bootstrap_wsl.sh',
            'scripts/profile_config.py', 'scripts/profile_status.py', 'scripts/ingest_papers.py',
            'scripts/prose_gate.py', 'scripts/term_check.py', 'scripts/check_bib.py',
            'skills/writing-skill/references/validation-and-completion.md',
            'skills/style-profiler/references/extraction.md']

def frontmatter(text: str) -> tuple[dict, str]:
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError('missing YAML frontmatter')
    fields = safe_load(parts[1])
    if not isinstance(fields, dict):
        raise ValueError('frontmatter must be a mapping')
    return fields, parts[2].strip()

def inspect_source(root: Path, installed: bool = False, user_root: Path | None = None) -> dict:
    failures, warnings, passes = [], [], []
    def require(condition, label):
        (passes if condition else failures).append(label)
    for name in REQUIRED:
        require((root/name).is_file(), f'file: {name}')
    for name in SKILLS:
        p=root/'skills'/name/'SKILL.md'
        try:
            text=p.read_text();fm,_=frontmatter(text)
            require(fm.get('name')==name, f'skill name: {name}')
            d=fm.get('description','')
            require(isinstance(d,str) and bool(d.strip()), f'description: {name}')
            # Local budgets, not vendor limits. Warn rather than falsifying behavior tests.
            if isinstance(d,str) and len(d)>240:
                warnings.append(f'{name}: description {len(d)} chars; consider a shorter trigger')
            if len(text.encode())>10000:
                warnings.append(f'{name}: entrypoint >10 KB; inspect conditional detail')
        except (OSError,ValueError,YAMLError) as exc:
            failures.append(f'{name}: {exc}')
        for base in ['.agents/skills','.claude/skills']:
            link=root/base/name
            require(link.exists() and link.resolve()==(root/'skills'/name).resolve(), f'project link: {base}/{name}')
    for cname,xname,role,sandbox in PAIRS:
        try:
            fm,cbody=frontmatter((root/f'.claude/agents/{cname}.md').read_text())
            xbody=(root/f'.codex/agents/{xname}/AGENTS.md').read_text().strip()
            config=tomllib.loads((root/f'.codex/agents/{xname}/config.toml').read_text())
            require(fm.get('name')==cname and config.get('name')==xname, f'role names: {role}')
            require(cbody==xbody==config.get('developer_instructions','').strip(), f'adapter contract equality: {role}')
            contract=f'knowledge/roles/{role}.md'
            require(contract in cbody and (root/contract).is_file(), f'role contract: {role}')
            require(config.get('sandbox_mode')==sandbox, f'Codex sandbox: {role}')
            require(fm.get('model')=='inherit' and 'model' not in config, f'model inheritance: {role}')
            if role=='corpus-analyst':
                require(set(fm.get('tools',[]))<={'Read','Grep','Glob'}, 'Claude analyst read-only tools')
        except (OSError,ValueError,YAMLError) as exc:
            failures.append(f'role {role}: {exc}')
    for folder in ['skills','knowledge']:
        for p in (root/folder).rglob('*.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
                target=target.split('#',1)[0]
                if not target or '://' in target or target.startswith(('/', '<')):
                    continue
                if not (p.parent/target).exists():
                    failures.append(f'broken reference: {p.relative_to(root)} -> {target}')
    try:
        spec=importlib.util.spec_from_file_location('parity_prose',root/'scripts/prose_gate.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        doc=(root/'knowledge/prose_patterns.md').read_text().lower()
        absent=[phrase for rule in mod.RULES for phrase in rule.get('phrases',[]) if phrase.lower() not in doc]
        require(not absent,f'prose lexicon documented ({len(absent)} missing)')
    except (OSError,ImportError,SyntaxError) as exc:
        failures.append(f'prose lexicon: {exc}')
    if installed:
        user=Path.home() if user_root is None else user_root
        for name in SKILLS:
            for base in ['.agents/skills','.claude/skills']:
                p=user/base/name
                require(p.exists() and p.resolve()==(root/'skills'/name).resolve(),f'installed: {p}')
            legacy=user/'.codex/skills'/name
            if legacy.exists() or legacy.is_symlink():
                require(legacy.exists() and legacy.resolve()==(root/'skills'/name).resolve(),f'legacy alias: {legacy}')
        targets={f'.claude/agents/{c}.md':f'.claude/agents/{c}.md' for c,_,_,_ in PAIRS}
        targets.update({f'.codex/agents/{x}':f'.codex/agents/{x}' for _,x,_,_ in PAIRS})
        targets['.claude/output-styles/manuscript-writer.md']='.claude/output-styles/manuscript-writer.md'
        for dest,source in targets.items():
            p=user/dest;q=root/source
            equal=p.exists() and (p.resolve()==q.resolve() or (p.is_file() and q.is_file() and p.read_bytes()==q.read_bytes()))
            require(equal,f'installed adapter: {p}')
    return {'root':str(root),'scope':'source+installed' if installed else 'source','passed':len(passes),'failures':failures,'warnings':warnings}

def main() -> int:
    import json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installed',action='store_true',help='also require current user installation links')
    parser.add_argument('--quiet',action='store_true')
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    result=inspect_source(ROOT,args.installed)
    if args.json:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for msg in result['failures']:print('FAIL '+msg)
        if not args.quiet:
            for msg in result['warnings']:print('WARN '+msg)
        print(f"Parity {'FAILED' if result['failures'] else 'passed'} ({result['passed']} static checks; {result['scope']}).")
        if not args.quiet:print('This checks files/adapters, not model behavior or scientific correctness.')
    return int(bool(result['failures']))
if __name__=='__main__':
    sys.dont_write_bytecode=True
    raise SystemExit(main())
