# Validation and completion

## Scope the checks

| Change | Checks |
|---|---|
| Grammar/shortening of supplied text | Meaning and protected numbers/conditions/citations; prose gate on changed text |
| New technical paragraph | Claim-source support, local prose/terms, adjacent transition; affected labels/first uses |
| New/changed citation | Source passage and relevant metadata/key checks; unchanged records can be reused |
| Global terminology or symbols | Relevant manuscript files, registry and definition/usage context |
| Section completion | Paragraph claims/repetition, taxonomy/argument flow, terms, numbering, citations |
| Requested final/submission audit | Whole manuscript and bibliography; identify what was checked online/local-only |

Do not interpret a successful process exit as proof of scientific correctness. Do not repeat checks on unchanged inputs. Rerun affected checks after edits; broaden only for a newly identified concern.

## Commands and meaning

Use the toolkit's environment and absolute script paths when the current directory is a different manuscript project. Files should be plain manuscript text (.md/.tex/.txt), not a raw DOCX/PDF.

```bash
python scripts/prose_gate.py <changed-text> --json
python scripts/term_check.py <changed-text> --registry <state> --discover --json
python scripts/check_bib.py --bib <bibliography> --tex <affected-text> --json
```

`prose_gate.py`: BAN is a local editorial rule (exit 1 by default); AUDIT is contextual; COUNT is a statistic. `novel` is AUDIT: check novelty evidence and author intent, not just synonyms. Over-40-word sentences are reported, not automatically failed. An actual editorial constraint may be stricter. Preserve mandatory qualifiers while resolving findings.

`term_check.py`: default reporting remains backward-compatible. `--fail-on-findings` returns 1 for explicit registered variants remaining after the requested operation; discovery/hyphen candidates still need context. `--fix` previews; `--fix --write` applies an authorized replacement and preserves a backup. `--write` alone is an error. The checker is heuristic and does not separate abstract/body abbreviation definitions.

`check_bib.py`: missing keys, unresolved citation placeholders, metadata errors, and confirmed online metadata mismatches return 1. Network-unresolved checks are reported separately and are not evidence of a fabricated paper; `--require-online` makes unresolved online verification block a requested final audit. Metadata matching does not verify claim-source alignment.

## Completion states

- `analysis complete`: requested analysis/candidates delivered; no implication that writing was authorized.
- `draft complete; issues open`: all draft units delivered with explicit evidence/citation gaps.
- `ready for author review`: authorized text and relevant checks completed, with remaining editorial decisions identified.
- `verification incomplete`: required evidence/tool access unavailable; say which checks ran and which did not.

Save requested artifacts, update relevant project state, and provide output locations. For a reply-only task, return text without creating project files. Report only material findings by default; retain a detailed audit when requested or needed to make a substantive claim change traceable.
