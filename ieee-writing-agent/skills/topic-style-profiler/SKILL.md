---
name: topic-style-profiler
description: Build a topic-specific writing and validation-flow profile from closely related IEEE journal papers in corpora/domain_papers/topic_reference_set or processed/domain_papers/topic_reference_set. Use when the user has papers from the same topic, method family, or experimental style and wants to learn their argument structure without importing their facts.
argument-hint: "[processed/domain_papers/topic_reference_set]"
---

# Topic Style Profiler

## Purpose

Extract topic-specific manuscript architecture from highly related papers.

The default output should be:

`profiles/topic_style/current.md`

## Inputs

Preferred:
- `processed/domain_papers/topic_reference_set/`

Fallback:
- `corpora/domain_papers/topic_reference_set/` after running `paper-corpus-ingest`

## What To Extract

1. Problem framing
   - how the topic is motivated;
   - which technical bottlenecks recur;
   - how the gap is made precise.

2. Methodology architecture
   - what is explained first;
   - how equations, models, algorithms, circuits, devices, systems, or experiments are introduced;
   - how design implications are stated.

3. Validation ladder
   - what evidence appears first;
   - which baselines are used;
   - how stress cases, ablations, simulations, experiments, or hardware tests are ordered.

4. Figure/table strategy
   - common figure roles;
   - caption style;
   - where tables are used.

5. Claim boundaries
   - what similar papers claim strongly;
   - what they state cautiously;
   - what they leave as limitation or future work.

## Output File Format

Create or update `profiles/topic_style/current.md`:

```md
# Topic-Specific IEEE Writing Profile

## Source corpus
- Topic:
- Number of papers:
- Processed folder:
- Date generated:

## Topic framing

## Introduction gap pattern

## Method / system / analysis pattern

## Validation ladder

## Figure and table roles

## Comparison and ablation habits

## Claim boundaries

## Do not import as facts
- Paper-specific results
- Paper-specific baselines
- Paper-specific claims
- Paper-specific language
```

## Rules

- This profile learns how similar papers build an argument, not what the current paper proves.
- Do not reuse old results or old claims as current manuscript evidence.
- Do not copy wording from related papers.
