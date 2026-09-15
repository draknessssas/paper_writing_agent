# Editorial patterns and script lexicon

Read the relevant row when a prose finding needs explanation. These are local editing conventions and heuristics, not proof of AI authorship or universal IEEE prohibitions. Scientific meaning, required disclosure and explicit user/venue requirements take priority over surface preferences.

## Part B. AI-tell patterns, calibrated for IEEE style

Why this part exists: reviewers and editors now recognize the surface signature of machine-generated prose, and several of its habits (hype adjectives, decorative antithesis, dash-heavy rhythm) also violate IEEE editorial style. The calibration matters: some patterns that generic humanizers ban are legitimate in IEEE prose (en dashes in numeric ranges, passive voice for procedures, a single "In this article, ..." contribution statement). Follow the calibrated rule, not the generic one.

| ID | Pattern | Examples | Fix | Why |
| --- | --- | --- | --- | --- |
| B1 | Hype adjectives | groundbreaking, cutting-edge, unprecedented, remarkable, impressive, revolutionary, game-changing, seamless, seamlessly, holistic, synergistic | delete, or replace with the number or the specific property | Unsupported evaluation words invite the reviewer to disagree; IEEE titles and abstracts avoid "new"/"novel" |
| B2 | Audit adjectives | novel, significant, substantial, comprehensive, robust, powerful, state-of-the-art, promising, excellent, paradigm | keep only with a statistic, a robustness test, a defined benchmark, or a number | "Significant" without a test and "robust" without a perturbation study are empty |
| B3 | Hype verbs | unlock, unlocks, paves the way, pave the way, opens the door, open the door, opens new avenues, revolutionize, revolutionizes, empower, empowers, delve, delves, delving, harness, harnesses | state the concrete mechanism or result | Vague-mechanism verbs replace an explanation with an emotion |
| B4 | Audit verbs | leverage, leverages, leveraging, facilitate, facilitates | prefer "use", "allow", or the specific action; keep only when precise | Overused substitutes for plain verbs |
| B5 | Throat-clearing openers (ban) | Notably, Importantly, Crucially, Indeed, Ultimately, It is worth noting that, It should be noted that, It is worth mentioning that, It can be seen that, It is obvious that, It is evident that, It is clear that, As we all know, As is well known, As is known to all, It is well known that, Needless to say | delete the opener and start with the content; if something is well known, cite it | They announce importance instead of showing it; "it can be seen" hides the observer |
| B6 | Connective openers (audit) | Moreover, Furthermore, Additionally, Besides, What is more | use when the sentence adds a parallel point; reduce repetitive scaffolding | IEEE prose uses them, but a paragraph that starts three sentences this way is list-shaped, not argued |
| B7 | Content-free openers | In this section, we (ban); In this paper, we / In this article, we (audit) | replace with the content; use "this article" where it identifies the subject clearly, without repetitive scaffolding | The sentence has no information until its second half |
| B8 | Decorative antithesis | "not X but Y", "rather than merely", "on the one hand ... on the other hand" without factual content | keep only when both sides carry information | Rhetorical contrast is the most recognizable machine tic |
| B9 | Forced triads | lists padded to three items; three parallel clauses for rhythm | keep the items that are distinct and necessary | Rule-of-three padding adds words and no facts |
| B10 | Dashes | em dash in prose ("—" or LaTeX `---`); en dash outside numeric ranges | commas, colons, parentheses, or a new sentence; en dash only for numeric ranges (40–50 mm) and IEEE compound forms (dc–dc, voltage–current) | Dash-heavy rhythm is an AI tell, and IEEE style reserves en dashes for ranges and opposites |
| B11 | Vacuous intensifiers | truly, genuinely, in essence, in effect, essentially, actually, in fact, indeed, simply | delete | They add emphasis, not evidence |
| B12 | Weak qualifiers | very, quite, fairly, pretty, somewhat, rather (not "rather than"), relatively (audit: allowed with a stated comparison) | delete, or replace with the number or the baseline | A qualifier without a reference point is noise |
| B13 | Generic closers and outlook | "holds great promise", "opens new avenues", "which is of great importance", "in the future, ... will be explored" as the last sentence | end on the demonstrated result or one scoped outlook sentence | Stock endings signal that the writer ran out of content |
| B14 | Synonym cycling and heading echo | rotating "approach/method/technique/scheme" for the same object; first sentence restating the heading | keep the canonical term from the terminology registry; open with the claim | Synonym rotation breaks terminology consistency, which reviewers read as imprecision |
| B15 | Passive-voice calibration | "it is found that", "it was found that", "it was observed that", "was found to", "were found to", stacked "is performed", "is carried out" | active voice when the agent matters ("The controller regulates ..."); passive is acceptable for standard procedures ("The core loss was measured with ...") | Total passive bans do not fit IEEE methods prose; agentless observation chains do not fit any prose |
| B16 | Sentence length and rhythm | mean above 25 words; any sentence above 40; three consecutive sentences with the same structure | review readability; split overloaded clauses while preserving technical relationships; 40 words is a signal, not a hard limit | Long uniform sentences read as generated and hide the claim |
| B17 | Figure and equation callouts | "See Fig. 3", "Fig. 3 shows the results", "as shown in (5)" | "Fig. 3 shows X under Y, which confirms Z"; "(5) gives the boundary at which ..." | A callout that does not interpret is a caption, not prose |
| B18 | Exclamation and rhetorical questions | "!" anywhere; "?" outside at most one Introduction question | delete | Not technical register |
| B19 | Nominalization stacks | "the utilization of", "the implementation of the optimization of" | verbs: "using", "implementing", "optimizing" | Nominalization hides the actor and doubles the length |
| B20 | Answering unraised objections, fake alternatives | "one might argue that ...", "unlike naive approaches that ..." | delete unless a reviewer or the literature actually raised it | See A2 rule 7 |

