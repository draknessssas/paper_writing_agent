---
name: ieee-paragraph-writer
description: Draft or revise one target IEEE journal manuscript paragraph using the user's current facts, author style profile, journal style profile, topic style profile, and optional introduction reference map. Use for abstract, introduction, method, experiment, results, conclusion, and reviewer response paragraphs.
argument-hint: "[section] [paragraph role] [clean|annotated|alternatives|review]"
---

# IEEE Paragraph Writer

## Purpose

Write or revise exactly one manuscript paragraph for the target IEEE journal.

## Inputs

Use, in priority order:

1. User's current prompt.
2. Experimental data, results, figure/table/equation references, and file paths provided in the current conversation.
3. Current draft paragraph.
4. Previous and next paragraphs, if provided.
5. `working/intro_reference_map.md`, if relevant.
6. `profiles/author_style/current.md`, if available.
7. `profiles/journal_style/current.md`, if available.
8. `profiles/topic_style/current.md`, if available.
9. `profiles/domain_style/current.md`, if available as a legacy combined profile.
10. Target IEEE journal writing rules.

## Key Behavior

Before writing, determine:

- target section;
- paragraph role;
- evidence available;
- claim strength allowed;
- style source;
- missing information.

## Style Blending

Use:
- `profiles/author_style/current.md` for the user's voice;
- `profiles/journal_style/current.md` for broad target-journal flow;
- `profiles/topic_style/current.md` for same-topic architecture and validation flow;
- `profiles/domain_style/current.md` only as a legacy combined fallback;
- current references only for literature positioning;
- current user-provided data only for technical claims.

If profiles are missing, proceed but say which profile is missing.

## Section Patterns

### Abstract

Problem -> method -> key mechanism -> validation -> most important result -> implication.

No citations, no equations, no unsupported quantitative claims.

### Introduction

Context -> technical bottleneck -> prior-art categories -> limitations -> gap -> proposed approach -> contributions.

Use `working/intro_reference_map.md` when available.

### Method / Modeling / Control

Objective -> model/assumption -> proposed mechanism -> equation/figure link -> design implication.

For topic-specific constraints, use `working/current_manuscript_brief.md`, `working/evidence_packet.md`, or `profiles/topic_style/current.md`.

### Experimental Setup

Prototype or dataset -> operating condition -> measurement/evaluation setup -> baseline -> purpose of the test.

### Results

Condition -> measured or evaluated result -> comparison -> physical interpretation -> supported claim.

Use the validation ladder extracted in `profiles/topic_style/current.md` when available.

### Conclusion

What was proposed -> what was demonstrated -> key evidence -> limitation or implication.

## Output Modes

### clean

Output only the final paragraph.

### annotated

Output:
1. Paragraph
2. Why it works
3. Missing evidence / risk flags
4. Optional tighter version

### alternatives

Output 2-3 versions:
- author-style dominant;
- target-journal-style dominant;
- conservative reviewer-safe.

### review

Do not rewrite first. Diagnose issues.

## Rules

- Do not invent data, references, or hardware conditions.
- Do not copy sentences from style or reference corpora.
- Preserve LaTeX commands, citations, labels, variables, units, equations, and figure/table references.
- Use `[NEED: ...]` for missing evidence.
- Avoid vague praise and unsupported novelty.
- Keep topic-specific framing tied to current evidence, not to generic method claims.
