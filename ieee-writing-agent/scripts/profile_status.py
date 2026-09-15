#!/usr/bin/env python3
"""Report active profiles and a specified manuscript state without creating files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from profile_config import load_profile

ROOT=Path(__file__).resolve().parents[1]

def path_value(root: Path, value) -> Path | None:
    if not value:
        return None
    path=Path(str(value)).expanduser()
    return path if path.is_absolute() else root/path

def resolve_state(manuscript: Path | None, explicit: Path | None=None, root: Path=ROOT) -> Path | None:
    if explicit is not None:
        return explicit.expanduser().resolve()
    if manuscript:
        m=manuscript.expanduser().resolve()
        base=m if m.is_dir() else m.parent
        for parent in [base,base.parent,base.parent.parent]:
            p=parent/'manuscript_state.md'
            if p.is_file():return p
    fallback=root/'working/manuscript_state.md'
    return fallback if fallback.is_file() else None

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript',type=Path)
    parser.add_argument('--state',type=Path)
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    try:
        config=load_profile(ROOT/'profiles/active_profile.yml')
    except Exception as exc:
        print(f'Cannot read profile: {exc}',file=sys.stderr);return 2
    manuscript=args.manuscript or path_value(ROOT,config.get('current_manuscript'))
    state=resolve_state(manuscript,args.state)
    warnings=[]
    profiles={}
    for key in ['profile_index','language_style','argument_architecture','author_style']:
        p=path_value(ROOT,config.get(key))
        profiles[key]={'path':str(p) if p else None,'status':'disabled' if p is None else 'available' if p.is_file() else 'missing'}
        if p and not p.is_file():warnings.append(f'Configured {key} missing: {p}')
    counts={}
    if state and state.is_file():
        text=state.read_text(encoding='utf-8')
        for heading in ['Terminology registry','Paragraph log','Section theses']:
            match=re.search(rf'^##\s+{heading}.*?$([\s\S]*?)(?=^##\s|\Z)',text,re.M|re.I)
            rows=[line for line in match.group(1).splitlines() if line.lstrip().startswith('|')] if match else []
            counts[heading]=max(0,len(rows)-2)
    error=bool(args.state and not args.state.is_file()) or bool(args.manuscript and not args.manuscript.exists())
    if error:warnings.append('Explicit manuscript/state path is missing.')
    report={'version':(ROOT/'VERSION').read_text().strip(),'root':str(ROOT),'profiles':profiles,
            'legacy_profiles':'Preserved; enabled only by an explicit active path',
            'manuscript':str(manuscript) if manuscript else None,'state':str(state) if state else None,
            'state_counts':counts,'warnings':warnings,
            'note':'State discovery by this status tool reports paths only; verify project Bindings before adopting a parent state.'}
    if args.json:print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        print(f"Writing toolkit {report['version']}: {ROOT}")
        for key,entry in profiles.items():print(f"{key}: {entry['status']} {entry['path'] or ''}")
        print(f"Manuscript: {manuscript or '<unset>'}; state: {state or '<none>'}")
        print(f'State counts: {counts}')
        for w in warnings:print('WARN '+w)
    return 2 if error else 0
if __name__=='__main__':
    raise SystemExit(main())
