@AGENTS.md

# Claude Code Specific Behavior

This is a manuscript-writing workspace, not a normal software-only project.

Prefer these skills:
- `/paper-corpus-ingest` when the user provides complete papers or asks to process corpora.
- `/author-style-profiler` when the user wants to extract or refresh their own writing style.
- `/journal-style-profiler` when the user wants to extract broad target IEEE journal writing flow.
- `/topic-style-profiler` when the user wants to extract same-topic article architecture and validation flow.
- `/domain-style-profiler` only as a legacy combined profiler when journal/topic profiles are not separated.
- `/intro-reference-miner` when the user provides reference papers for writing an Introduction.
- `/ieee-section-planner` when the user wants full-paper structure, section order, or paragraph maps.
- `/ieee-claim-ledger` before strengthening contribution, result, comparison, or conclusion claims.
- `/ieee-citation-verifier` when adding, checking, or repairing citations and BibTeX entries.
- `/ieee-paragraph-writer` when drafting or revising a paragraph.
- `/ieee-figure-caption-writer` when writing captions, table notes, or figure callouts.
- `/ieee-reviewer` when checking a paragraph or section.
- `/ieee-submission-auditor` for final pre-submission review.
- `/ieee-response-writer` when drafting reviewer responses or revision plans.
- `/ieee-page-compressor` when shortening a manuscript while preserving claims and evidence.

Prefer these agents:
- `ieee-writing-agent` for autonomous paragraph drafting or revision.
- `corpus-analyst` for large processed-corpus inspection.
- `ieee-technical-skeptic` for evidence and reviewer-risk checks.

When processing complete papers, first convert raw files into `processed/`, then analyze the processed files. Do not load many full raw papers into the main context at once.

When drafting, use current conversation facts first. Do not treat style corpora as current manuscript evidence.

For large corpus analysis, use subagents where helpful to preserve the main conversation context.

Markdown inputs are accepted. Use `templates/md-inputs/` as examples for author papers, domain references, current reference summaries, evidence packets, manuscript briefs, and reviewer comments.
