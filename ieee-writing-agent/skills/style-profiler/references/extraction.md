# Style Profiler

## Purpose

Produce calibration profiles for `writing-skill` from papers the user points at. Two layers, both descriptive ("this is how the field does it"), never knowledge:

- Language layer: how sentences and paragraphs are built. Output `profiles/language_style.md` from the field's papers, or `profiles/author_style.md` from the user's own papers.
- Argument-architecture layer: the implicit structure of the writing. Paragraph mechanics: what each paragraph is for, how its first sentence positions it, what follows a claim, when one paper is cited and when several, how the author turns from summarizing the literature to judging it, what figures and tables do in the argument, how the Introduction chains gap, contributions, and organization. Article level: how large reviews build a taxonomy, how small reviews compare methods, how the gap is constructed, how research questions map to experiments, how results move from observation to mechanism, how future work is derived from what came before. Output `profiles/argument_architecture.md` from the field's papers; for the user's own papers the same findings go into an "Argument habits" section of `profiles/author_style.md`.

Both layers are optional. Without profiles the writing skill uses IEEE defaults and its own section patterns.

## Inputs

- The folder the user names in the request, used exactly as given (absolute, or relative to the user's current directory). When no folder is named, use `corpora/exemplars/` and `corpora/my_papers/`. Accepted files: pdf, docx, tex, md, txt.
- Which profile the folder feeds: `exemplars` (default) or `author`.
- Which layers: `language`, `architecture`, or `both` (default).
- Corpus composition: taxonomy and comparison patterns are learned only from review papers; research-question and results-ladder patterns only from research articles. A mixed folder is fine, every paper is typed first and the profile reports patterns per type. Recommended: 8 to 15 field papers, at least 3 of them reviews when the user is writing a review; 3 to 5 own papers.
- Converted text goes to `processed/<folder name>/`; one argument skeleton per paper goes to `processed/<folder name>/skeletons/<paper>.md` (traceable intermediate; reusable when the source is unchanged, not copied into manuscript prose).

## Procedure

1. Reuse usable unchanged processed text; otherwise ingest: `python scripts/ingest_papers.py --input <folder> --output processed/<folder name>` (for example `--input /home/me/reviews --output processed/reviews`). Open two processed files and check that headings and paragraph breaks are usable; note extraction damage (two-column order, dropped tables, image-only pages with no text).
2. Type each paper from its headings and first page: large review (taxonomy-driven, many category sections), small comparative review (a few methods compared on stated dimensions), research article, tutorial. Note whether it has a taxonomy figure or table, comparison tables, explicit research questions or hypotheses, a future-work section, and its approximate paragraph count.
3. Language layer, per paper, read only: abstract; the first two Introduction paragraphs and the contribution paragraph; one method paragraph; one results paragraph; the conclusion.
4. Architecture layer, per paper, read: the whole Introduction; every section heading; the first sentence of every paragraph in the Introduction, in one method or technical section, in one results or validation section, in the taxonomy or comparison section (reviews), and in the conclusion and future work; the headers (never the values) of comparison tables; the list of figure captions; explicit research-question statements; every future-work item. Fill the skeleton template below and save it under `processed/<folder name>/skeletons/`.
5. When authorized independent paper reading would benefit from delegation, use `corpus-analyst` with the relevant extraction question and skeleton template; synthesize the results in the coordinator. Paper count alone does not require delegation. The analyst returns notes; the coordinator saves artifacts.
6. Synthesize per item: the majority pattern, the spread, and the paper type it applies to. Do not let one paper dominate; when reviews and research articles differ, say so for each item.
7. Fill the role-coverage table below. A role is `calibrated` when at least three papers show that paragraph function, `thin` when one or two do, and `not observed` when none does; `not observed` roles keep the built-in patterns of `skills/writing-skill/references/section-moves.md`, which is never overridden by an empty finding. Some roles are never learnable from published papers (`response-to-reviewer`) or only weakly (`caption`, when the extractor drops caption text): mark those `not learnable here`.
8. Write the profile files in the formats below; record corpus size, paper types, and date. Report: file paths, papers by type, extraction risks, the role-coverage summary (how many roles calibrated, thin, not observed), and the five findings most likely to change what `writing-skill` produces.

## Language layer: what to extract

- Register: person ("this article" vs "we"), tense and voice habits per section, formality, typical sentence length (estimate mean and spread), paragraph length in sentences.
- Section openers: the shape of the first sentence of each section as a slot template, for example "[Application] requires [property] at [condition]".
- Gap sentence shapes and how the limitation of prior work is introduced (which verbs, how proportionate).
- Contribution-list phrasing: numbered or prose, result-worded or task-worded, how many items.
- Transition inventory: which connectives appear, how often, and where paragraphs link by content rather than by connectives.
- Hedging calibration: which hedges appear with which kind of evidence; where claims are stated flatly.
- Callout templates: how figures, tables, and equations are introduced and interpreted, as slot templates.
- Comparison sentence shapes: how numbers are set against baselines, how conditions are attached.
- Limitation phrasing and where limitations sit.
- Conclusion shapes.
- Recurrent connective phrases up to eight words that are generic to the genre (for example "under the same operating conditions"); never distinctive sentences.
- Author profile only: idiosyncrasies worth keeping; weaknesses to correct (with the rule from `knowledge/prose_quality.md` that applies); things the user should stop doing.

## Architecture layer: what to extract

### A. Paragraph mechanics (every paper type)

- A1 Paragraph function inventory. Per section, the sequence of paragraph functions (for example Introduction: context, category, category, limitation, gap, contribution, organization). How many paragraphs each function takes; whether one paragraph ever carries two functions; where the sequence differs between reviews and research articles.
- A2 First-sentence positioning. For each function, how the first sentence tells the reader what the paragraph is for: a claim, a category label, a contrast with the previous paragraph, a question, a condition. Slot templates per function. Whether the first sentence is the claim or the claim arrives later, and how the last sentence hands over to the next paragraph.
- A3 Claim to evidence. What sits immediately after a claim: a number with its condition, a figure or table callout, a citation cluster, a mechanism sentence, an equation, a worked example. The typical order and distance (same sentence, next sentence, next paragraph). Which claim types get which kind of evidence.
- A4 Citation grouping. When a single paper is cited (a specific number, a specific method, a named author, a direct contrast) and when several are grouped ([3]–[7]: category membership, an established fact, a trend). Typical cluster size. Whether authors are named in prose. How one representative paper is singled out from a cluster and what is said about it.
- A5 Summary-to-judgment turn. The move by which the author stops reporting the literature and starts evaluating it: the marker constructions ("these approaches share", "in practice", "a closer look at", "however, none"), where in the paragraph or section the turn happens, how the judgment is backed (citation, number, argument), and how strong the judgment language is.
- A6 Figures and tables in the argument. For each figure or table type, which claim it carries: taxonomy overview, comparison, mechanism illustration, evidence for a result, summary of the field. Whether the text states the claim before or after the callout; whether the text interprets or merely points; whether a table replaces prose or is walked through; where the taxonomy figure sits.
- A7 Introduction closing chain. How the last paragraphs chain gap, contributions, and organization: number of paragraphs, whether the gap is one sentence or accumulated, contribution-list form (numbered, prose, result-worded, task-worded, count), whether an organization paragraph exists and how it maps contributions to sections, and how the chain refers back to the categories set up earlier.

### B. Article-level architecture

- B1 Taxonomy construction (large reviews). Number and kind of axes (by mechanism, by application, by data type, and so on, recorded as kinds, not as a specific paper's labels); how the top-level split is justified; whether categories are exclusive or form a matrix; hierarchy depth; how the taxonomy is announced; where the taxonomy figure or table appears relative to the announcement; how each category section opens and closes; how cross-cutting themes that do not fit the axes are handled; how the taxonomy is reused in the comparison and future-work sections.
- B2 Method comparison (small reviews and comparative sections). The comparison dimensions used, as dimension kinds; how the comparison table is introduced and interpreted; whether the text states trade-offs or declares winners; how differing test conditions are handled; whether a qualitative rating rubric is used; how the comparison feeds a recommendation.
- B3 Gap construction across the Introduction. How many prior-work categories precede the gap; whether each category ends with its own limitation or the limitations are collected once; whether the gap accumulates over paragraphs or is stated in one sentence; how the gap maps to the contribution list (one-to-one, many-to-one); the strength of the gap language.
- B4 Research questions to experiments. Whether research questions or hypotheses are explicit; where they are stated; how each is answered (a section, an experiment, a figure) and how the cross-reference is written; whether the results section restates the question before answering it; how questions left open are handled.
- B5 Results ladder. How results move from observation to mechanism to implication: sentences per rung; which verbs mark an observation ("increases", "is measured") and which mark a mechanism claim ("because", "arises from", "is attributed to"); where the physical or causal interpretation appears; how counter-evidence or anomalies are handled; how the ladder ends (a bounded claim, a design implication).
- B6 Future work derivation. Whether each future-work item traces to a stated limitation, an unexplored cell of the taxonomy, or an open question raised earlier; the derivation pattern ("X was validated only under Y; extending to Z requires ..."); placement (own section, end of discussion, conclusion); length; how it avoids becoming a wish list.
- B7 Section endings and synthesis (reviews). Whether category sections end with a synthesis paragraph; what it does (cross-paper comparison, open problem, bridge to the next category); how the final synthesis section relates the categories to each other and to the research agenda.

## Skeleton template (one per paper)

```markdown
# Skeleton: <paper key>
- Type: large review | small comparative review | research article | tutorial
- Venue, year, approximate paragraph count
- Has: taxonomy figure/table [y/n]; comparison tables [y/n]; explicit RQs [y/n]; future-work section [y/n]

## Section list

## Paragraph map (Introduction; one results/validation section; taxonomy or comparison section; conclusion and future work)
| Section | Para | Function | First-sentence template | What follows the claim | Citation pattern (single / cluster of n) | Figures or tables referenced |
|---|---|---|---|---|---|---|

## Summary-to-judgment turns (where, marker construction, backing, strength)
## Figure and table roles (per item: type, claim carried, stated before or after, interpreted or pointed)
## Introduction closing chain (paragraph count, gap form, contribution form, organization paragraph, mapping to sections)
## Taxonomy (reviews): axis kinds, justification, exclusivity, depth, announcement template, placement, reuse
## Comparison: dimension kinds, table-introduction template, trade-off vs winner, condition handling, rubric
## Research questions: statements as templates, answered where, cross-reference form
## Results ladder: rungs, verbs, interpretation placement, anomaly handling, ending
## Future work: items with traced source (limitation / taxonomy cell / open question), placement, pattern
```

## Output formats

`profiles/language_style.md` (or `profiles/author_style.md`):

```markdown
# Language Style Profile   (or: Author Style Profile)

## Source corpus
- Folder, number of papers, venues represented, date generated, extraction risks

## Register
## Section openers (slot templates)
## Gap and limitation shapes
## Contribution phrasing
## Transitions
## Hedging calibration
## Callout templates (figures, tables, equations)
## Comparison shapes
## Conclusion shapes
## Generic connective phrases (max eight words each)
## Argument habits   (author profile only: the architecture findings for the user's own papers)
## Weaknesses to correct   (author profile only)
## Do not imitate
- Domain facts, numbers, results, prototype or dataset specifics, citations, and any sentence longer than eight words from any paper.

## Operational rules for writing-skill
1.
2.
3.
```

`profiles/argument_architecture.md`:

```markdown
# Argument Architecture Profile

## Source corpus
- Folder, papers by type (large review / small comparative review / research article / tutorial), venues, date generated, extraction risks

## A. Paragraph mechanics
### A1 Paragraph function sequences (per section, per paper type)
### A2 First-sentence positioning (slot templates per function)
### A3 Claim to evidence
### A4 Citation grouping
### A5 Summary-to-judgment turn
### A6 Figures and tables in the argument
### A7 Introduction closing chain

## B. Article-level architecture
### B1 Taxonomy construction (from N reviews)
### B2 Method comparison
### B3 Gap construction
### B4 Research questions to experiments
### B5 Results ladder
### B6 Future work derivation
### B7 Section endings and synthesis

## Role coverage
One row per `writing-skill` paragraph role. Roles marked `not observed` or `not learnable here` fall back to `references/section-moves.md`.

| Role | Papers showing it | Status | First-sentence template | Claim-to-evidence order | Citation pattern |
|---|---|---|---|---|---|
| intro-context | | | | | |
| literature-category | | | | | |
| limitation | | | | | |
| gap | | | | | |
| approach-and-contributions | | | | | |
| contribution-list | | | | | |
| research-questions | | | | | |
| organization | | | | | |
| method-objective | | | | | |
| model-or-assumption | | | | | |
| mechanism | | | | | |
| design-implication | | | | | |
| setup | | | | | |
| results | | | | | |
| comparison | | | | | |
| discussion-or-limitation | | | | | |
| conclusion | | | | | |
| abstract | | | | | |
| caption | | | | | |
| taxonomy-overview | | | | | |
| category-opener | | | | | |
| cross-cutting-comparison | | | | | |
| synthesis | | | | | |
| research-agenda | | | | | |
| response-to-reviewer | 0 | not learnable here | | | |

## Do not imitate
- Domain facts, numbers, results, any specific paper's category labels, citations, and any sentence longer than eight words.

## Operational rules for writing-skill
1. (which paragraph-function sequence to follow per section and paper type)
2. (which first-sentence templates and claim-to-evidence order to use per role)
3. (where this profile disagrees with knowledge files: the knowledge files win)
```

## Rules

- Extract style and structure, never content. No numbers, results, materials, ratings, model coefficients, citations, or a specific paper's category labels enter a profile. Axis kinds and dimension kinds are structure; the labels a paper gives its categories are content.
- No verbatim beyond eight words; every longer pattern becomes a slot template.
- When a corpus habit conflicts with `knowledge/ieee_editorial_conventions.md` or `knowledge/prose_quality.md`, the knowledge files win and the profile says so.
- When the author profile conflicts with the field profiles, the author profile wins unless the habit is listed under weaknesses to correct.
- Report patterns per paper type; never present a review's taxonomy habits as rules for a research article or the reverse.
- Never invent a pattern for a role the corpus does not show. An unobserved role is recorded as `not observed` and left to the built-in patterns; a profile that claims coverage it does not have is worse than no profile.
- Regenerate when the corpus changes; note the date. Profiles are calibration, not rules; the writing skill may deviate when the brief asks.
