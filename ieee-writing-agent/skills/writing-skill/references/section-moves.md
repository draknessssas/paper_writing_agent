# Section moves: language-level paragraph patterns

These are optional structural examples. Select the role needed for the task; evidence and reader comprehension take priority over a fixed sentence order, mandatory limitation sentence, or forward-pointing ending.

Each role below lists the purpose, the move sequence, the tense and voice habits, slot templates, evidence that must exist, and the pitfalls to check. Templates use slots in brackets; they are shapes, not sentences to copy. Venue-neutral IEEE register; a loaded venue file may add expectations (for example abstract length or a required evidence ladder).

## Abstract (one unit)

Purpose: the whole argument in one paragraph. Moves: problem and why it matters; approach and its key mechanism; validation vehicle and scope; the most important supported number; implication. Keep it self-contained and follow the applicable venue rules on citations, equations and abbreviations. State the headline claim at supported strength and preserve all necessary scope/uncertainty.

Templates: "[Application] requires [property], but [limitation of current practice]." "This article [proposes/presents] [approach] that [mechanism]." "The [model/converter/method] is validated [scope: materials, conditions, prototype rating]." "[Metric] is [number] at [condition], compared with [baseline number] for [baseline]." "The result [implication for design or analysis]."

Pitfalls: opening with background history; hedged headline; listing sections; numbers without conditions.

## Introduction: context paragraph (intro-context)

Purpose: establish the application demand and the technical bottleneck in concrete terms. Moves: application and requirement (with a number or a specific case); the physical or engineering bottleneck; why it matters for the reader's design problem. Present tense. Citations for facts that are not common knowledge.

Templates: "[Application] now operates at [condition], which places [requirement] on [component or subsystem]." "At these conditions, [quantity] becomes [problem] because [mechanism]."

Pitfalls: "with the rapid development of"; "more and more"; generic global-demand openings; starting with the proposed method.

## Introduction: literature-category paragraph

Purpose: characterize one family of prior work and its shared limitation. Moves: name the family; what it does and on what basis; representative detail as stated in the sources; the limitation the family shares, tied to the manuscript's core idea; bridge. Full rules in `literature-paragraphs.md`.

Templates: "[Family] [what it does] [3]–[6]." "These models [strength], and [ref] reports [number as stated] for [condition]." "Their [parameter/assumption] is [property], so [limitation] when [condition]."

Pitfalls: paper-by-paper listing ("A proposed ... B proposed ..."); loaded verbs ("fails", "ignores"); limitations the sources do not show.

## Introduction: limitation and gap paragraphs

Purpose: state what remains unresolved across the families, precisely, as the setup for the contribution. Moves: what the families share; the unresolved requirement; the consequence for the application; the gap sentence, which is the user's core idea, not a new claim. The gap is citation-backed by the preceding category paragraphs.

Templates: "Across these approaches, [requirement] remains [unmet] because [shared cause]." "A [model/converter/method] that [property] under [condition] has not been [demonstrated/reported]."

Pitfalls: gap wider than the contribution; "to the best of our knowledge" without a search basis; premature limitations of the proposed work.

## Introduction: approach and contributions

Purpose: name the proposed approach, its mechanism, and the numbered contributions that the evidence supports. Moves: "This article proposes ..." once; mechanism in one sentence; validation scope; numbered contributions (each maps to a section and to evidence); paper organization only if the venue expects it.

Templates: "This article proposes [approach], which [mechanism] to [effect]." "The contributions are threefold: 1) [contribution] (Section II); 2) ...; 3) ..." Each contribution is a result, not an activity ("a model that ... within X% across Y" rather than "we develop a model").

Pitfalls: contributions worded as tasks; unsupported novelty; contributions exceeding the evidence; vague rather than informative qualifications.

## Method: objective, model or assumption, mechanism, design implication

Purpose: explain what the method does and why it works, in the order a reader needs to reproduce or evaluate it. Moves: objective of this part; assumptions or model structure; the mechanism or derivation step with its equation link; what the result means for design or analysis. Present tense for the method, past tense for choices made in this work.

