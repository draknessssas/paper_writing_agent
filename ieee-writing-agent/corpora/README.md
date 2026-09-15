# corpora/: style corpora (language only)

Two folders, both optional:

```text
corpora/exemplars/    well-written papers from the venues you target; any subfield
corpora/my_papers/    your own complete papers
```

Run `/style-profiler` (Codex: `Use $style-profiler.`) after adding papers. It converts them into `processed/` and writes `profiles/language_style.md` and `profiles/author_style.md`.

What the profiles keep: the language layer (sentence architecture, paragraph rhythm, section openers as slot templates, transition and hedging habits, callout templates) and the argument-architecture layer (paragraph functions, first-sentence positioning, claim-to-evidence order, citation grouping, summary-to-judgment turns, figure roles, gap-to-contribution chain, taxonomy and comparison conventions, RQ-to-experiment mapping, results ladder, future-work derivation). What they never keep: domain facts, numbers, results, citations, a paper's category labels, or any sentence longer than eight words.

Papers can also stay where they are: `/style-profiler /path/to/folder` reads any folder.

Recommended sizes: 8 to 15 exemplars; 3 to 5 own papers. PDF, DOCX, TeX, Markdown, and text are accepted.

References for a specific paragraph do not belong here; put them in `refs/<name>/`.
