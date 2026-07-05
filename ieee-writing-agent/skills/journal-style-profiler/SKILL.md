---
name: journal-style-profiler
description: Build a broad target IEEE journal writing style and workflow profile from complete papers in corpora/domain_papers/journal_reference_set or processed/domain_papers/journal_reference_set. Use when the user wants to learn a journal's article flow, tone, claim discipline, and section conventions without copying wording.
argument-hint: "[processed/domain_papers/journal_reference_set]"
---

# Journal Style Profiler

## Purpose

Extract broad target-journal writing conventions from complete papers published in the same IEEE journal or closely comparable IEEE venues.

The default output should be:

`profiles/journal_style/current.md`

## Inputs

Preferred:
- `processed/domain_papers/journal_reference_set/`

Fallback:
- `corpora/domain_papers/journal_reference_set/` after running `paper-corpus-ingest`

## What To Extract

1. Journal-level article architecture
   - section order;
   - abstract structure;
   - Introduction arc;
   - contribution-list style;
   - conclusion style.

2. Journal tone
   - claim strength;
   - preferred technical density;
   - how much implementation detail is typical;
   - how limitations are stated.

3. Evidence presentation
   - how figures/tables are introduced;
   - how comparisons are framed;
   - how experiments, simulations, or analyses are connected to claims.

4. Reusable rhetorical templates
   Use abstract structures only:
   - context -> bottleneck -> limitation -> gap;
   - method principle -> implementation detail -> evidence;
   - condition -> observation -> comparison -> interpretation.

## Output File Format

Create or update `profiles/journal_style/current.md`:

```md
# IEEE Journal Writing Style Profile

## Source corpus
- Target journal:
- Number of papers:
- Processed folder:
- Date generated:

## Overall journal writing flow

## Abstract pattern

## Introduction workflow

## Contribution-list patterns

## Method / analysis section patterns

## Experiment / results section patterns

## Figure and table integration

## Claim strength and reviewer-safe wording

## Things not to imitate
- Paper-specific facts
- Paper-specific claims
- Distinctive sentences
```

## Rules

- Extract journal conventions, not current-paper facts.
- Do not copy sentences.
- Do not let one paper dominate the profile.
- Keep this profile broad enough to be reused for future papers targeting the same journal.
