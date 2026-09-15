# Writing profile index

No profiles are installed. `writing-skill` works without them: it falls back to the built-in
role examples in `skills/writing-skill/references/section-moves.md` and the IEEE defaults in
`knowledge/`.

## Creating profiles

`style-profiler <folder>` reads example papers (PDF, DOCX, TeX, Markdown, text) from any
folder you name and writes:

- `language_style.md`: register, section openers, gap and limitation shapes, contribution
  phrasing, transitions, hedging calibration, callout templates, comparison shapes,
  conclusion shapes.
- `argument_architecture.md`: paragraph functions and first-sentence positioning,
  claim-to-evidence order, citation grouping, the summary-to-judgment turn, figure roles,
  the gap-to-contribution-to-organization chain, taxonomy construction, method comparison,
  research-question mapping, the observation-to-mechanism results ladder, future-work
  derivation, and a per-role coverage table.
- `author_style.md` when the folder is profiled with `author`; set `author_style` in
  `active_profile.yml` to activate it. No author profile is needed for normal writing.

Per-paper argument skeletons are written to `processed/<corpus>/skeletons/` as regenerable
intermediates, not as style memory.

Profiles keep structure and phrasing patterns only. Domain facts, numbers, results,
citations, a paper's own category labels, and any sentence longer than eight words are
never recorded.

## Routing once profiles exist

Read only the relevant headings rather than both files in full for every paragraph.

| Task | Read these headings |
|---|---|
| Local grammar or compression | Relevant Register / Transitions / Hedging calibration in language_style.md only if needed |
| Literature category or comparison | Architecture A3-A5, B2; language Comparison shapes |
| Taxonomy or review synthesis | Architecture B1, B7 and A4/A5 |
| Introduction gap/contribution | Architecture A7, B3; language Gap and limitation shapes / Contribution phrasing |
| Results interpretation | Architecture A3, B5; language Hedging calibration / Comparison shapes |
| Future work | Architecture B6; language Conclusion shapes |
| Captions/callouts | Language Callout templates; architecture A6; consult built-in moves for sparse coverage |
| Choosing a less familiar role | Architecture Role coverage first, then the relevant heading |

A profile records what one corpus did, not what is universally correct. Current user
requirements and `knowledge/prose_quality.md` govern evidence, uncertainty and required
disclosure even where a profile uses imperative wording.
