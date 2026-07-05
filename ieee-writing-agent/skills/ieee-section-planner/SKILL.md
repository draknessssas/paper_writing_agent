---
name: ieee-section-planner
description: Plan a full IEEE journal manuscript or a major section before drafting. Use when the user asks for paper structure, section order, contribution framing, Introduction flow, Methodology layout, Results narrative, or paragraph-by-paragraph writing plans.
argument-hint: "[paper topic] [evidence packet] [target section or full paper]"
---

# IEEE journal Section Planner

## Purpose

Design the argument before writing sentences.

Default output:

`working/section_plan.md`

## Intake

Before planning, identify:
- target manuscript type;
- current contribution;
- IEEE journal scope hook;
- core evidence;
- key figures/tables;
- comparison baselines;
- claim boundaries;
- missing information.

## Default IEEE journal Architecture

Use this as a starting point, then adapt to the manuscript:

1. Abstract: problem -> proposed approach -> physical mechanism -> validation -> main evidence -> implication.
2. Introduction: application context -> technical bottleneck -> prior-art groups -> unresolved gap -> proposed approach -> contributions.
3. Methodology: objective -> model/control/design structure -> physical role of each component -> compact equations -> implementation details.
4. Experimental or evaluation setup: data/prototype -> conditions -> metrics -> baselines -> protocol.
5. Results and comparison: baseline behavior -> main result -> stress cases -> ablation -> competing methods -> physical interpretation.
6. Conclusion: contribution -> decisive evidence -> boundary -> implication.

## Workflow

1. Build a one-sentence argument:
   `In [target-field problem], this paper shows [advance] using [approach], supported by [evidence], within [boundary].`
2. Map each major claim to a planned figure/table/experiment.
3. Assign one job to each paragraph.
4. Choose where claim ledger, citation audit, and figure-caption work are needed.
5. Produce a section plan that can drive `ieee-paragraph-writer`.

## Output Format

```md
# IEEE journal Section Plan

## One-sentence argument

## Section outline

## Paragraph map
| Section | Paragraph role | Evidence | Risk |
|---|---|---|---|

## Required figures/tables

## Missing inputs
- [NEED: ...]
```

## Rules

- Do not plan claims that the evidence cannot support.
- Do not bury the target-field contribution behind generic algorithms.
- Keep methods and experiments ordered by narrative logic, not habit.
