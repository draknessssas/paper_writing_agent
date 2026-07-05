---
name: ieee-reviewer
description: Review target IEEE journal manuscript paragraphs or sections for journal fit, technical claim discipline, evidence support, author-style consistency, journal/topic-style consistency, and reviewer risk.
argument-hint: "[paragraph file or pasted text]"
---

# IEEE journal Reviewer

## Purpose

Review manuscript text before submission to the target IEEE journal.

## Review Dimensions

1. IEEE journal fit
   - Is the target-field contribution explicit?
   - Is there target-field method, system, design, modeling, implementation, experiment, or validation content?
   - Is the paper more than generic theory, generic algorithm design, or component characterization?

2. Style consistency
   - Does it match `profiles/author_style/current.md`?
   - Does it match `profiles/journal_style/current.md` and `profiles/topic_style/current.md`?
   - Is the tone IEEE Transactions-like?

3. Literature positioning
   - Are prior-art categories fair?
   - Are limitations citation-backed?
   - Is the gap precise?

4. Evidence discipline
   - Are quantitative claims supported?
   - Are baselines and conditions stated?
   - Are hardware validation claims justified?

5. Paragraph logic
   - one role per paragraph;
   - clear topic sentence;
   - no abrupt transition;
   - final sentence points to the next idea.

6. Topic-specific manuscript risks
   - Avoid generic framing that hides the target-field contribution.
   - Check terminology from `working/current_manuscript_brief.md` and the current manuscript.
   - Check whether comparison baselines and protocols are complete enough for each claim.

## Output

Use:

| Severity | Issue | Why it matters | Suggested fix |
|---|---|---|---|

Then provide a revised paragraph only when requested.

## Rules

- Do not invent citations or results.
- Use `[NEED: ...]` for missing support.
- Flag overclaiming aggressively.
