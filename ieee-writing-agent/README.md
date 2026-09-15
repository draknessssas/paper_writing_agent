# IEEE manuscript writing toolkit

Version: 2026.09.14. Shared evidence-based writing workflows for Codex and Claude Code; adapted for GPT-6 Astra's instruction following while preserving model-neutral scientific rules.

The user defines the task scope. The writer drafts and checks paragraphs sequentially, including a complete section when authorized. Existing text and prior decisions count as input; a special brief form is optional. Requested claim planning produces evidence-backed candidates. Unknown results/references are never invented.

## Skills and roles

- `writing-skill`: writing, revision, compression, captions, abstracts, terminology, claim planning.
- `manuscript-reviewer`: critique of manuscript text.
- `citation-verifier`: citation metadata and claim-source alignment.
- `style-profiler`: requested extraction/refresh of writing profiles.
- `writer` (Codex) / `writing-agent` (Claude): assigned writing work.
- `corpus-analyst`: read-only source analysis; coordinator owns state/profile writes.

Rules live in AGENTS.md, skills and knowledge. Client adapters reference shared `knowledge/roles/` contracts. `profiles/index.md` routes to relevant sections of whichever profiles exist. No profiles ship with this package; `style-profiler` creates them from papers you supply, and the toolkit works without them.

## Install/update

Python 3.11+ and the dependencies in requirements.txt are needed for the full toolkit. Basic prose/term/bib checks use the standard library; PDF/DOCX and YAML helpers use the listed libraries. No local model training/GPU deployment is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash scripts/bootstrap.sh user
python -B scripts/check_parity.py --installed
python -B scripts/profile_status.py
```

`local` registers only project links for testing. `user` registers both clients and modern Codex `~/.agents/skills` plus legacy aliases. Bootstrap preserves custom YAML fields and backs up changed configuration; explicit empty IEEE_* variables clear bindings. It does not select models or log into accounts. Restart existing client sessions to load changed descriptions/adapters.

Windows: create `.venv` with Python, install requirements and run `powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Scope user`. The script uses the same YAML updater and backs up ordinary destination files/directories before replacing them. Native Windows execution should be verified on Windows; directory junctions and copied-file fallbacks differ from POSIX links.

## Use

In Codex use `$writing-skill`; in Claude use `/writing-skill`. Supply the manuscript/text, intended judgment and relevant evidence, or ask for candidate claims first. Examples and migration behavior are in [the Chinese tutorial](TUTORIAL.zh-CN.md).

Natural-language “edit this paragraph” authorizes that edit. “Analyze only, do not change files” stays read-only. A request to propose claims and wait stops before prose; a request to draft from proposed claims retains candidate provenance. Scope/permissions are not expanded by a profile or output style.

## Checks

```bash
python -B scripts/check_parity.py                  # static source/adapters
python -B scripts/check_parity.py --installed      # also installed entrypoints
python -B -m unittest discover -s tests -v         # isolated tool regression tests
python -B scripts/prose_gate.py draft.tex --json
python -B scripts/term_check.py draft.tex --registry manuscript_state.md --discover
python -B scripts/check_bib.py --bib references.bib --tex draft.tex
```

BAN is an editorial finding; AUDIT/COUNT require context. `novel` is AUDIT, sentence length is a signal. Bibliography placeholders/missing keys/confirmed online mismatches fail the bib check; unresolved networking is not proof of fabrication. `--require-online` requests strict online completeness. `--fail-on-findings` opts into failing on remaining registered term variants.

Static checks and tests do not prove model behavior or scientific correctness. Report real verification scope and unresolved issues; do not call provisional drafts submission-ready.
