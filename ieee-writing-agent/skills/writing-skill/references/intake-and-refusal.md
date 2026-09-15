# Input decisions and paragraph briefs

The intake gate tests whether the information needed for the requested work is available. It does not require a particular form and does not reject a section simply because it contains several paragraphs.

## Recover before asking

Use the current request, relevant earlier decisions, supplied text, and manuscript state. Fill ordinary context such as section, role, position or length from an unambiguous assignment. Do not infer a new scientific claim solely from a topic or filenames. For an edit that preserves meaning, identify the existing claim and proceed; ask only if competing interpretations would change the result.

A new paragraph needs a claim/core idea, purpose and position, plus evidence for methods/results/comparisons or sources for literature assertions. A definition or conceptual explanation still needs a reliable basis for technical facts. Missing optional fields use reasonable defaults. Standalone pasted text is a known position; it need not be bound to a manuscript.

## Decisions

| Request/context | Action |
|---|---|
| Rewrite/shorten pasted text, keep meaning | Use the existing claim; preserve numbers/conditions; no `claim: unchanged` password |
| Continue paragraph 2 from previously agreed claims | Retrieve the claim and evidence, then continue |
| Topic only, no stated or authorized candidate claim | Ask what judgment the paragraph should establish; do not fabricate prose |
| Analyze a source folder and propose claims | Read sources, return candidate claims with support, boundaries and uncertainties |
| Propose claims, wait for my approval | Stop after candidate claims, without drafting or recording approval |
| Propose supported claims and then draft the section | Show candidate claims, draft/check sequentially, retain candidate status for author review |
| Write a section from supplied/approved claims | Complete its paragraphs and an integration check; no per-paragraph reapproval |
| Results claim with no usable evidence | Request the concrete result/figure/condition; continue independent authorized analysis |
| Conflicting claim and manuscript state | Check whether the state is stale or the user already authorized a change; ask only for a real unresolved decision |
| Analysis only, do not change files | Read and report; do not create state, notes or drafts on disk |

User authorization to draft candidate claims is not evidence of scientific truth. Keep limitations, provenance and unresolved support visible. A `candidate` is not marked `author-approved` without an explicit author decision. Later user steering may narrow, extend or stop the authorized work.

## Brief fields (optional structured interface)

| Field | Meaning |
|---|---|
| id, section, role, previous, next | Unit identifier, purpose and neighbors; infer from a clear position if omitted |
| claim | User's assertion, previously accepted claim, or `unchanged` for an edit |
| evidence, refs | Files/passages/figures with conditions, reference notes or cite keys |
| manuscript, bib, state | Paths; remember project bindings after authorized writing |
| mode | write, revise, compress, caption, abstract, terms, plan |
| length, terms, style | Output target and preferences |
| output | concise default; annotated, clean, confirm-first |
| insert, unify | Optional explicit edit location or terminology authority; ordinary language is also valid |
| existing | Text or location being edited |

Useful roles include context, literature-category, taxonomy-overview, category-opener, comparison, synthesis, gap, contribution-list, research-questions, organization, method, setup, results, discussion, conclusion and caption. The complete move examples are in `section-moves.md`; a role label is not required to understand a plain-language task.

## Ask specifically when blocked

State the missing decision or evidence and what work can continue. For example: “The requested comparison needs the baseline and test condition. I found A in Table II; B's condition is missing. I can summarize A while you provide B.” Do not repeat a generic refusal when the user has supplied new context. Link the controlling skill rule if a toolkit rule is the reason for a pause.

## Examples

```text
压缩下面这段到 120 词，保持结论、引用和测试条件不变：<text>
```

```text
根据 reference/II/A 中的资料，先给 II-A 的候选 claim 和证据位置，等我确认再写。
```

```text
按上轮确认的五个 claim 逐段完成 II-A，写到 drafts/II_A/。
检查全节衔接；缺少支撑的地方标明，不要编数字。
```
