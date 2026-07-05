---
name: domain-style-profiler
description: Build a combined discipline/journal/topic writing style profile from complete professional reference papers. Use as a legacy or fallback profiler when journal-style-profiler and topic-style-profiler are not separated.
argument-hint: "[processed/domain_papers/<collection>]"
---

# Domain Style Profiler

## Purpose

Extract genre-level writing conventions from professional academic papers in the target field. Prefer `journal-style-profiler` and `topic-style-profiler` when the user separates broad journal papers from highly related topic papers.

The output should be saved to:

`profiles/domain_style/current.md`

## Inputs

Preferred:
- `processed/domain_papers/journal_reference_set/`
- `processed/domain_papers/topic_reference_set/`

Other possible folders:
- any user-provided processed reference corpus.

## What To Extract

1. Journal/field writing flow
   - typical section order;
   - typical Introduction arc;
   - how the problem is motivated;
   - how prior art is grouped;
   - how the research gap is stated;
   - how contributions are listed;
   - how validation is introduced.

2. Technical discourse style
   - terminology density;
   - use of converter/control/modeling language;
   - equation-to-text explanation style;
   - figure/table reference style;
   - use of quantitative evidence.

3. IEEE journal-style claim discipline
   - how strongly claims are stated;
   - how experiments are used;
   - how limitations are framed;
   - how comparison baselines are introduced.

4. Rhetorical templates
   Use abstract patterns only, not copied wording:
   - Context -> bottleneck -> limitation -> gap.
   - Existing category A/B/C -> unresolved issue -> need for new approach.
   - Model assumption -> derived relationship -> design implication.
   - Measurement condition -> observed result -> comparison -> interpretation.

5. Common section roles
   - Abstract role sequence;
   - Introduction paragraph sequence;
   - Method paragraph sequence;
   - Experiment paragraph sequence;
   - Conclusion sequence.

## Output File Format

Create or update `profiles/domain_style/current.md`:

```md
# Domain / IEEE Writing Style Profile

## Source corpus
- Collection:
- Number of papers:
- Processed folder:
- Date generated:

## Target field and journal
Target field / target IEEE journal writing

## Overall writing flow

## Introduction workflow
1.
2.
3.

## Prior-art grouping habits

## Gap-statement patterns

## Contribution-list patterns

## Method-section writing patterns

## Experimental-section writing patterns

## Result-interpretation patterns

## Language and tone

## Rhetorical templates
Use these as abstract structures only:
- ...

## Forbidden imitation
- Do not copy wording.
- Do not copy paper-specific claims.
- Do not copy old results.
- Do not imitate one author's distinctive voice.
```

## Rules

- This profile captures field/journal conventions, not private facts.
- Do not extract long phrases.
- Do not create reusable sentences copied from reference papers.
- Keep the profile usable for future manuscripts in the same area.
