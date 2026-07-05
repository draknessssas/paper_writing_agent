#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "skills/paper-corpus-ingest/SKILL.md",
    "skills/author-style-profiler/SKILL.md",
    "skills/journal-style-profiler/SKILL.md",
    "skills/topic-style-profiler/SKILL.md",
    "skills/domain-style-profiler/SKILL.md",
    "skills/intro-reference-miner/SKILL.md",
    "skills/ieee-paragraph-writer/SKILL.md",
    "skills/ieee-reviewer/SKILL.md",
    "skills/ieee-style-extractor/SKILL.md",
    "skills/ieee-claim-ledger/SKILL.md",
    "skills/ieee-citation-verifier/SKILL.md",
    "skills/ieee-section-planner/SKILL.md",
    "skills/ieee-figure-caption-writer/SKILL.md",
    "skills/ieee-submission-auditor/SKILL.md",
    "skills/ieee-response-writer/SKILL.md",
    "skills/ieee-page-compressor/SKILL.md",
    ".claude/agents/ieee-writing-agent.md",
    ".claude/agents/corpus-analyst.md",
    ".claude/agents/ieee-technical-skeptic.md",
    ".claude/output-styles/ieee-writer.md",
    ".codex/agents/ieee-writer/config.toml",
    ".codex/agents/ieee-writer/AGENTS.md",
    ".codex/agents/corpus-analyst/config.toml",
    ".codex/agents/corpus-analyst/AGENTS.md",
    ".codex/agents/ieee-technical-skeptic/config.toml",
    ".codex/agents/ieee-technical-skeptic/AGENTS.md",
    "profiles/active_profile.yml",
    "profiles/author_style/current.md",
    "profiles/journal_style/current.md",
    "profiles/topic_style/current.md",
    "profiles/domain_style/current.md",
    "working/intro_reference_map.md",
    "templates/md-inputs/author-paper.md",
    "templates/md-inputs/domain-paper.md",
    "templates/md-inputs/current-intro-reference.md",
    "templates/md-inputs/current-manuscript-brief.md",
    "templates/md-inputs/evidence-packet.md",
    "templates/md-inputs/reviewer-comments.md",
    "corpora/README.md",
    "profiles/README.md",
    "working/README.md",
]

SKILLS = [
    "paper-corpus-ingest",
    "author-style-profiler",
    "journal-style-profiler",
    "topic-style-profiler",
    "domain-style-profiler",
    "intro-reference-miner",
    "ieee-paragraph-writer",
    "ieee-reviewer",
    "ieee-style-extractor",
    "ieee-claim-ledger",
    "ieee-citation-verifier",
    "ieee-section-planner",
    "ieee-figure-caption-writer",
    "ieee-submission-auditor",
    "ieee-response-writer",
    "ieee-page-compressor",
]


def status(path: Path) -> str:
    if path.is_symlink():
        target = path.readlink()
        return f"link -> {target}"
    if path.exists():
        return "ok"
    return "missing"


def main() -> int:
    print("IEEE journal writing workspace status\n")
    for item in PATHS:
        path = ROOT / item
        print(f"{status(path):<32} {item}")

    print("\nSkill links")
    for skill in SKILLS:
        codex_link = ROOT / ".agents" / "skills" / skill
        claude_link = ROOT / ".claude" / "skills" / skill
        print(f"{status(codex_link):<32} .agents/skills/{skill}")
        print(f"{status(claude_link):<32} .claude/skills/{skill}")

    print("\nCorpus counts")
    for folder in [
        "corpora/my_papers",
        "corpora/domain_papers/journal_reference_set",
        "corpora/domain_papers/topic_reference_set",
        "corpora/current_intro_refs",
        "processed/my_papers",
        "processed/domain_papers/journal_reference_set",
        "processed/domain_papers/topic_reference_set",
        "processed/current_intro_refs",
    ]:
        path = ROOT / folder
        count = sum(1 for child in path.rglob("*") if child.is_file()) if path.exists() else 0
        print(f"{count:<32} {folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
