# IEEE Writing Agent Workspace

This workspace implements a portable IEEE journal writing agent setup for Codex and Claude Code.

Recommended source location:

```text
~/work/ieee-writing-agent
```

The source folder can live outside any manuscript project. The bootstrap script installs user-level links into `~/.claude` and `~/.codex`.

## What This Contains

- `AGENTS.md`: shared project rules for Codex-style agents.
- `CLAUDE.md`: Claude Code project rules that import `AGENTS.md`.
- `skills/`: shared reusable workflows.
- `.agents/skills/`: local Codex skill symlinks created by `scripts/bootstrap_wsl.sh`.
- `.claude/skills/`: local Claude Code skill symlinks created by `scripts/bootstrap_wsl.sh`.
- `.codex/agents/`: local Codex subagent directories.
- `.claude/agents/`: local Claude Code subagent Markdown files.
- `.claude/output-styles/ieee-writer.md`: Claude Code output style for manuscript writing.
- `corpora/`: full papers supplied by the user.
- `processed/`: generated section/paragraph Markdown.
- `profiles/`: reusable author and domain writing profiles.
- `working/`: temporary current-paper analysis.
- `templates/md-inputs/`: Markdown templates for clean article summaries, evidence packets, manuscript briefs, and reviewer comments.

## First Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/bootstrap_wsl.sh user
python scripts/profile_status.py
```

To bind the agent to a manuscript project, set these optional paths when bootstrapping:

```bash
IEEE_MANUSCRIPT_PATH=/path/to/main.tex \
IEEE_SUPPORT_PACKAGE=/path/to/support_package \
bash scripts/bootstrap_wsl.sh user
```

## Main Workflow

1. Put your own complete papers in `corpora/my_papers/`.
2. Run `paper-corpus-ingest` to generate `processed/my_papers/`.
3. Run `author-style-profiler` to create `profiles/author_style/current.md`.
4. Put broad target-journal papers in `corpora/domain_papers/journal_reference_set/`.
5. Run `paper-corpus-ingest` for the journal corpus.
6. Run `journal-style-profiler` to create `profiles/journal_style/current.md`.
7. Put highly related same-topic papers in `corpora/domain_papers/topic_reference_set/`.
8. Run `paper-corpus-ingest` for the topic corpus.
9. Run `topic-style-profiler` to create `profiles/topic_style/current.md`.
10. For current Introduction references, put full papers or clean Markdown in `corpora/current_intro_refs/` and run `intro-reference-miner`.
11. Plan the manuscript with `ieee-section-planner`.
12. Create or audit `working/claim_ledger.md` with `ieee-claim-ledger`.
13. Audit citations with `ieee-citation-verifier`.
14. Draft paragraphs with `ieee-paragraph-writer` or the `ieee-writing-agent`.
15. Integrate figures/tables with `ieee-figure-caption-writer`.
16. Review with `ieee-reviewer` or `ieee-technical-skeptic`.
17. Before submission, run `ieee-submission-auditor`.
18. For reviewer comments, use `ieee-response-writer`.
19. For length reduction, use `ieee-page-compressor`.

## Codex Usage

```text
Use $paper-corpus-ingest.
Use $author-style-profiler.
Use $journal-style-profiler.
Use $topic-style-profiler.
Use $domain-style-profiler.
Use $intro-reference-miner.
Use $ieee-section-planner.
Use $ieee-claim-ledger.
Use $ieee-citation-verifier.
Use $ieee-paragraph-writer.
Use $ieee-figure-caption-writer.
Use $ieee-reviewer.
Use $ieee-submission-auditor.
Use $ieee-response-writer.
Use $ieee-page-compressor.
```

Codex subagents are installed to `~/.codex/agents/` and kept in `.codex/agents/` inside this source bundle.

## Claude Code Usage

```text
/paper-corpus-ingest
/author-style-profiler
/journal-style-profiler
/topic-style-profiler
/domain-style-profiler
/intro-reference-miner
/ieee-section-planner
/ieee-claim-ledger
/ieee-citation-verifier
/ieee-paragraph-writer
/ieee-figure-caption-writer
/ieee-reviewer
/ieee-submission-auditor
/ieee-response-writer
/ieee-page-compressor
```

Claude Code subagents are installed to `~/.claude/agents/` and kept in `.claude/agents/` inside this source bundle. Select the `IEEE Writer` output style from Claude Code config when doing manuscript writing.

## Migration To Another Computer

Copy or clone this workspace to `~/work/ieee-writing-agent`, then run:

```bash
cd ~/work/ieee-writing-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/bootstrap_wsl.sh user
python scripts/profile_status.py
```

Raw corpora can be copied separately if they should not be stored in Git:

```bash
rsync -av /path/to/backup/corpora/ ./corpora/
```

Regenerate `processed/` after moving machines if raw papers were copied separately.

## Markdown Inputs

Markdown files are accepted and recommended when you have already cleaned or summarized papers.

Use these locations:

```text
corpora/my_papers/*.md
corpora/domain_papers/journal_reference_set/*.md
corpora/domain_papers/topic_reference_set/*.md
corpora/current_intro_refs/*.md
working/current_manuscript_brief.md
working/evidence_packet.md
working/reviewer_comments.md
```

Templates:

```text
templates/md-inputs/author-paper.md
templates/md-inputs/domain-paper.md
templates/md-inputs/current-intro-reference.md
templates/md-inputs/current-manuscript-brief.md
templates/md-inputs/evidence-packet.md
templates/md-inputs/reviewer-comments.md
```

Recommended corpus size:

- `corpora/my_papers`: 3-5 complete papers or clean Markdown versions.
- `corpora/domain_papers/journal_reference_set`: 10-15 broad papers from the target IEEE journal.
- `corpora/domain_papers/topic_reference_set`: 5-8 closely related same-topic papers, preferably from the same or adjacent IEEE journals.
- `corpora/current_intro_refs`: 8-12 references that will actually shape the Introduction.

Do not put current experimental results into author/domain style corpora. Put current facts in `working/current_manuscript_brief.md`, `working/evidence_packet.md`, or provide them directly in the conversation.

`corpora/current_intro_refs` may contain full papers. This does not make them style memory; the `intro-reference-miner` uses them for current citation roles, prior-art categories, and safe gap construction.
