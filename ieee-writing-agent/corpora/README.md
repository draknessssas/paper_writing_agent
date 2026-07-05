# Corpora Inputs

This folder stores reusable paper corpora.

Markdown is accepted and often preferred when the source paper has already been cleaned.

## Author Style

Put the user's own complete papers here:

```text
corpora/my_papers/
```

Use this for personal writing style only. Do not reuse old claims, old results, or old citations as current manuscript facts.

Recommended amount: 3-5 high-quality papers, up to 8 if the style is consistent.

## Journal Style

Put broad target IEEE journal reference papers here:

```text
corpora/domain_papers/journal_reference_set/
```

Use this for journal-level writing flow, section architecture, tone, claim discipline, and evidence presentation.

Recommended amount: 10-15 papers.

## Topic-Specific Style

Put highly related same-topic papers here:

```text
corpora/domain_papers/topic_reference_set/
```

Use this for topic-specific article architecture, validation ladder, figure/table strategy, and claim boundaries.

Recommended amount: 5-8 papers.

## Current Introduction References

Put references that are actively used for the current manuscript Introduction here:

```text
corpora/current_intro_refs/
```

Use this for citation anchors, prior-art categories, and research-gap construction.

Recommended amount: 8-12 papers.

Full papers are acceptable in this folder. They are mined for the current manuscript's citation map and prior-art positioning, not for long-term writing style.

## Templates

Use:

```text
templates/md-inputs/author-paper.md
templates/md-inputs/domain-paper.md
templates/md-inputs/current-intro-reference.md
```
