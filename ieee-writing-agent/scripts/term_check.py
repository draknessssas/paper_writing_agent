#!/usr/bin/env python3
"""Terminology consistency checker and unifier (stdlib only).

Reads the "Terminology registry" table from the manuscript's manuscript_state.md (next to
the first input file, else up to two directories up, else working/manuscript_state.md; or any
markdown file given with --registry) and scans manuscript files for:
  1. registered variants that should be the canonical term;
  2. (--discover) unregistered inconsistencies: hyphen/space variants, casing
     variants of technical tokens, acronyms defined twice, used before
     definition, or never defined, and symbol subscript variants in math.

Fix mode replaces registered variants with their canonical form:
  python scripts/term_check.py main.tex --fix            # dry run, shows replacements
  python scripts/term_check.py main.tex --fix --write    # apply, keeps <file>.bak

Usage:
  python scripts/term_check.py <files...> [--registry <state file>]
                               [--discover] [--fix [--write]] [--json]
                               [--ignore IEEE,USA,...]

Registry table format (any column order; header names are matched loosely):
| Canonical | Variants | Symbol | Acronym | First use | Notes |
Variants are separated by ";".  Case-insensitive; matches inside \\cite, \\ref,
\\label, \\includegraphics, \\begin/\\end and file names are skipped.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PROTECT_RE = re.compile(
    r"\\(cite[a-zA-Z]*|ref|eqref|label|autoref|cref|Cref|includegraphics|input|include|url|href|"
    r"bibliography|bibliographystyle|begin|end|section|subsection|subsubsection|chapter|paragraph|title)"
    r"\*?(\[[^\]]*\])?\{[^}]*\}"
)
COMMENT_RE = re.compile(r"(?<!\\)%.*")
MATH_RE = re.compile(r"\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$[^$\n]*\$", re.S)
DEFAULT_IGNORE = {"IEEE", "USA", "UK", "EU", "URL", "DOI", "PDF", "ORCID", "MATLAB", "LATEX",
                  "ISBN", "ISSN", "AND", "OR", "NOT", "THE", "II", "III", "IV", "VI", "VII",
                  "VIII", "IX", "XI", "XII", "TABLE", "FIG"}
SEPARATORS = ["-", "–", " ", "/", ""]


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
def parse_registry(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#") and "terminology registry" in line.lower():
            start = i + 1
            break
    if start is None:
        return []
    header = None
    rows: list[dict] = []
    for line in lines[start:]:
        s = line.strip()
        if not s.startswith("|"):
            if header is not None and not s:
                break
            if header is not None:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue  # separator row
        row = {}
        for name, value in zip(header, cells):
            if "canonical" in name:
                row["canonical"] = value
            elif "variant" in name:
                row["variants"] = [v.strip() for v in re.split(r";", value) if v.strip()]
            elif "symbol" in name:
                row["symbol"] = value
            elif "acronym" in name:
                row["acronym"] = value
            elif "first" in name:
                row["first_use"] = value
            elif "note" in name:
                row["notes"] = value
        if row.get("canonical"):
            row.setdefault("variants", [])
            rows.append(row)
    return rows


def auto_variants(canonical: str) -> list[str]:
    """Generate hyphen/space/en-dash/slash/joined variants of a multi-token term."""
    tokens = re.split(r"[-–/ ]", canonical)
    if len(tokens) < 2:
        return []
    variants = set()
    for sep in SEPARATORS:
        candidate = sep.join(tokens)
        if candidate and candidate.lower() != canonical.lower():
            variants.add(candidate)
    return sorted(variants)


def compile_variant(variant: str) -> re.Pattern:
    escaped = re.escape(variant).replace(r"\ ", r"\s+")
    return re.compile(r"(?<![\w-])" + escaped + r"(?![\w-])", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def protected_spans(line: str) -> list[tuple[int, int]]:
    spans = [(m.start(), m.end()) for m in PROTECT_RE.finditer(line)]
    m = COMMENT_RE.search(line)
    if m:
        spans.append((m.start(), len(line)))
    return spans


def overlaps(spans: list[tuple[int, int]], start: int, end: int) -> bool:
    return any(s < end and start < e for s, e in spans)


def clean_for_discovery(line: str) -> str:
    line = COMMENT_RE.sub("", line)
    line = PROTECT_RE.sub(" ", line)
    line = MATH_RE.sub(" ", line)
    line = re.sub(r"\\[A-Za-z]+\*?", " ", line)
    return line.replace("{", " ").replace("}", " ")


# ---------------------------------------------------------------------------
# Registry check and fix
# ---------------------------------------------------------------------------
def check_registry(files: list[Path], registry: list[dict]) -> list[dict]:
    findings = []
    compiled = compile_registry(registry)
    for path in files:
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue  # markdown heading: title case is expected
            spans = protected_spans(line)
            for canonical, variant, pat, kind in compiled:
                for m in pat.finditer(line):
                    if overlaps(spans, m.start(), m.end()):
                        continue
                    if m.group(0) == canonical:
                        continue  # exact canonical, fine
                    if variant == canonical and m.group(0).lower() == canonical.lower() and m.start() == 0:
                        continue  # sentence-initial capitalization of the canonical term
                    if variant == canonical and m.group(0).lower() == canonical.lower():
                        before = line[:m.start()].rstrip()
                        if not before or before.endswith((".", "!", "?", ":")):
                            continue  # sentence-initial capitalization
                    findings.append({"file": str(path), "line": lineno, "found": m.group(0),
                                     "canonical": canonical, "kind": kind,
                                     "snippet": line[max(0, m.start() - 40): m.end() + 40].strip()})
    return findings


def compile_registry(registry: list[dict]) -> list[tuple]:
    """Return (canonical, variant, pattern, kind). kind: explicit | auto | auto-hyphen | case.

    explicit: listed in the registry (hard: reported and fixed);
    auto: generated separator variant without a hyphen (hard);
    auto-hyphen: generated hyphenated form (soft: reported only, because a hyphenated
        compound modifier before a noun, e.g. "core-loss model", is correct IEEE style);
    case: the canonical term with different capitalization (hard, outside headings).
    """
    compiled = []
    for row in registry:
        canonical = row["canonical"]
        seen = set()
        for v in row.get("variants", []):
            if v.lower() in seen or v.lower() == canonical.lower():
                continue
            seen.add(v.lower())
            compiled.append((canonical, v, compile_variant(v), "explicit"))
        for v in auto_variants(canonical):
            if v.lower() in seen:
                continue
            seen.add(v.lower())
            kind = "auto-hyphen" if "-" in v and "-" not in canonical else "auto"
            compiled.append((canonical, v, compile_variant(v), kind))
        compiled.append((canonical, canonical, re.compile(
            r"(?<![\w-])" + re.escape(canonical).replace(r"\ ", r"\s+") + r"(?![\w-])", re.IGNORECASE), "case"))
    return compiled


def apply_fix(files: list[Path], registry: list[dict], write: bool) -> list[dict]:
    changes = []
    compiled = [(c, pat, kind) for c, v, pat, kind in compile_registry(registry) if kind != "auto-hyphen"]
    for path in files:
        original = path.read_text(encoding="utf-8", errors="ignore")
        new_lines = []
        for lineno, line in enumerate(original.splitlines(keepends=True), 1):
            if line.lstrip().startswith("#"):
                new_lines.append(line)
                continue
            spans = protected_spans(line)
            out = line
            edits = []
            for canonical, pat, kind in compiled:
                for m in list(pat.finditer(line)):
                    if overlaps(spans, m.start(), m.end()):
                        continue
                    if m.group(0) == canonical:
                        continue
                    if kind == "case":
                        before = line[:m.start()].rstrip()
                        if not before or before.endswith((".", "!", "?", ":")):
                            continue  # sentence-initial capitalization is correct
                    replacement = canonical
                    if m.group(0)[:1].isupper() and canonical[:1].islower():
                        before = line[:m.start()].rstrip()
                        if not before or before.endswith((".", "!", "?")):
                            replacement = canonical[:1].upper() + canonical[1:]
                    edits.append((m.start(), m.end(), replacement, m.group(0)))
            # All coordinates refer to the original line. Prefer the longest match at
            # a shared start, then apply non-overlapping edits from right to left.
            selected = []
            for edit in sorted(edits, key=lambda e: (e[0], -(e[1] - e[0]))):
                if not selected or edit[0] >= selected[-1][1]:
                    selected.append(edit)
            for start, end, replacement, found in reversed(selected):
                out = out[:start] + replacement + out[end:]
            for start, end, replacement, found in selected:
                changes.append({"file": str(path), "line": lineno, "from": found, "to": replacement})
            new_lines.append(out)
        if write and "".join(new_lines) != original:
            backup = path.with_suffix(path.suffix + ".bak")
            backup.write_text(original, encoding="utf-8")
            path.write_text("".join(new_lines), encoding="utf-8")
    return changes


# ---------------------------------------------------------------------------
# Discovery of unregistered inconsistencies
# ---------------------------------------------------------------------------
def discover(files: list[Path], ignore: set[str]) -> dict:
    ngram_forms: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    token_forms: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    acronym_defs: dict[str, list[dict]] = defaultdict(list)
    acronym_uses: dict[str, list[dict]] = defaultdict(list)
    symbol_subs: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    def_re = re.compile(r"((?:[A-Za-z][\w-]*\s+){1,7}[A-Za-z][\w-]*)\s*\(([A-Za-z][A-Za-z0-9]{1,7})\)")
    acro_re = re.compile(r"\b[A-Z][A-Z0-9]{1,7}\b")
    ngram_re = re.compile(r"[A-Za-z][A-Za-z]+(?:[- ][A-Za-z][A-Za-z]+){1,2}")

    order = 0
    for path in files:
        raw_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for lineno, raw in enumerate(raw_lines, 1):
            order += 1
            # symbols in math segments (before cleaning)
            for seg in MATH_RE.findall(COMMENT_RE.sub("", raw)):
                for m in re.finditer(r"(?<![A-Za-z\\])([A-Za-z])_(\{[^{}]*\}|[A-Za-z0-9])", seg):
                    base, sub = m.group(1), m.group(2)
                    norm = re.sub(r"\\(mathrm|text|mathit|rm)", "", sub).replace("{", "").replace("}", "")
                    symbol_subs[base][f"{norm} (raw: {sub})"] += 1
            line = clean_for_discovery(raw)
            for m in def_re.finditer(line):
                acro = m.group(2)
                if acro.upper() in ignore:
                    continue
                acronym_defs[acro].append({"file": str(path), "line": lineno, "order": order,
                                           "expansion": m.group(1).strip()})
            for m in acro_re.finditer(line):
                acro = m.group(0)
                if acro in ignore or acro.isdigit():
                    continue
                acronym_uses[acro].append({"file": str(path), "line": lineno, "order": order})
            for m in ngram_re.finditer(line):
                surface = m.group(0)
                key = re.sub(r"[- ]+", " ", surface).lower()
                ngram_forms[key][re.sub(r"\s+", " ", surface.lower())] += 1
            for tok in re.findall(r"[A-Za-z][\w-]*", line):
                if any(ch.isdigit() for ch in tok) or any(ch.isupper() for ch in tok[1:]):
                    token_forms[tok.lower()][tok] += 1
                elif tok.lower() in token_forms:
                    token_forms[tok.lower()][tok] += 1

    hyphen_variants = []
    for key, forms in ngram_forms.items():
        distinct = {f for f in forms}
        if len(distinct) > 1 and any("-" in f for f in distinct):
            hyphen_variants.append({"term": key, "forms": dict(forms)})
    casing_variants = []
    for key, forms in token_forms.items():
        distinct = list(forms)
        if len(distinct) < 2:
            continue
        # ignore plain sentence-initial capitalization of an all-lowercase word
        lowered = {f for f in distinct if f.islower()}
        capitalized = {f for f in distinct if f[:1].isupper() and f[1:].islower()}
        others = set(distinct) - lowered - capitalized
        if others and len(distinct) > 1:
            casing_variants.append({"token": key, "forms": dict(forms)})
    acronym_issues = []
    for acro, defs in acronym_defs.items():
        if len(defs) > 1:
            acronym_issues.append({"acronym": acro, "issue": "defined more than once",
                                   "locations": [f"{d['file']}:{d['line']} ({d['expansion']})" for d in defs]})
    for acro, uses in acronym_uses.items():
        if len(acro) < 2:
            continue
        defs = acronym_defs.get(acro)
        if not defs:
            if len(uses) >= 1:
                acronym_issues.append({"acronym": acro, "issue": "used but never defined (add to registry or define at first use)",
                                       "locations": [f"{u['file']}:{u['line']}" for u in uses[:5]],
                                       "count": len(uses)})
            continue
        first_def = min(d["order"] for d in defs)
        early = [u for u in uses if u["order"] < first_def]
        if early:
            acronym_issues.append({"acronym": acro, "issue": "used before its definition",
                                   "locations": [f"{u['file']}:{u['line']}" for u in early[:5]]})
    symbol_variants = [{"symbol": base, "subscripts": dict(subs)} for base, subs in symbol_subs.items()
                       if len(subs) > 1]
    return {"hyphen_or_space_variants": sorted(hyphen_variants, key=lambda x: x["term"]),
            "casing_variants": sorted(casing_variants, key=lambda x: x["token"]),
            "acronym_issues": sorted(acronym_issues, key=lambda x: x["acronym"]),
            "symbol_subscript_variants": sorted(symbol_variants, key=lambda x: x["symbol"])}


def resolve_registry(explicit: str | None, files: list[Path]) -> Path:
    """State file rule: next to the manuscript, then up to two directories up, then the workspace fallback."""
    if explicit:
        return Path(explicit)
    first = files[0].resolve().parent
    for cand in (first / "manuscript_state.md", first.parent / "manuscript_state.md", first.parent.parent / "manuscript_state.md"):
        if cand.is_file():
            return cand
    return Path("working/manuscript_state.md")


# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Terminology consistency checker (stdlib only).")
    parser.add_argument("files", nargs="+", help="manuscript files (.tex/.md/.txt)")
    parser.add_argument("--registry", default=None,
                        help="markdown file containing a 'Terminology registry' table (default: manuscript_state.md "
                             "next to the first input file, then up to two directories up, then working/manuscript_state.md)")
    parser.add_argument("--discover", action="store_true", help="also report unregistered inconsistencies")
    parser.add_argument("--fix", action="store_true", help="replace registered variants with canonical forms (dry run)")
    parser.add_argument("--write", action="store_true", help="with --fix: apply changes (keeps .bak)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--ignore", default="", help="comma-separated acronyms to ignore in discovery")
    parser.add_argument("--fail-on-findings", action="store_true", help="exit 1 for remaining explicit registered variants")
    args = parser.parse_args()
    if args.write and not args.fix:
        parser.error("--write requires --fix")

    files = [Path(f) for f in args.files]
    missing = [str(f) for f in files if not f.is_file()]
    if missing:
        print(f"missing files: {', '.join(missing)}", file=sys.stderr)
        return 2
    if any(f.suffix.lower() in {".docx", ".pdf"} for f in files):
        parser.error("extract PDF/DOCX to text before checking terminology")
    registry_path = resolve_registry(args.registry, files)
    if args.registry and not registry_path.is_file():
        parser.error(f"explicit registry not found: {registry_path}")
    registry = parse_registry(registry_path)
    ignore = DEFAULT_IGNORE | {a.strip().upper() for a in args.ignore.split(",") if a.strip()}
    for row in registry:
        if row.get("acronym"):
            ignore.add(row["acronym"].split()[0].strip("()").upper())

    result: dict = {"registry_rows": len(registry), "registry_file": str(registry_path)}
    if not registry:
        result["warning"] = (f"no 'Terminology registry' table found in {registry_path}; "
                             "only discovery is possible")
    if args.fix:
        result["fix"] = apply_fix(files, registry, write=args.write)
        result["fix_applied"] = bool(args.write)
    else:
        result["registry_findings"] = check_registry(files, registry)
    if args.discover:
        result["discovery"] = discover(files, ignore)

    remaining = check_registry(files, registry) if args.fix else result["registry_findings"]
    blocking = [f for f in remaining if f["kind"] != "auto-hyphen"]
    result["remaining_registered_variants"] = len(blocking)
    exit_code = 1 if args.fail_on_findings and blocking else 0
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return exit_code

    print(f"Terminology check ({len(registry)} registry rows from {registry_path})")
    if result.get("warning"):
        print(f"  warning: {result['warning']}")
    if args.fix:
        changes = result["fix"]
        print(f"\nFix {'applied' if args.write else 'dry run'}: {len(changes)} replacement(s)")
        for c in changes[:200]:
            print(f"  {c['file']}:{c['line']}  '{c['from']}' -> '{c['to']}'")
    else:
        findings = result["registry_findings"]
        hard = [f for f in findings if f["kind"] != "auto-hyphen"]
        soft = [f for f in findings if f["kind"] == "auto-hyphen"]
        print(f"\nRegistered-variant findings: {len(hard)} (fixable) + {len(soft)} (hyphenated form; compound modifier may be intended, not auto-fixed)")
        for f in hard[:200]:
            print(f"  {f['file']}:{f['line']}  '{f['found']}' -> '{f['canonical']}'  [{f['kind']}]   ...{f['snippet']}...")
        for f in soft[:200]:
            print(f"  {f['file']}:{f['line']}  '{f['found']}' ~ '{f['canonical']}'  [check: adjective use?]   ...{f['snippet']}...")
    if args.discover:
        d = result["discovery"]
        print(f"\nDiscovery: hyphen/space variants: {len(d['hyphen_or_space_variants'])}")
        for item in d["hyphen_or_space_variants"][:100]:
            forms = ", ".join(f"'{k}' x{v}" for k, v in item["forms"].items())
            print(f"  {item['term']}: {forms}")
        print(f"Discovery: casing variants: {len(d['casing_variants'])}")
        for item in d["casing_variants"][:100]:
            forms = ", ".join(f"'{k}' x{v}" for k, v in item["forms"].items())
            print(f"  {forms}")
        print(f"Discovery: acronym issues: {len(d['acronym_issues'])}")
        for item in d["acronym_issues"][:100]:
            extra = f" (x{item['count']})" if item.get("count") else ""
            print(f"  {item['acronym']}: {item['issue']}{extra}; {', '.join(item['locations'])}")
        print(f"Discovery: symbol subscript variants: {len(d['symbol_subscript_variants'])}")
        for item in d["symbol_subscript_variants"][:100]:
            print(f"  {item['symbol']}: {item['subscripts']}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