Templates: "The objective of this stage is to [what], given [inputs]." "Under [assumption], [quantity] follows (n), where [symbol] is [meaning]." "Therefore, [consequence], which [design implication]." "Fig. n shows [structure], in which [element] [function]."

Pitfalls: textbook derivations reproduced in full; equations without an interpreting sentence; symbols not in the registry; passive chains ("it is assumed ... it is obtained ... it is found").

## Setup (experimental or evaluation)

Purpose: give the reader the conditions that bound every later claim. Moves: what was built or used (ratings, materials, dataset); conditions covered (ranges, waveforms, temperatures, splits); instruments or measurement method; baselines and how conditions were matched; purpose of the test. Past tense.

Templates: "The [prototype/dataset] consists of [items], covering [ranges]." "[Quantity] was measured with [instrument] at [condition]." "[Baseline] serves as the reference, evaluated on the same [data/conditions]."

Pitfalls: missing instruments; ranges stated without units; baselines evaluated under different conditions without saying so.

## Results

Purpose: present one result and its physical interpretation. Moves: condition; observation with the number; comparison with baseline or expectation; physical interpretation; the supported claim. Past tense for measurements, present tense for what the figure shows and for the interpretation.

Templates: "At [condition], the measured [quantity] is [number] (Fig. n)." "Compared with [baseline] under the same [condition], [quantity] [changes] from [a] to [b]." "This difference arises because [mechanism]." "The result confirms [claim] within [scope]."

Pitfalls: "Fig. n shows the results" without interpretation; results without conditions; hedged interpretation of a measured fact; unbounded comparatives ("outperforms").

## Comparison

Purpose: place the result against prior work at matched conditions. Moves: the metric and its definition; the baselines and their conditions; the normalization; the comparison with numbers; the supported tradeoff, avoiding redundant repetition. Comparison tables are cited, and the text says what the table shows.

Pitfalls: numbers quoted from prior work that the source does not state; unmatched conditions without a normalization statement; "superior" without a metric.

## Discussion or limitation (scoped)

Purpose: bound the claim where the reader needs the limitation to interpret it. Moves: what is limited; where the evidence still holds; what would extend it. No global negative labels. See Part A5 of `knowledge/prose_quality.md`.

Template: "The validation covers [scope]; extending it to [other scope] requires [what]."

## Conclusion

Purpose: restate what was proposed and demonstrated, with the decisive evidence and the scope. Moves: what was proposed; what was demonstrated and the headline number; the boundary; one implication or outlook sentence. Past tense for what was done. No new claims, no new hedges.

Pitfalls: repeating the abstract verbatim; reopening limitations; "future work will explore" as the last sentence.

## Caption (figure or table)

Purpose: make the figure or table stand alone. Pattern: what is shown; condition; signals or quantities with units; the main visible trend or comparison; a boundary when needed. Figure caption below the figure, starts with a capital, never with "A", "An", or "The". Table caption above, no terminal period, TABLE with Roman numerals. Per-channel scales for oscilloscope captures when supplied; `[NEED: channel scales]` when not. Every measured-result caption carries its condition; every comparison caption carries its normalization. The text callout interprets: "Fig. n shows [what] under [condition], which [confirms/indicates] [claim]."

Templates: "Measured [quantity] versus [variable] at [condition]." "Comparison of [quantity] predicted by [models] and measured values for [material/setup] at [condition]." "Photograph of the [rating] prototype with [labeled elements]."

## Response to a reviewer (one point)

Purpose: answer one reviewer point directly. Moves: the direct answer; the concrete revision; the evidence (figure, table, number); the location in the revised manuscript. Thank once per reviewer, not per point. When the criticism targets an unclaimed dimension, clarify the scope instead of conceding. Never promise work not done.

## Introduction: organization paragraph (organization)

Purpose: map the contributions to the sections in one short paragraph, when the venue or the field expects it (check A7 of `profiles/argument_architecture.md`). Moves: one sentence per section or per contribution, in reading order; each names what the section establishes, not just its topic. Present tense.

