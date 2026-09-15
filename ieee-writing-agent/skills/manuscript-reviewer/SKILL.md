---
name: manuscript-reviewer
description: Review manuscript paragraphs or sections for evidence, argument, terminology and prose problems. Use for critique of manuscript text, not toolkit or software audits.
---

# Manuscript reviewer

Optional invocation hints: `[text or file] [focus: claims|literature|prose|terms|all]`. Natural-language requests are sufficient.


Review the requested text and scope. Produce ranked actionable findings; rewrite only when the user requests editing, then use writing-skill for the affected text. Do not run a full reviewer workflow automatically after every ordinary edit.

## Read what the review needs

Use supplied text, relevant evidence/notes and adjacent text. Resolve manuscript paths from the conversation, project `manuscript_state.md` Bindings, then active profile. State is read-only for review; its absence does not block critique of pasted text. Read relevant prose-quality/IEEE rules and venue conventions only if a venue is selected. Profiles matter when style consistency is in scope.

## Assess

- Claim/evidence: attributed source, metric, baseline, condition, measured/simulated/analytical status; distinguish unsupported overclaims from defensive underclaiming. Assess severity by the consequence, not merely by a word hit. Never recommend hiding required limitations or negative findings.
- Literature: fair characterization, precise gap, actual source support. Existing foundational sources are not defective merely because they are old; recency matters for claims about the current field.
- Argument: paragraph purpose, sufficient support, synthesis and neighboring flow. A mechanism explanation is required only when supported and needed; do not invent causality to fill a template.
- Continuity: relevant terminology, first use, labels, duplication and section thesis. Use `scripts/term_check.py <affected-files> --registry <state> --discover` when terms are in scope; broader checks follow the requested audit.
- Prose: run `scripts/prose_gate.py <text>` when prose is in scope. BAN findings are local editorial problems; AUDIT/COUNT require context. Use `knowledge/prose_quality.md` for evidence-calibrated wording.
- Editorial rules: relevant units, symbols, references and caption/abstract rules, preserving valid LaTeX.

For suspicious attributions or new metadata problems use citation-verifier. Reuse valid existing checks; reread evidence when the reviewed assertion differs.

## Deliver

Lead with material findings and locations, then a concise assessment. Use a table for several issues: severity, location, problem, reason, proposed fix. Severity is blocking (invalidates a claim or required support), major (material argument problem), or minor (editing). State what was not verifiable. Do not invent issues to fill a report or label a paragraph submission-ready based only on regex checks.

A user request for read-only review creates no files. When saving an audit is requested, use the project working area. A requested fix already authorizes the identified edit; do not ask again solely for an `insert:` field.
