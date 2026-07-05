---
name: ieee-response-writer
description: Draft or audit IEEE journal reviewer response letters and revision plans. Use when the user provides reviewer comments, editor decisions, rebuttal notes, revision tables, or asks how to respond to IEEE journal reviewers.
argument-hint: "[reviewer comments] [revision evidence]"
---

# IEEE journal Response Writer

## Purpose

Create a professional, evidence-backed response to reviewers.

Default output:

`working/response_plan.md`

## Workflow

1. Parse editor and reviewer comments into atomic requests.
2. Classify each request:
   - technical clarification;
   - additional experiment;
   - citation/literature;
   - presentation or writing;
   - figure/table;
   - scope or novelty concern.
3. Map each response to an actual manuscript change or a clear reason no change is needed.
4. Use evidence paths, figure/table numbers, and section references when available.
5. Draft polite responses with:
   - gratitude;
   - direct answer;
   - concrete revision;
   - evidence;
   - location in the revised manuscript.

## Output Format

```md
# IEEE journal Response Plan

## Summary of major revisions

## Point-by-point responses

Reviewer comment:

Response:

Revision made:

Evidence / manuscript location:
```

## Rules

- Do not promise experiments or analyses that were not done.
- Do not argue emotionally.
- Do not hide limitations; explain boundaries with evidence.
- Preserve a respectful, concise IEEE journal response tone.
