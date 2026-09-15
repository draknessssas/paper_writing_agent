#!/usr/bin/env python3
"""Deterministic BibTeX / citation checks (stdlib only).

Checks:
  - cited keys missing from the .bib; .bib entries never cited; duplicate keys;
    duplicate titles
  - required fields per entry type; DOI format; year sanity; author format
  - journal names not abbreviated (IEEE style uses the official abbreviations)
  - journal articles without volume/pages (early access? re-verify before submission)
  - page ranges written with a single hyphen instead of "--"
  - optional --online: Crossref lookup by DOI, title/year comparison (no API key)

Usage:
  python scripts/check_bib.py --bib refs.bib --tex main.tex [more.tex ...]
  python scripts/check_bib.py --bib refs.bib                      # bib-only checks
  python scripts/check_bib.py --bib refs.bib --tex main.tex --online --mailto you@uni.edu
  add --json for machine-readable output.

It never generates or repairs metadata; it only reports. Metadata that cannot be
verified offline is marked [VERIFY ONLINE].
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

REQUIRED = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "conference": ["author", "title", "booktitle", "year"],
    "book": ["title", "publisher", "year"],
    "incollection": ["author", "title", "booktitle", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "misc": ["title"],
    "online": ["title"],
    "electronic": ["title"],
    "standard": ["title"],
}
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
CITE_RE = re.compile(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]*)\}")
UNABBREVIATED = ["transactions on", "journal of", "proceedings of the", "conference on", "international journal"]


# ---------------------------------------------------------------------------
# BibTeX parsing (tolerant, brace-matching)
# ---------------------------------------------------------------------------
def parse_bib(text: str) -> list[dict]:
    entries = []
    i = 0
    n = len(text)
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        m = re.match(r"@(\w+)\s*[\{\(]", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        body_start = at + m.end()
        depth = 1
        j = body_start
        while j < n and depth > 0:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[body_start:j - 1]
        line = text.count("\n", 0, at) + 1
        i = j
        if etype in ("comment", "preamble", "string"):
            continue
        key_match = re.match(r"\s*([^,\s]+)\s*,", body)
        key = key_match.group(1) if key_match else ""
        fields = {}
        rest = body[key_match.end():] if key_match else body
        pos = 0
        while True:
            fm = re.match(r"\s*,?\s*(\w[\w-]*)\s*=\s*", rest[pos:])
            if not fm:
                break
            name = fm.group(1).lower()
            pos += fm.end()
            if pos >= len(rest):
                break
            ch = rest[pos]
            if ch == "{":
                depth = 1
                k = pos + 1
                while k < len(rest) and depth > 0:
                    if rest[k] == "{":
                        depth += 1
                    elif rest[k] == "}":
                        depth -= 1
                    k += 1
                value = rest[pos + 1:k - 1]
                pos = k
            elif ch == '"':
                k = rest.find('"', pos + 1)
                while k > 0 and rest[k - 1] == "\\":
                    k = rest.find('"', k + 1)
                value = rest[pos + 1:k] if k > 0 else rest[pos + 1:]
                pos = k + 1 if k > 0 else len(rest)
            else:
                vm = re.match(r"[^,\n]*", rest[pos:])
                value = vm.group(0).strip()
                pos += vm.end()
            fields[name] = re.sub(r"\s+", " ", value).strip()
        entries.append({"type": etype, "key": key, "fields": fields, "line": line})
    return entries


def norm_title(t: str) -> str:
    t = re.sub(r"[{}\\]", "", t).lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


# ---------------------------------------------------------------------------
# TeX citations
# ---------------------------------------------------------------------------
def collect_cites(tex_paths: list[Path], follow_inputs: bool = True) -> dict[str, list[str]]:
    cites: dict[str, list[str]] = {}
    seen = set()
    stack = list(tex_paths)
    while stack:
        p = stack.pop()
        if p in seen or not p.is_file():
            continue
        seen.add(p)
        text = re.sub(r"(?<!\\)%.*", "", p.read_text(encoding="utf-8", errors="ignore"))
        for m in CITE_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            for key in m.group(1).split(","):
                key = key.strip()
                if key:
                    cites.setdefault(key, []).append(f"{p}:{line}")
        if follow_inputs:
            for m in INPUT_RE.finditer(text):
                child = (p.parent / m.group(1))
                if child.suffix == "":
                    child = child.with_suffix(".tex")
                stack.append(child)
    return cites


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def check_entries(entries: list[dict]) -> list[dict]:
    issues = []
    this_year = date.today().year
    keys_seen: dict[str, int] = {}
    titles_seen: dict[str, str] = {}
    for e in entries:
        key, f, t = e["key"], e["fields"], e["type"]
        loc = f"bib:{e['line']}"
        if key in keys_seen:
            issues.append({"key": key, "severity": "error", "issue": f"duplicate key (also at bib:{keys_seen[key]})", "where": loc})
        keys_seen.setdefault(key, e["line"])
        title = f.get("title", "")
        if title:
            nt = norm_title(title)
            if nt in titles_seen and titles_seen[nt] != key:
                issues.append({"key": key, "severity": "warn", "issue": f"duplicate title of entry '{titles_seen[nt]}' (conference vs journal version? cite the archival one)", "where": loc})
            titles_seen.setdefault(nt, key)
            if title.isupper():
                issues.append({"key": key, "severity": "warn", "issue": "title in all caps", "where": loc})
        for req in REQUIRED.get(t, ["title"]):
            if req == "author" and ("author" in f or "editor" in f):
                continue
            if req not in f or not f[req]:
                issues.append({"key": key, "severity": "error", "issue": f"missing required field '{req}' for @{t}", "where": loc})
        year = f.get("year", "")
        if year and not re.fullmatch(r"\d{4}", re.sub(r"[{}]", "", year)):
            issues.append({"key": key, "severity": "warn", "issue": f"year not four digits: {year}", "where": loc})
        elif year and int(re.sub(r"[{}]", "", year)) > this_year + 1:
            issues.append({"key": key, "severity": "warn", "issue": f"year in the future: {year}", "where": loc})
        doi = f.get("doi", "")
        if doi:
            clean = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip())
            if not DOI_RE.match(clean):
                issues.append({"key": key, "severity": "error", "issue": f"malformed DOI: {doi}", "where": loc})
        author = f.get("author", "")
        if author and re.search(r"\bet\.? al\.?", author, re.IGNORECASE):
            issues.append({"key": key, "severity": "error", "issue": "author field contains 'et al.'; list all authors (BibTeX truncates)", "where": loc})
        if author and "," not in author and " and " not in author and len(author.split()) > 3:
            issues.append({"key": key, "severity": "warn", "issue": "author field has several names without 'and'", "where": loc})
        journal = f.get("journal", "")
        if journal:
            jl = journal.lower()
            if any(w in jl for w in UNABBREVIATED):
                issues.append({"key": key, "severity": "warn", "issue": f"journal name not abbreviated per IEEE list: '{journal}'", "where": loc})
            if re.search(r"trans\.\s+\w+\s+electronics\b", jl):
                issues.append({"key": key, "severity": "warn", "issue": f"use the official abbreviation (e.g., 'IEEE Trans. Power Electron.'), found '{journal}'", "where": loc})
        if t == "article":
            if "arxiv" in (journal + f.get("eprint", "") + f.get("archiveprefix", "")).lower():
                issues.append({"key": key, "severity": "info", "issue": "arXiv preprint; check whether a published version exists", "where": loc})
            elif not f.get("volume") or not (f.get("pages") or f.get("number") or f.get("articleno")):
                issues.append({"key": key, "severity": "warn", "issue": "article without volume/pages: early access? re-verify before submission [VERIFY ONLINE]", "where": loc})
        pages = f.get("pages", "")
        if pages and re.fullmatch(r"\d+\s*-\s*\d+", pages):
            issues.append({"key": key, "severity": "info", "issue": f"page range with a single hyphen; BibTeX convention is '--': {pages}", "where": loc})
        if not doi and t in ("article", "inproceedings") and not f.get("url"):
            issues.append({"key": key, "severity": "info", "issue": "no DOI or URL; metadata cannot be verified offline [VERIFY ONLINE]", "where": loc})
    return issues


def crossref_lookup(doi: str, mailto: str | None, timeout: float = 10.0) -> dict | None:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    headers = {"User-Agent": "check_bib.py (writing-agent)" + (f"; mailto:{mailto}" if mailto else "")}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("message")
    except urllib.error.HTTPError as exc:
        return {"_error": f"HTTP {exc.code}"}
    except Exception as exc:  # network errors
        return {"_error": str(exc)}


def check_online(entries: list[dict], mailto: str | None) -> list[dict]:
    results = []
    for e in entries:
        doi = e["fields"].get("doi", "")
        if not doi:
            continue
        clean = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip())
        msg = crossref_lookup(clean, mailto)
        time.sleep(0.2)
        if msg is None or "_error" in (msg or {}):
            results.append({"key": e["key"], "doi": clean, "status": "unresolved",
                            "detail": (msg or {}).get("_error", "no response") + " (verification unresolved)"})
            continue
        cr_title = " ".join(msg.get("title", []) or [])
        cr_year = None
        for k in ("published-print", "published-online", "issued", "created"):
            parts = (msg.get(k) or {}).get("date-parts") or []
            if parts and parts[0]:
                cr_year = parts[0][0]
                break
        ratio = difflib.SequenceMatcher(None, norm_title(e["fields"].get("title", "")), norm_title(cr_title)).ratio()
        year = re.sub(r"[{}]", "", e["fields"].get("year", ""))
        status = "match" if ratio > 0.85 and (not year or not cr_year or str(cr_year) == year) else "mismatch"
        results.append({"key": e["key"], "doi": clean, "status": status,
                        "detail": f"title similarity {ratio:.2f}; bib year {year or '?'} vs Crossref {cr_year or '?'}; "
                                  f"Crossref title: {cr_title[:100]}; container: {' '.join(msg.get('container-title', []) or [])[:80]}"})
    return results


# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic BibTeX/citation checks (stdlib only).")
    parser.add_argument("--bib", required=True, nargs="+", help=".bib file(s)")
    parser.add_argument("--tex", nargs="*", default=[], help=".tex file(s); \\input/\\include are followed")
    parser.add_argument("--online", action="store_true", help="verify DOIs against Crossref")
    parser.add_argument("--require-online", action="store_true", help="require resolved online DOI verification; implies --online")
    parser.add_argument("--mailto", default=None, help="contact email for Crossref polite pool")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    args.online = args.online or args.require_online
    for name in args.tex:
        if not Path(name).is_file():
            parser.error(f"missing manuscript file: {name}")

    entries = []
    for b in args.bib:
        p = Path(b)
        if not p.is_file():
            print(f"missing bib: {p}", file=sys.stderr)
            return 2
        entries += parse_bib(p.read_text(encoding="utf-8", errors="ignore"))
    bib_keys = {e["key"] for e in entries}
    cites = collect_cites([Path(t) for t in args.tex]) if args.tex else {}
    missing = {k: v for k, v in cites.items() if k not in bib_keys}
    uncited = sorted(bib_keys - set(cites)) if cites else []
    placeholders = {k: v for k, v in cites.items() if "PLACEHOLDER" in k.upper() or "VERIFY" in k.upper()}
    issues = check_entries(entries)
    online = check_online(entries, args.mailto) if args.online else []

    if args.require_online:
        checked = {r["key"] for r in online}
        online.extend({"key": e["key"], "doi": "", "status": "unresolved",
                       "detail": "No DOI available for this script; verify an authoritative record separately."}
                      for e in entries if e["key"] not in checked)
    errors = (len(missing) + len(placeholders)
              + sum(i["severity"] == "error" for i in issues)
              + sum(r["status"] == "mismatch" for r in online)
              + (sum(r["status"] == "unresolved" for r in online) if args.require_online else 0))
    result = {"blocking_problems": errors, "entries": len(entries), "cited_keys": len(cites), "missing_keys": missing,
              "uncited_entries": uncited, "placeholders": placeholders, "issues": issues, "online": online}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    print(f"BibTeX check: {len(entries)} entries, {len(cites)} distinct cited keys")
    print(f"\nCited but missing from .bib: {len(missing)}")
    for k, locs in sorted(missing.items()):
        print(f"  {k}  ({', '.join(locs[:3])})")
    print(f"\nPlaceholder citations to resolve: {len(placeholders)}")
    for k, locs in sorted(placeholders.items()):
        print(f"  {k}  ({', '.join(locs[:3])})")
    if cites:
        print(f"\nIn .bib but never cited: {len(uncited)}")
        for k in uncited:
            print(f"  {k}")
    for sev in ("error", "warn", "info"):
        sel = [i for i in issues if i["severity"] == sev]
        print(f"\n{sev.upper()} ({len(sel)})")
        for i in sel:
            print(f"  {i['key']:<28} {i['issue']}  [{i['where']}]")
    if args.online:
        print(f"\nCrossref DOI verification ({len(online)})")
        for r in online:
            print(f"  {r['key']:<28} {r['status']:<10} {r['detail']}")
    print(f"\nSummary: {errors} blocking problem(s). Entries without DOI/URL stay [VERIFY ONLINE].")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
