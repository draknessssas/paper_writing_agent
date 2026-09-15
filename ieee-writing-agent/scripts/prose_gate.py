#!/usr/bin/env python3
"""Mechanical prose gate for manuscript paragraphs (stdlib only).

Mirrors the lexicon in knowledge/prose_patterns.md; see prose_quality.md for semantics. Three tiers:
  BAN   must be fixed before text is returned (exit code 1 while any remain)
  AUDIT keep only with a written justification
  COUNT reported, not judged (passive heuristic, sentence stats, word counts)

Usage:
  python scripts/prose_gate.py draft.md            # text report, exit 1 on BAN hits
  python scripts/prose_gate.py draft.tex --json    # machine-readable
  python scripts/prose_gate.py draft.md --no-fail  # always exit 0
  python scripts/prose_gate.py --list              # print the lexicon
  cat draft.md | python scripts/prose_gate.py -    # read stdin

LaTeX comments, citations, references, labels, and math are stripped before
matching, so symbol names and cite keys do not trigger word rules.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Lexicon. Each rule: id, tier, name, phrases (literal, case-insensitive,
# word-boundary), optional "initial" (sentence-initial only), optional regex.
# Keep every literal phrase present in knowledge/prose_patterns.md (parity check).
# ---------------------------------------------------------------------------
RULES: list[dict] = [
    {"id": "B1", "tier": "BAN", "name": "hype adjectives",
     "phrases": ["groundbreaking", "cutting-edge", "unprecedented", "remarkable",
                 "impressive", "revolutionary", "game-changing", "seamless", "seamlessly",
                 "holistic", "synergistic"]},
    {"id": "B2", "tier": "AUDIT", "name": "audit adjectives (need a number, test, or benchmark)",
     "phrases": ["novel", "significant", "substantial", "comprehensive", "robust", "powerful",
                 "state-of-the-art", "promising", "excellent", "paradigm"]},
    {"id": "B3", "tier": "BAN", "name": "hype verbs",
     "phrases": ["unlock", "unlocks", "paves the way", "pave the way", "opens the door",
                 "open the door", "opens new avenues", "revolutionize", "revolutionizes",
                 "empower", "empowers", "delve", "delves", "delving", "harness", "harnesses"]},
    {"id": "B4", "tier": "AUDIT", "name": "audit verbs (prefer plain verbs)",
     "phrases": ["leverage", "leverages", "leveraging", "facilitate", "facilitates"]},
    {"id": "B5", "tier": "BAN", "name": "throat-clearing openers",
     "phrases": ["It is worth noting that", "It should be noted that", "It is worth mentioning that",
                 "It can be seen that", "It is obvious that", "It is evident that", "It is clear that",
                 "As we all know", "As is well known", "As is known to all", "It is well known that",
                 "Needless to say"]},
    {"id": "B5i", "tier": "BAN", "name": "throat-clearing sentence openers", "initial": True,
     "phrases": ["Notably", "Importantly", "Crucially", "Ultimately"]},
    {"id": "B6", "tier": "AUDIT", "name": "connective openers (at most one per paragraph)", "initial": True,
     "phrases": ["Moreover", "Furthermore", "Additionally", "Besides", "What is more"]},
    {"id": "B7", "tier": "BAN", "name": "content-free opener",
     "phrases": ["In this section, we"]},
    {"id": "B7a", "tier": "AUDIT", "name": "\"In this paper/article, we\" (once in Introduction, once in Conclusion)",
     "phrases": ["In this paper, we", "In this article, we"]},
    {"id": "B11", "tier": "BAN", "name": "vacuous intensifiers",
     "phrases": ["truly", "genuinely", "in essence", "in effect", "essentially", "actually",
                 "in fact", "indeed"]},
    {"id": "B11a", "tier": "AUDIT", "name": "\"simply\" (keep only as a mathematical statement)",
     "phrases": ["simply"]},
    {"id": "B12", "tier": "BAN", "name": "weak qualifiers",
     "phrases": ["very", "quite", "fairly", "pretty", "somewhat"],
     "regex": [r"\brather\b(?!\s+than\b)"]},
    {"id": "B12a", "tier": "AUDIT", "name": "\"relatively\" (needs a stated comparison)",
     "phrases": ["relatively"]},
    {"id": "B13", "tier": "AUDIT", "name": "generic closers",
     "phrases": ["holds great promise", "which is of great importance"]},
    {"id": "B15", "tier": "AUDIT", "name": "agentless observation chains",
     "phrases": ["it is found that", "it was observed that", "it was found that", "was found to",
                 "were found to"]},
    {"id": "A4", "tier": "AUDIT", "name": "defensive red flags",
     "phrases": ["unfortunately", "fails to", "we were unable", "we attempted to", "we tried to",
                 "severe weakness", "severe drawback", "not ideal", "disappointing",
                 "poor performance", "merely"]},
    {"id": "C1", "tier": "BAN", "name": "development/attention boilerplate",
     "phrases": ["with the rapid development of", "with the development of", "more and more",
                 "has attracted more and more attention", "attracted increasing attention",
                 "attracted extensive attention"]},
    {"id": "C2", "tier": "AUDIT", "name": "time filler",
     "phrases": ["in recent years", "has been widely studied"]},
    {"id": "C2i", "tier": "AUDIT", "name": "\"Recently\" as opener", "initial": True,
     "phrases": ["Recently"]},
    {"id": "C2b", "tier": "BAN", "name": "\"nowadays\"",
     "phrases": ["nowadays"]},
    {"id": "C3", "tier": "AUDIT", "name": "insecurity adverbs (cite or delete)",
     "phrases": ["obviously", "clearly"]},
    {"id": "C4", "tier": "BAN", "name": "\"aiming at\" (use \"to address\")",
     "phrases": ["aiming at the problem", "aiming at"]},
    {"id": "C5", "tier": "AUDIT", "name": "performance words without a number",
     "phrases": ["good performance", "better performance", "excellent performance", "high accuracy",
                 "high efficiency", "low loss"]},
    {"id": "C6", "tier": "BAN", "name": "pluralized uncountables",
     "phrases": ["researches", "literatures", "equipments", "informations"]},
    {"id": "C12", "tier": "AUDIT", "name": "open-ended lists",
     "phrases": ["etc.", "and so on"]},
    {"id": "C13", "tier": "BAN", "name": "light-verb constructions",
     "phrases": ["make a comparison", "perform an analysis", "carry out an analysis",
                 "give a description", "conduct an investigation", "make use of"]},
    {"id": "C14", "tier": "BAN", "name": "connector errors",
     "phrases": ["can not", "in the meanwhile", "what's more"]},
    {"id": "C14a", "tier": "AUDIT", "name": "connector misuse",
     "phrases": ["on the contrary", "at the same time"]},
    {"id": "C15", "tier": "BAN", "name": "ordinal adverbs",
     "phrases": ["firstly", "secondly", "thirdly", "lastly"]},
    {"id": "C17", "tier": "BAN", "name": "redundant pairs",
     "phrases": ["first and foremost", "each and every", "basic fundamentals", "past history",
                 "as a matter of fact"]},
    {"id": "C18", "tier": "BAN", "name": "wordy fillers",
     "phrases": ["in order to", "due to the fact that", "the fact that", "a number of",
                 "a large number of", "a lot of", "at the present time", "at this point in time",
                 "in the event that", "has the ability to", "the majority of", "utilize", "utilizes",
                 "utilization", "prior to", "subsequent to", "for the purpose of",
                 "in spite of the fact that", "plays a crucial role", "plays a vital role",
                 "plays an important role"]},
    {"id": "C18a", "tier": "AUDIT", "name": "fillers to justify",
     "phrases": ["in terms of", "is able to", "carry out", "with the aim of"]},
]

HEDGES = ["may", "might", "could", "possibly", "potentially", "perhaps", "seems", "seem",
          "appears", "appear", "likely", "somewhat", "relatively", "to some extent", "arguably"]

COUNT_WORDS = ["only", "respectively", "the proposed"]

PASSIVE_RE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(\w+ed|\w+en|built|made|shown|given|taken|"
    r"found|done|seen|known|written|driven|chosen|set|put|kept|held|led|fed|met|cut|hit|split)\b",
    re.IGNORECASE)

ABBREV = ["Fig.", "Figs.", "Eq.", "Eqs.", "Sec.", "Secs.", "Ref.", "Refs.", "et al.", "e.g.", "i.e.",
          "vs.", "cf.", "approx.", "No.", "Vol.", "pp.", "Dr.", "Prof.", "Tab.", "Ch."]


# ---------------------------------------------------------------------------
# LaTeX / markdown cleaning
# ---------------------------------------------------------------------------
ENV_RE = re.compile(r"\\begin\{(equation|align|eqnarray|gather|multline|figure|table|tabular|"
                    r"algorithm|algorithmic|lstlisting|verbatim)\*?\}.*?\\end\{\1\*?\}", re.S)
CMD_ARG_RE = re.compile(r"\\(cite[a-zA-Z]*|ref|eqref|label|autoref|cref|Cref|includegraphics|input|"
                        r"include|bibliography|bibliographystyle|url|href)\*?(\[[^\]]*\])?\{[^}]*\}")
KEEP_ARG_RE = re.compile(r"\\(textit|emph|textbf|textrm|texttt|underline|text|mathrm|section|"
                         r"subsection|subsubsection|caption|title)\*?\{([^{}]*)\}")


def strip_comments_and_math(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = ENV_RE.sub(" ", text)
    text = re.sub(r"\$\$.*?\$\$", " MATH ", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]", " MATH ", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", " MATH ", text, flags=re.S)
    text = re.sub(r"(?<!\\)\$[^$\n]*\$", " MATH ", text)
    return text


def strip_latex(text: str) -> str:
    text = strip_comments_and_math(text)
    text = CMD_ARG_RE.sub(" REF ", text)
    text = KEEP_ARG_RE.sub(r"\2", text)
    text = re.sub(r"\\[A-Za-z]+\*?(\[[^\]]*\])?", " ", text)
    text = text.replace("{", "").replace("}", "")
    # markdown emphasis markers
    text = re.sub(r"[*_]{1,3}", "", text)
    return text


def split_sentences(text: str) -> list[str]:
    protected = text
    for abbr in ABBREV:
        protected = protected.replace(abbr, abbr.replace(".", "<DOT>"))
    protected = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", protected)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\[\"'])", protected)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def word_count(sentence: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][\w'-]*", sentence))


def is_sentence_initial(text: str, start: int) -> bool:
    before = text[:start].rstrip()
    return not before or before.endswith((".", "!", "?", ":", ";"))


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------
def phrase_regex(phrase: str) -> re.Pattern:
    escaped = re.escape(phrase).replace(r"\ ", r"\s+")
    # treat "etc." specially: trailing dot is literal, no trailing word boundary
    if phrase.endswith("."):
        return re.compile(r"(?<![\w-])" + escaped, re.IGNORECASE)
    return re.compile(r"(?<![\w-])" + escaped + r"(?![\w-])", re.IGNORECASE)


def scan(text: str) -> tuple[list[dict], dict]:
    hits: list[dict] = []
    lines = text.splitlines()

    # multi-line environments: mark lines inside math/figure environments
    cleaned_lines = strip_latex(text).splitlines()
    # strip_latex may join lines when removing environments; fall back per line
    if len(cleaned_lines) != len(lines):
        cleaned_lines = [strip_latex(line) for line in lines]

    for rule in RULES:
        patterns = [phrase_regex(p) for p in rule.get("phrases", [])]
        patterns += [re.compile(r, re.IGNORECASE) for r in rule.get("regex", [])]
        for lineno, line in enumerate(cleaned_lines, start=1):
            for pat in patterns:
                for m in pat.finditer(line):
                    if rule.get("initial") and not is_sentence_initial(line, m.start()):
                        continue
                    snippet = line[max(0, m.start() - 40): m.end() + 40].strip()
                    hits.append({"tier": rule["tier"], "rule": f"{rule['id']} {rule['name']}",
                                 "term": m.group(0), "line": lineno, "snippet": snippet})

    # dashes (on comment/math-stripped raw text so LaTeX --- is visible)
    raw = strip_comments_and_math(text)
    for lineno, line in enumerate(raw.splitlines(), start=1):
        for m in re.finditer(r"—|(?<!-)---(?!-)", line):
            hits.append({"tier": "BAN", "rule": "B10 em dash in prose", "term": m.group(0),
                         "line": lineno, "snippet": line[max(0, m.start() - 40): m.end() + 40].strip()})
        for m in re.finditer(r"–|(?<!-)--(?!-)", line):
            left = line[m.start() - 1] if m.start() > 0 else " "
            right = line[m.end()] if m.end() < len(line) else " "
            if left.isalnum() and right.isalnum():
                continue  # tight range (40–50) or IEEE compound (dc–dc, B–H, voltage–current): allowed
            hits.append({"tier": "AUDIT", "rule": "B10 spaced en dash used as a parenthetical dash (en dash is for tight ranges and compounds)",
                         "term": m.group(0), "line": lineno,
                         "snippet": line[max(0, m.start() - 40): m.end() + 40].strip()})
        for m in re.finditer(r"!(?!\[)", line):
            hits.append({"tier": "BAN", "rule": "B18 exclamation mark", "term": "!", "line": lineno,
                         "snippet": line[max(0, m.start() - 40): m.end() + 40].strip()})
        for m in re.finditer(r"\?", line):
            hits.append({"tier": "AUDIT", "rule": "B18 question mark (at most one, Introduction only)",
                         "term": "?", "line": lineno,
                         "snippet": line[max(0, m.start() - 40): m.end() + 40].strip()})

    # sentence-level statistics and hedge stacks
    cleaned = strip_latex(text)
    sentences = split_sentences(re.sub(r"\s+", " ", cleaned))
    lengths = [word_count(s) for s in sentences if word_count(s) > 0]
    long_sentences = [(n, s) for n, s in zip(lengths, sentences) if n > 40]
    hedge_pats = [phrase_regex(h) for h in HEDGES]
    hedge_stacks = []
    for s in sentences:
        found = [h for h, p in zip(HEDGES, hedge_pats) if p.search(s)]
        if len(found) >= 2:
            hedge_stacks.append({"hedges": found, "sentence": s[:160]})
            hits.append({"tier": "AUDIT", "rule": "A2 hedge stack (two or more hedges in one sentence)",
                         "term": ", ".join(found), "line": 0, "snippet": s[:120]})
    passive_hits = [s for s in sentences if PASSIVE_RE.search(s)]
    counts = {w: len(phrase_regex(w).findall(cleaned)) for w in COUNT_WORDS}

    stats = {
        "sentences": len(lengths),
        "mean_words": round(sum(lengths) / len(lengths), 1) if lengths else 0.0,
        "max_words": max(lengths) if lengths else 0,
        "over_40": [{"words": n, "sentence": s[:160]} for n, s in long_sentences],
        "passive_sentences": len(passive_hits),
        "passive_examples": [s[:120] for s in passive_hits[:5]],
        "counts": counts,
        "hedge_stacks": hedge_stacks,
    }
    return hits, stats


def report(path_label: str, hits: list[dict], stats: dict) -> str:
    out = [f"Prose gate: {path_label}"]
    for tier in ("BAN", "AUDIT"):
        tier_hits = [h for h in hits if h["tier"] == tier]
        out.append(f"\n{tier} hits: {len(tier_hits)}")
        by_rule: dict[str, list[dict]] = {}
        for h in tier_hits:
            by_rule.setdefault(h["rule"], []).append(h)
        for rule, items in by_rule.items():
            out.append(f"  [{rule}] x{len(items)}")
            for h in items[:8]:
                loc = f"L{h['line']}" if h["line"] else "sent"
                out.append(f"      {loc}: '{h['term']}'  ...{h['snippet']}...")
            if len(items) > 8:
                out.append(f"      ... {len(items) - 8} more")
    out.append("\nCOUNT")
    out.append(f"  sentences: {stats['sentences']}, mean words: {stats['mean_words']}, "
               f"max words: {stats['max_words']} (target mean 18-25, max 40)")
    for item in stats["over_40"]:
        out.append(f"  over 40 words ({item['words']}): {item['sentence']}")
    out.append(f"  passive-voice heuristic: {stats['passive_sentences']} of {stats['sentences']} sentences")
    for ex in stats["passive_examples"]:
        out.append(f"      {ex}")
    for w, n in stats["counts"].items():
        out.append(f"  '{w}': {n}")
    ban = sum(1 for h in hits if h["tier"] == "BAN")
    audit = sum(1 for h in hits if h["tier"] == "AUDIT")
    out.append(f"\nSummary: BAN {ban}, AUDIT {audit}. "
               + ("Fix all BAN hits before returning the text." if ban else "No BAN hits."))
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mechanical prose gate (stdlib only).")
    parser.add_argument("path", nargs="?", help="file to check, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--no-fail", action="store_true", help="always exit 0")
    parser.add_argument("--list", action="store_true", help="print the lexicon and exit")
    args = parser.parse_args()

    if args.list:
        if args.json:
            print(json.dumps({"rules": RULES, "hedges": HEDGES, "count_words": COUNT_WORDS},
                             indent=2, ensure_ascii=False))
        else:
            for rule in RULES:
                print(f"{rule['tier']:<5} {rule['id']:<5} {rule['name']}")
                print("      " + ", ".join(rule.get("phrases", []) + rule.get("regex", [])))
        return 0
    if not args.path:
        parser.error("path is required (or --list)")

    if args.path == "-":
        text = sys.stdin.read()
        label = "<stdin>"
    else:
        p = Path(args.path)
        if not p.is_file():
            print(f"not a file: {p}", file=sys.stderr)
            return 2
        text = p.read_text(encoding="utf-8", errors="ignore")
        label = str(p)

    hits, stats = scan(text)
    ban = sum(1 for h in hits if h["tier"] == "BAN")
    if args.json:
        print(json.dumps({"file": label, "hits": hits, "stats": stats, "ban": ban,
                          "audit": sum(1 for h in hits if h["tier"] == "AUDIT")},
                         indent=2, ensure_ascii=False))
    else:
        print(report(label, hits, stats))
    if ban and not args.no_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
