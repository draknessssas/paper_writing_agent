---
name: ieee-submission-auditor
description: Run a final target IEEE journal submission-readiness audit. Use when the user asks to review paper quality, check completeness, audit claims before submission, check IEEE journal fit, or prepare a manuscript for IEEE journal submission.
argument-hint: "[main manuscript path] [figures/tables/bib/evidence package]"
---

# IEEE journal Submission Auditor

## Purpose

Perform a systematic reviewer-facing audit before submission.

Default output:

`working/submission_audit.md`

## Audit Dimensions

1. IEEE journal scope
   - Is the target-field contribution explicit?
   - Is it more than generic ML/control/optimization/theory/component characterization?

2. Manuscript structure
   - Does each section have a clear job?
   - Does the Introduction lead to a precise gap?
   - Do Methodology and Experiments support the stated contributions?

3. Claim evidence
   - Are major claims present in `working/claim_ledger.md`?
   - Are unsupported claims weakened or removed?

4. Citations
   - Are all cited keys present in `.bib`?
   - Are citation-backed claims fair?
   - Are placeholders explicitly marked?

5. Figures and tables
   - Are captions standalone?
   - Does text cite every figure/table?
   - Do figures/tables support the narrative?

6. Reproducibility and protocol
   - Are data/prototype conditions clear?
   - Are metrics, baselines, and evaluation protocols stated?

7. LaTeX and submission mechanics
   - Does the paper compile?
   - Are labels, references, units, and equations consistent?
   - Verify the latest IEEE journal author guidelines before relying on exact page limits, fee rules, or formatting requirements.

## Output Format

```md
# IEEE journal Submission Audit

## Verdict
ready | minor revision | major revision | not ready

| Severity | Issue | Evidence | Suggested fix |
|---|---|---|---|

## Blocking items

## Suggested final pass order
1.
2.
3.
```

## Rules

- Lead with blocking issues.
- Do not rewrite the paper unless requested.
- Do not invent guideline details; mark current-author-guideline checks as needing live verification when not verified in this turn.