## Part C. ESL patterns common in IEEE submissions

Why this part exists: inadequate English is an explicit rejection ground at most IEEE Transactions, and a few recurring patterns account for most of the reviewer irritation. Each one has a mechanical fix.

| ID | Pattern | Fix |
| --- | --- | --- |
| C1 | "With the rapid development of X, Y has attracted more and more attention" and variants ("with the development of", "more and more", "has attracted more and more attention", "attracted increasing attention", "attracted extensive attention") | Name the concrete driver with a number or a specific application: "Data-center power supplies now require X at Y" |
| C2 | "In recent years", "Recently, ... has been widely studied", "nowadays" | Cite the specific works and state the specific trend; delete the time filler |
| C3 | "It is well known that", "As is known to all", "obviously", "clearly" | Cite or delete; a claim that needs "obviously" usually needs a reference |
| C4 | "Aiming at the problem of ..." | "To address ..." |
| C5 | "has good performance", "better performance", "excellent performance", "high accuracy", "high efficiency", "low loss" without a number | Give the metric, the number, and the condition |
| C6 | Uncountable nouns pluralized: researches, literatures, equipments, informations | research, literature, equipment, information |
| C7 | "In this paper, a novel ... is proposed" | Verify novelty support when retaining "novel"; prefer a direct subject: "This article proposes ..." |
| C8 | Dangling modifiers: "Using the proposed model, the loss is reduced" | Give the modifier a subject: "Using the proposed model, the designer reduces the loss" or "The proposed model reduces the loss" |
| C9 | Article errors: "the" before general plurals ("the converters are widely used"); missing article before singular count nouns ("model is trained") | General plurals take no article; singular count nouns need one |
| C10 | Tense: "will" for obtained results; present for what was done | Past for what this work did ("was measured"); present for what figures show and for general truths |
| C11 | "respectively" misplaced or overused | Use once per sentence, at the end, only when the pairing is unambiguous; otherwise rewrite as two clauses |
| C12 | "etc.", "and so on" in technical enumerations | Close the list, or use "such as" with a complete representative set |
| C13 | Light-verb constructions: "make a comparison", "perform an analysis", "carry out an analysis", "give a description", "conduct an investigation", "make use of" | compare, analyze, describe, investigate, use |
| C14 | "can not", "in the meanwhile", "on the contrary" (used for "in contrast"), "at the same time" as filler, "what's more", "besides" at sentence start | cannot, meanwhile, in contrast, delete, delete, delete |
| C15 | Ordinal adverbs: firstly, secondly, thirdly, lastly | first, second, third, last |
| C16 | Noun stacks: "the proposed high-frequency transformer core loss prediction model accuracy" | Unpack with prepositions: "the accuracy of the proposed core-loss model for high-frequency transformers" |
| C17 | Redundant pairs: "first and foremost", "each and every", "basic fundamentals", "past history", "as a matter of fact" | Keep one word |
| C18 | Wordy fillers: in order to, due to the fact that, the fact that, a number of, a large number of, a lot of, at the present time, at this point in time, in the event that, has the ability to, the majority of, utilize, utilizes, utilization, prior to, subsequent to, for the purpose of, in spite of the fact that, plays a crucial role, plays a vital role, plays an important role | to, because, (delete), several or N, many or N, many or N, now, now, if, can, most, use, use, use, before, after, for, although, state what it does |
| C19 | "the proposed method/approach/scheme" repeated in every sentence | Name the method once (an acronym or a short name registered in the terminology registry) and use the name |
| C20 | "Research on", "study on" as subjects | Make the finding the subject: "X reduces Y", not "Research on X shows that Y is reduced" |

## Other contextual scan findings

Defensive wording (AUDIT, not a reason to hide a negative result): unfortunately, fails to, we were unable, we attempted to, we tried to, severe weakness, severe drawback, not ideal, disappointing, poor performance. Keep precise unfavorable findings when true; remove unsupported apologies or invented tradeoffs.

Other phrasing to inspect in context: in terms of, is able to, with the aim of. Prefer direct wording when meaning is preserved.
