---
name: ieee-citation-verifier
description: Verify IEEE journal manuscript citations, BibTeX entries, citation-backed claims, and related-work anchors. Use when the user asks to check references, add citations, validate BibTeX, or avoid hallucinated citations.
argument-hint: "[manuscript .tex] [references.bib] [processed/current_intro_refs]"
---

# IEEE journal Citation Verifier

## Purpose

Prevent hallucinated or misused citations in IEEE journal manuscripts.

Default output:

`working/citation_audit.md`

## Inputs

Use any available:
- manuscript `.tex` files;
- `.bib` files;
- `processed/current_intro_refs/`;
- reference-paper Markdown notes;
- DOI/arXiv/IEEE metadata supplied by the user.

## Workflow

1. Extract all `\cite{...}` keys from the relevant manuscript section.
2. Check whether each key exists in the provided `.bib`.
3. Check whether the cited paper actually supports the sentence it is attached to.
4. If online verification is available and the user asks for it, verify metadata through reliable sources such as publisher pages, DOI/Crossref, Semantic Scholar, arXiv, or IEEE pages.
5. If online verification is not available, mark metadata status as `local-only` or `[VERIFY ONLINE]`.
6. Produce safe citation wording for each claim.

## Output Format

```md
# IEEE journal Citation Audit

| Cite key | Manuscript claim | Metadata status | Claim support | Risk | Action |
|---|---|---|---|---|---|

## Missing BibTeX keys
- ...

## Citation placeholders
- `\cite{PLACEHOLDER_author_year_verify}`: [reason]

## Claims needing citation
- ...
```

## Rules

- Never generate BibTeX from memory.
- Never invent titles, authors, years, DOIs, venues, or page numbers.
- Do not cite a paper for a limitation unless the paper actually shows that limitation or the limitation is fairly inferable from its scope.
- Use placeholders when verification is incomplete.
