# Manuscript state and continuity

## Find before create

For project writing, use an explicit `state:` first. Otherwise search next to the manuscript, then one and two parent directories up. Check that Bindings refer to this manuscript/project before adopting a parent state. A toolkit `working/manuscript_state.md` is a fallback only when its binding matches; do not silently move it. If a state needs relocating, preserve it and use the user's authorized location.

Create one state beside the manuscript only when none belongs to the project and project writing is authorized. Pasted-text editing or read-only analysis needs no new state. A user can explicitly choose another state path. Scripts receive `--registry <state>` for nonstandard layouts.

Read relevant Bindings, argument/section theses, terms and paragraph entries. The manuscript wins over a stale summary; update the state during authorized writing, and ask only about unresolved scientific contradictions. Do not reread an unchanged history log on every small edit.

## State file template

Create it when it does not exist, seeded from `working/manuscript_brief.md` if present.

```markdown
# Manuscript State

## Bindings
- Manuscript file:
- Bib file:
- Reference root:
- Evidence packet:

## Argument spine
- Working title:
- One-sentence argument:
- Target venue (optional):

## Decisions
- (manuscript-wide choices: "this article" vs "this paper", symbol and subscript style, tense conventions, acronym policy, citation style; one line each, dated)

## Section theses
| Section | Thesis (what the section must establish) | Status |
|---|---|---|

## Terminology registry
| Canonical | Variants | Symbol | Acronym | First use | Notes |
|---|---|---|---|---|---|

## Paragraph log
| Id | Section | Role | Claim | New terms / symbols / acronyms | Figures, equations, citations | Open flags | Date |
|---|---|---|---|---|---|---|---|

## References used per point
| Point | Cite keys |
|---|---|

## History
- (one line per action, newest last: date, action such as wrote / revised / compressed / terms sweep / state moved, paragraph id or scope)

## Open issues
-
```

Registry conventions: `Variants` are separated by `;`. `Acronym` holds the acronym and, in Notes or Canonical, its expansion. `First use` is the paragraph id where the term or acronym is first defined. The script `scripts/term_check.py` parses this table; keep the header names.


## Bindings and provenance

Paths follow the request/conversation, existing Bindings, then active profile. User-relative paths resolve from the user's project; toolkit-relative paths resolve from the real toolkit root. Save working notes/drafts/reports under the manuscript project's working directory unless another location was requested.

For each paragraph, record its claim source: `author-supplied`, `existing-text`, `candidate`, or `author-approved`. Record drafting authority separately from author approval. Include output path, checks completed, unresolved issues and date. Revise an existing entry for the same id instead of adding duplicate paragraph rows. Log material changes, not every read or checker invocation.

## Continuity checks

- Terms: use author-selected forms, then established manuscript forms, then relevant conventions. Check changed text against the registry. Search the full manuscript when changing a canonical term or resolving inconsistent usage.
- Acronyms/symbols: verify first use in the applicable body/abstract context. Registry entries help locate first use but do not prove every occurrence is correct. Respect an abstract's independent readability and actual venue rules.
- Labels: verify new/changed callouts against the manuscript or supplied figure/equation information.
- Repetition: check the paragraph log and adjacent text; an intentional recap is allowed.
- Flow: connect to the section's purpose and neighboring ideas; no mandatory forward-pointing last sentence.
- Drift: remove irrelevant additions while preserving the requested argument.
- Argument: reconcile a new claim with the section thesis; do not silently replace the author's scientific position.
- Disclosure: retain measured/simulated status, conditions, uncertainty and matched-comparison limits where needed.

## Authorized terminology edits

Natural language such as “统一全文使用 digital twin” authorizes that named unification; `unify: yes` is optional. When a global choice is not settled, report alternatives before changing unrelated text. Do not ask again for a choice already made.

```bash
python scripts/term_check.py <files> --registry <state> --discover
python scripts/term_check.py <files> --registry <state> --fix
python scripts/term_check.py <files> --registry <state> --fix --write
```

The preview is optional when the requested replacement is already explicit. Applying fixes keeps a backup. Recheck affected files after changes. Discovery is heuristic: hyphenated modifiers and different physical symbols may be valid; do not automatically unify them. Do not alter citation keys, math, labels or image paths as prose substitutions.
