---
name: ieee-style-extractor
description: Compatibility alias for the older IEEE journal style extraction workflow. Use when an existing Claude Code setup calls /ieee-style-extractor; route the work to paper-corpus-ingest, author-style-profiler, journal-style-profiler, and topic-style-profiler.
argument-hint: "[my_papers|domain_papers|both]"
---

# IEEE journal Style Extractor Compatibility Alias

## Purpose

Keep older Claude Code links working while using the newer corpus-based architecture.

## Routing

Use the newer workflow:

1. Run `paper-corpus-ingest` on the relevant corpus.
2. Run `author-style-profiler` for `corpora/my_papers`.
3. Run `journal-style-profiler` for `corpora/domain_papers/journal_reference_set`.
4. Run `topic-style-profiler` for `corpora/domain_papers/topic_reference_set`.
5. Use `domain-style-profiler` only as a legacy combined fallback.

## Rules

- Extract style and writing workflow only.
- Do not copy wording from papers.
- Do not use old papers as current manuscript facts.
