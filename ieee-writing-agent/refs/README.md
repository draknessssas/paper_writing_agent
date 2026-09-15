# refs/: references for one paragraph or one survey topic

Put the papers that one paragraph (or one survey section) will cite into a subfolder, then name that subfolder in the paragraph brief:

```text
refs/intro-loss-models/     <- PDFs, DOCX, TeX, Markdown, or text
refs/related-control/
```

The writing skill converts a folder with `scripts/ingest_papers.py` into `processed/refs/<name>/`, reads abstract, introduction, and conclusion first, and writes one note per paper into `working/ref_notes/<brief-id>/` (template: `templates/reference-note.md`).

These files are citation sources for the current manuscript. They are never style memory and never evidence for the manuscript's own results. Large PDFs can be kept out of Git; see `.gitignore`.
