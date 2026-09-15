# IEEE Writing Agent

A manuscript-writing toolkit for **Codex** and **Claude Code**, with shared writing rules, optional style profiles, and local checking tools.

## Features

- **Write and revise** paragraphs, sections, abstracts, and captions.
- **Compress text** and keep terminology consistent.
- **Review manuscripts** for argument, evidence, structure, and language issues.
- **Verify citations** against source material, with scripts for BibTeX and optional DOI metadata checks.
- **Extract writing profiles** from your papers or selected examples.

The workflow requires evidence-based claims and keeps missing evidence visible. Authors remain responsible for scientific accuracy.

## Install

Install and configure Codex or Claude Code, and Python **3.11+**. Download or clone this repository, then open a terminal in its root directory.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Scope user
.\.venv\Scripts\python.exe -B scripts\check_parity.py --installed
```

### Linux / macOS / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash scripts/bootstrap.sh user
python -B scripts/check_parity.py --installed
```

Start a new client session after installation. Keep this repository in place: installed skills link to its files. To install only inside this repository, replace `user` with `local` and omit `--installed` from the check.

**Codex compatibility:** the bundled role adapters use nested `config.toml` files. Clients requiring standalone agent TOML files need an adapter update; use the skill commands below for the main workflow.

## Extract Writing Profiles

No papers or generated profiles are included. You can start writing with the built-in rules, or supply example papers to learn their language and argument structure.

Place papers in `corpora/exemplars/`, or use any folder you choose. Send this request in your client:

**Codex**

```text
$style-profiler corpora/exemplars/ exemplars both
```

**Claude Code**

```text
/style-profiler corpora/exemplars/ exemplars both
```

This can generate:

- `profiles/language_style.md` — language and phrasing patterns.
- `profiles/argument_architecture.md` — paragraph and argument structure.

To extract your own author style, use `corpora/my_papers/ author` instead. Set `author_style` in `profiles/active_profile.yml` to the generated author profile to activate it.

Supported inputs include PDF, DOCX, TeX, Markdown, and text. Scanned PDFs need OCR first. Profiles capture writing patterns, not research facts or results.

## Use

Open your client in the toolkit directory and provide your manuscript or text, relevant evidence, and the task you want completed. Allow access to external manuscript folders when your client requests it.

| Task | Codex | Claude Code |
| --- | --- | --- |
| Write, revise, or compress | `$writing-skill` | `/writing-skill` |
| Review a manuscript | `$manuscript-reviewer` | `/manuscript-reviewer` |
| Verify citations | `$citation-verifier` | `/citation-verifier` |
| Extract writing profiles | `$style-profiler` | `/style-profiler` |

Example requests for Codex; replace `$` with `/` in Claude Code:

```text
$writing-skill Revise the paragraph below for clarity. Keep all numbers,
conditions, and citations unchanged.

<paste your paragraph>
```

```text
$writing-skill Draft Section II-A using the supplied outline and evidence.
Save a separate draft and mark missing evidence as [NEED: ...].
```

```text
$manuscript-reviewer Review manuscript/main.tex for argument and evidence
problems. Report findings without changing files.
```

```text
$citation-verifier Check main.tex and references.bib against the papers
in refs/. Report metadata errors and unsupported claims separately.
```

