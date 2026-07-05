---
name: ieee-claim-ledger
description: Build or audit an IEEE journal manuscript claim ledger. Use when the user asks to check claims, evidence, overclaiming, contribution wording, result support, or whether a sentence can be stated in the manuscript.
argument-hint: "[manuscript path or pasted section] [evidence paths]"
---

# IEEE journal Claim Ledger

## Purpose

Create a claim-evidence ledger before manuscript prose becomes too polished.

Default output:

`working/claim_ledger.md`

## Claim Types

- scope claim;
- literature/background claim;
- method contribution;
- modeling or control mechanism;
- experimental setup;
- quantitative result;
- comparison;
- limitation;
- conclusion or implication.

## Workflow

1. Extract candidate claims from the manuscript section, draft paragraph, table, figure, or user notes.
2. For each claim, identify the strongest available evidence:
   - manuscript figure/table;
   - saved metric/report;
   - code/notebook/script;
   - current user statement;
   - cited reference;
   - missing.
3. Assign a status:
   - `supported`;
   - `needs weaker wording`;
   - `needs citation`;
   - `needs experimental evidence`;
   - `remove or mark as future work`.
4. Write allowed wording and forbidden stronger wording.
5. For the target IEEE journal, check whether each major claim makes the target-field contribution explicit.

## Output Format

```md
# IEEE journal Claim Ledger

| ID | Claim | Type | Evidence | Status | Allowed wording | Forbidden stronger wording |
|---|---|---|---|---|---|---|

## Blocking gaps
- [NEED: ...]

## Safe contribution wording
- ...
```

## Rules

- Do not turn a plan, hypothesis, or intuition into a result claim.
- Do not use style corpora as evidence for current-paper facts.
- Do not strengthen comparative wording unless the metric, baseline, condition, and protocol are clear.
- Use `[NEED: ...]` for missing support.
