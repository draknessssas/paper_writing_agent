#!/usr/bin/env python3
"""Read/update the active YAML profile without discarding custom fields."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys

# Reading stays possible without pyyaml so an install can be checked from a bare python3.
# Writing keeps arbitrary user fields intact, which needs a real YAML round-trip, so it
# requires pyyaml (already in requirements.txt and installed by the documented bootstrap).
try:
    import yaml as _yaml

    HAS_YAML = True
    YAMLError = _yaml.YAMLError

    def safe_load(text: str):
        return _yaml.safe_load(text)

    def safe_dump(data: dict) -> str:
        return _yaml.safe_dump(data, allow_unicode=True, sort_keys=False)

except ModuleNotFoundError:

    HAS_YAML = False

    class YAMLError(ValueError):
        """Raised when the fallback reader meets YAML it does not implement."""

    _UNSUPPORTED = ('|', '>', '{', '[', '&', '*', '!')

    def _scalar(raw: str):
        raw = raw.strip()
        if not raw:
            return None
        if len(raw) > 1 and raw[0] in ('"', "'") and raw[-1] == raw[0]:
            return raw[1:-1]
        if raw.startswith('#'):  # the whole value is a comment
            return None
        raw = raw.split(' #', 1)[0].rstrip()  # trailing comment on an unquoted scalar
        if raw[:1] in _UNSUPPORTED:
            raise YAMLError(f'unsupported YAML construct: {raw[:20]!r}; install pyyaml')
        return raw or None

    def safe_load(text: str):
        """Parse `key: value` mappings and `  - item` lists. Refuses anything else."""
        data: dict = {}
        key = None
        for lineno, line in enumerate(text.splitlines(), 1):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            stripped = line.strip()
            if stripped.startswith('- '):
                if key is None:
                    raise YAMLError(f'list item before any key (line {lineno})')
                if not isinstance(data.get(key), list):
                    data[key] = []
                data[key].append(_scalar(stripped[2:]))
                continue
            if line[:1].isspace():
                raise YAMLError(
                    f'line {lineno}: this profile uses nested YAML, which the fallback reader '
                    'does not parse. Install pyyaml (pip install -r requirements.txt).')
            if ':' not in line:
                raise YAMLError(f'not a `key: value` line (line {lineno}); install pyyaml')
            key, _, rest = line.partition(':')
            key = key.strip()
            data[key] = _scalar(rest)
        return data or None

    def safe_dump(data: dict) -> str:
        raise YAMLError(
            'writing profiles/active_profile.yml needs pyyaml so custom fields survive '
            'the rewrite. Install it with: pip install -r requirements.txt')

DEFAULTS = {
    "venue": "", "venue_conventions": "", "paper_type": "regular",
    "editorial_conventions": "knowledge/ieee_editorial_conventions.md",
    "prose_quality": "knowledge/prose_quality.md",
    "profile_index": "profiles/index.md",
    "language_style": "profiles/language_style.md", "author_style": "",
    "argument_architecture": "profiles/argument_architecture.md",
    "manuscript_state": "working/manuscript_state.md",
    "manuscript_brief": "working/manuscript_brief.md",
    "evidence_packet": "working/evidence_packet.md", "refs_root": "refs",
    "current_manuscript": "", "bib_file": "",
}
OVERRIDES = {"IEEE_MANUSCRIPT_PATH": "current_manuscript", "IEEE_BIB_PATH": "bib_file",
             "IEEE_VENUE": "venue", "IEEE_PAPER_TYPE": "paper_type"}

def load_profile(path: Path) -> dict:
    if not path.exists():
        return {}
    value = safe_load(path.read_text(encoding="utf-8-sig"))
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"Profile must be a YAML mapping: {path}")
    return value

def update_profile(root: Path, env: dict | None = None) -> dict:
    env = os.environ if env is None else env
    path = root / "profiles/active_profile.yml"
    original = load_profile(path)
    updated = dict(original)
    for key, value in DEFAULTS.items():
        updated.setdefault(key, value)
    for key, target in OVERRIDES.items():
        if key in env:
            updated[target] = env[key]  # explicit empty values clear a binding
    if updated.get("paper_type") not in {"regular", "letter"}:
        raise ValueError("paper_type must be regular or letter")
    venue = updated.get("venue") or ""
    if venue and (not isinstance(venue, str) or not venue.replace('-', '').replace('_', '').isalnum()):
        raise ValueError("venue must be a simple name")
    if venue and not (root / "knowledge/venues" / f"{venue}.md").is_file():
        raise ValueError(f"Unknown venue: {venue}")
    # Preserve custom venue file unless the user explicitly changes/clears the venue.
    if "IEEE_VENUE" in env or (venue and not updated.get("venue_conventions")):
        updated["venue_conventions"] = f"knowledge/venues/{venue}.md" if venue else ""
    changed = updated != original or not path.exists()
    backup = None
    if changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup = path.with_name(path.name + '.backup.' + stamp)
            shutil.copy2(path, backup)
        temp = path.with_name(path.name + f'.tmp.{os.getpid()}')
        try:
            temp.write_text(safe_dump(updated), encoding="utf-8")
            temp.replace(path)
        finally:
            if temp.exists():
                temp.unlink()
    return {"changed": changed, "profile": str(path), "backup": str(backup) if backup else None}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = update_profile(args.root.resolve())
    except (ValueError, OSError, YAMLError) as exc:
        print(f'Profile error: {exc}', file=sys.stderr)
        return 1
    print(f"Profile {'updated' if result['changed'] else 'preserved'}: {result['profile']}")
    if result['backup']:
        print(f"Previous profile: {result['backup']}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