Template: "Section II [establishes what]; Section III [does what] for [which contribution]; Section IV reports [evidence]; Section V concludes."

Pitfalls: listing topics without saying what each section shows; repeating the contribution list; a paragraph longer than four sentences.

## Research questions paragraph (research-questions)

Purpose: state the questions or hypotheses the article answers, each tied to where it is answered. Moves: the framing sentence; the numbered questions, each answerable and each mapped to a section, experiment, or figure; how the questions relate to the gap. When the field does not state explicit questions (B4 of the architecture profile), fold them into the contribution list instead.

Template: "This article addresses three questions. RQ1: [question]? (Section IV-A, Fig. n). RQ2: ..."

Pitfalls: questions the evidence cannot answer; questions without a mapped location; restating the contributions as questions.

## Review and survey roles

Consult B1, B2, B7, and A5 of `profiles/argument_architecture.md` for the field's conventions; the moves below are the venue-neutral default.

### taxonomy-overview

Purpose: announce the organizing scheme of the review once, before the category sections. Moves: the axes and why these axes (what question each answers for the reader); whether categories are exclusive or a matrix; the taxonomy figure or table callout, interpreted; the order in which the categories are treated. The category labels come from the user's brief and the state file's section theses, never from a profile.

Templates: "The literature is organized along [n] axes: [axis kind 1], which determines [what]; and [axis kind 2], which determines [what]." "Fig. n places each approach in this scheme; [what the placement shows]."

Pitfalls: axes that overlap; a taxonomy figure that is pointed at but not read; category labels that change later in the paper (register them in the terminology registry).

### category-opener

Purpose: open one category section by stating what unites its members and what the section will conclude about them. Moves: the defining property of the category; its position in the taxonomy; the section's thesis (what the category can and cannot do); how the section is ordered.

Template: "[Category] methods share [defining property], which makes them [strength] but [limitation] when [condition]."

Pitfalls: opening with a paper instead of the category; a section whose conclusion is not stated until its end.

### cross-cutting-comparison

Purpose: compare methods across categories on stated dimensions. Moves: the dimension kinds and why they matter to the reader; the comparison table callout, interpreted; the trade-offs (which method wins on which dimension under which conditions); what remains unmatched or unmeasured. State trade-offs; do not declare a winner unless the dimensions and conditions are matched.

Templates: "Table n compares the approaches on [dimensions]." "[Method family] leads on [dimension] at the cost of [dimension], whereas ..." "Conditions differ across [refs] in [what]; the comparison is therefore qualitative for [dimension]."

Pitfalls: numbers quoted from papers that do not state them; unmatched conditions without a normalization statement; a table that replaces the argument.

### synthesis

Purpose: close a category section or the review by drawing the conclusion the reader could not draw from any single paper. Moves: the cross-paper pattern (what most work does, what none does); the open problem this exposes; the bridge to the next category or to the research agenda. This is the summary-to-judgment turn made explicit: the judgment is backed by the categories just reviewed, with source citations retained where needed to make that judgment verifiable.

Templates: "Across [n] studies of [category], [pattern]; none reports [what]." "The open problem is therefore [problem], which [next section] examines from [angle]."

Pitfalls: summarizing instead of concluding; introducing new papers; a judgment stronger than the reviewed evidence.

### research-agenda

Purpose: derive future directions from what the review established. Moves: each item traces to a specific limitation, an empty cell of the taxonomy, or an open problem named in a synthesis paragraph; states what would have to be built or measured; states why it matters. Ordered by dependence or by importance, not by the order the categories appeared.

Template: "[Category] has been validated only for [scope] (Section n); extending it to [scope] requires [what], which would [payoff]."

Pitfalls: a wish list untethered from the text; items nobody could act on; repeating the gap paragraph of the Introduction.

## Cross-role habits

- One role per paragraph; the topic sentence asserts the claim; the last sentence points forward.
- Introduce the method clearly and use the registered name consistently; do not rotate synonyms.
- Numbers carry units and conditions; symbols match the registry; acronyms defined in the applicable body/abstract context.
- Callouts interpret; prose does not repeat captions.
