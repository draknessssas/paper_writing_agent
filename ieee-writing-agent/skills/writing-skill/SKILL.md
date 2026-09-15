---
name: writing-skill
description: Draft, revise, or compress evidence-based manuscript text, including abstracts and captions. Use for manuscript writing, terminology edits, or requested claim planning.
---

# Writing skill

Optional invocation hints: `[text or file] [claim/evidence when needed] [write|revise|compress|caption|abstract|terms|plan] [clean|annotated|confirm-first]`. Natural-language requests are sufficient.


Use one paragraph as the drafting and checking unit. Complete all units in the user's authorized scope; a section request is not itself a reason to refuse. Respect explicit checkpoints and read-only requests. This skill does not apply to explaining or maintaining the toolkit.

## Establish the task from available context

Read the relevant conversation, supplied text and existing state before deciding information is missing. A structured brief is optional. For a new paragraph, establish its claim, purpose, position and evidence/reference pointers. For a meaning-preserving edit, use the existing claim without requiring the literal `claim: unchanged`. Read [input decisions](references/intake-and-refusal.md) only for missing/conflicting inputs, candidate claims, multiple paragraphs, or brief field details.

Do not manufacture scientific conclusions to fill a missing brief. If claim planning is requested, propose evidence-backed candidates; if the user asks for approval first, stop before drafting. If the user explicitly requests proposed claims followed by a draft, continue sequentially and retain candidate provenance. Unknown essential evidence blocks the affected assertion, not unrelated authorized analysis.

## Load context proportionately

Resolve this toolkit from the real skill path. Resolve manuscript/refs/bib from the request, conversation, `manuscript_state.md` Bindings, then `profiles/active_profile.yml`. For project writing, find the state before creating it; read [continuity](references/continuity-and-terminology.md) for discovery, registration or cross-paragraph changes. Pasted-text edits do not require a state file.

Read the current section thesis, adjacent text, relevant terms and evidence. Consult `profiles/index.md` when a profile is useful, then just the applicable sections. Reuse unchanged context. Read the entire manuscript only when the scope or unresolved continuity requires it.

## Choose the needed branch

| Task | Guidance |
|---|---|
| `write`, `revise` | Use the claim and relevant evidence; [section moves](references/section-moves.md) only when structural guidance helps |
| `compress` | [Compression](references/compression.md): preserve meanings, numbers, conditions and citations |
| `caption`, `abstract` | Relevant roles in section moves and applicable IEEE/venue conventions; no invented figure features or results |
| Literature writing or reference analysis | [Literature](references/literature-paragraphs.md): source passages and reusable notes |
| `plan` | Input decisions: candidates plus evidence; no manuscript prose unless authorized |
| `terms` | Continuity reference: discover, apply authorized choices, verify changed files |

The six original writing/editing modes remain supported; `plan` makes requested claim planning explicit. Natural-language requests select these branches without special syntax.

## Compose and check

For each substantive technical assertion, identify its evidence and allowed scope. Use a compact claim table when planning, comparing uncertain claims, or producing annotated output; do not require a table for a grammatical edit. Preserve the distinction between this study's findings, cited findings, and interpretation. Use `[NEED: ...]` for unresolved material facts. An unverified original number already in pasted text may be preserved in an editing task, but is not thereby verified.

Draft with a clear paragraph purpose. Topic-first is useful, not a universal sentence-order rule. Preserve technical meaning and valid LaTeX, numbers, citations, labels, variables and units unless their correction is explicitly in scope. Read `knowledge/prose_quality.md` for claim calibration; profiles are descriptive preferences and cannot override evidence or required disclosure.

Run `scripts/prose_gate.py` on changed prose (stdin is available for a pasted-text task). Resolve BAN findings; assess AUDIT findings in context. Sentence length is a readability signal, not a forced rewrite threshold. Use `scripts/term_check.py --registry <state>` when technical terms are affected; check the whole manuscript only for global edits, uncertain definition/numbering, section integration or an explicit audit. See [validation and completion](references/validation-and-completion.md) for exact commands and limits.

Verify new or changed citations with `skills/citation-verifier/SKILL.md`, reusing unchanged source/metadata checks where appropriate. Fix relevant findings and rerun only affected checks. Tool failure is reported as incomplete verification, not hidden as success.

## Deliver and finish

Default: requested text plus concise material changes, uncertainties and verification limits. `annotated` adds the brief, claim/evidence table, mapping and terminology actions. `clean` minimizes commentary but still exposes unresolved `[NEED: ...]` and citations. `confirm-first` is an explicit pause after the proposed topic/claim.

For project writing, update the existing manuscript state after each completed unit, recording claim provenance (`author-supplied`, `existing-text`, `candidate`, or `author-approved`), output location and open issues. Update an existing paragraph entry on revision rather than duplicating it. Save authorized drafts/notes/reports under project-local working directories; natural-language editing requests authorize changes to the identified text. A response-only or read-only task does not authorize file writes.

Complete all authorized paragraphs and their integration check. Report `draft complete` only with material unresolved issues stated; use `ready for author review` when relevant checks pass. Do not call a draft submission-ready while evidence or citation blockers remain.
