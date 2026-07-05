---
name: paper-corpus-ingest
description: Ingest complete academic papers from corpora folders, convert PDF/DOCX/TEX/MD/TXT into structured section-and-paragraph Markdown files, and prepare them for style or reference analysis. Use when the user adds full papers, wants automatic paragraph detection, or asks to refresh processed corpora.
argument-hint: "[input-corpus-dir] [output-processed-dir]"
---

# Paper Corpus Ingest

## Purpose

Automatically process complete academic papers. The user should not need to manually crop paragraphs.

## Inputs

Common input folders:
- `corpora/my_papers/`
- `corpora/domain_papers/journal_reference_set/`
- `corpora/domain_papers/topic_reference_set/`
- `corpora/current_intro_refs/`

Common output folders:
- `processed/my_papers/`
- `processed/domain_papers/journal_reference_set/`
- `processed/domain_papers/topic_reference_set/`
- `processed/current_intro_refs/`

## Procedure

1. Identify the requested input corpus and output folder.
2. Run:

```bash
python scripts/ingest_papers.py --input <input-folder> --output <output-folder>
```

3. Inspect several generated Markdown files in `processed/`.
4. Check whether section headings and paragraph breaks are reasonable.
5. If PDF extraction has obvious two-column ordering issues, report it and proceed with caution.
6. Do not summarize the whole corpus in the main response unless requested.
7. Report:
   - number of papers processed;
   - output folder;
   - extraction risks;
   - recommended next skill.

## Important Rules

- The output is for style/process/reference analysis only.
- Do not treat processed papers as facts for the current manuscript unless they are in `corpora/current_intro_refs/` or explicitly provided as current references.
- Do not copy sentences from processed papers.
