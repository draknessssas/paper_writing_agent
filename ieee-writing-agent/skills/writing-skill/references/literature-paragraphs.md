# Literature writing and source analysis

Use this branch for reference-based paragraphs and authorized candidate-claim planning. Anchor reading to the requested claim or analysis question. Sources may supply attributed prior-work facts and results; never present them as the current study's own experiments.

## Evidence acquisition

Reuse existing processed text and notes after checking source identity, relevant passage and any changes. Convert new/unusable sources with `scripts/ingest_papers.py --input <folder> --output <project-working>/processed`. Inspect relevant extraction quality: PDF text extraction has no OCR and can disrupt columns; DOCX paragraph extraction omits tables. Read the original table/page when a claim depends on it.

Start with abstract/introduction/conclusion for orientation; inspect the exact method/result/discussion passage supporting an assertion. Read as much of the original as necessary to resolve context. Avoid loading unrelated full papers simply because a folder exists.

For several independent papers, delegate bounded source reading to `corpus-analyst` when available, authorized and useful. Paper count alone does not mandate delegation. Give a specific question and require source anchors. Analysts return notes; the parent maintains writing state to avoid concurrent edits.

## Reusable notes

Use `templates/reference-note.md`: source identity/path, relevant question, safe-to-cite findings and page/section/line, conditions, evidence type, limits and do-not-attribute claims. Distinguish an author's explicit statement from a reviewer's inference. Save notes only if file writes are authorized; otherwise return them in the response.

A prior note verifies a new sentence only if it covers the same claim, scope and source version. Check changed passages rather than rereading every paper. Missing references are a real evidence gap; use authorized search if available, or request sources and report the gap.

## Paragraph organization

Synthesize by a justified method family or comparison dimension. A useful sequence is category → shared mechanism → representative evidence → implication. Include a limitation or transition where it serves the argument, not automatically after every strength. Preserve fair coverage; repeated use of one source can be legitimate for distinct points.

For reviews, select relevant taxonomy/comparison/synthesis guidance through `profiles/index.md` and `section-moves.md`. Do not force all review roles into every section. Candidate taxonomies, gaps and research agendas remain author-review proposals unless already approved.

## Citation handling

Reuse real keys from the bound bibliography. Verify new/changed citations through `skills/citation-verifier/SKILL.md`: original support and source metadata are separate checks. If unresolved, a visible `\cite{PLACEHOLDER_<id>}` may remain only in an explicitly incomplete draft, with `[NEED: source/key]`. Do not invent first author/year merely to name the placeholder. Do not call such a paragraph ready for submission.

Use IEEE citation grammar ("in [1]", ranges [3]–[6]) and neutral attribution. Name authors when that helps the argument. Any numerical or limitation claim retains its original conditions and a traceable source passage.
