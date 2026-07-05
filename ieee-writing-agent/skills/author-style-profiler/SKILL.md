---
name: author-style-profiler
description: Build or refresh the user's personal academic writing style profile from complete papers in corpora/my_papers or processed/my_papers. Use when the user wants the agent to mimic their own writing style without manually selecting paragraphs.
argument-hint: "[processed/my_papers]"
---

# Author Style Profiler

## Purpose

Extract the user's high-level writing style from the user's own complete papers.

The result should be saved to:

`profiles/author_style/current.md`

## Inputs

Preferred:
- `processed/my_papers/`

Fallback:
- `corpora/my_papers/` after running `paper-corpus-ingest`

## Analysis Dimensions

Analyze the user's writing style by section:

1. Abstract
   - opening pattern;
   - problem statement style;
   - method summary style;
   - result reporting style;
   - claim strength.

2. Introduction
   - broad-to-specific transition;
   - prior-art grouping style;
   - gap construction;
   - contribution-list phrasing;
   - use of "this paper" vs "we".

3. Method/model/control sections
   - how equations are introduced;
   - how physical mechanisms are explained;
   - how design implications are stated;
   - density of technical details.

4. Experimental/results sections
   - setup description style;
   - waveform/result interpretation;
   - baseline comparison style;
   - quantitative evidence phrasing.

5. Conclusion
   - summary style;
   - limitation/future-work style;
   - claim restraint.

## Output File Format

Create or update `profiles/author_style/current.md`:

```md
# Author Writing Style Profile

## Source corpus
- Number of papers:
- Processed folder:
- Date generated:

## Global style summary

## Section-specific style

### Abstract

### Introduction

### Method / Modeling / Control

### Experimental Results

### Conclusion

## Paragraph architecture patterns

## Sentence rhythm

## Transition patterns

## Claim strength

## Contribution phrasing

## Preferred rhetorical moves

## Weaknesses to correct

## Things not to imitate
- Old technical claims
- Old experimental results
- Old citations
- Repeated phrases that are too paper-specific

## Operational writing rules
1.
2.
3.
```

## Rules

- Extract style, not technical content.
- Do not copy distinctive sentences.
- Do not preserve old paper claims as reusable claims.
- Do not include long verbatim examples.
- If the user's corpus contains different writing styles, describe the dominant style and section-specific variations.
