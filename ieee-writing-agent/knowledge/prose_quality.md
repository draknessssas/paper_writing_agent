# Evidence-calibrated manuscript prose

Use this compact contract for substantive writing or review. Consult [pattern reference](prose_patterns.md) only for a relevant language issue; it retains the editorial examples and script lexicon. These local style preferences do not establish scientific truth or detect AI authorship.

Source lineage: the earlier toolkit adapted prevent-defensive-ai-writing (Tina0514, MIT), humanizer (blader), SNL-UCSB paper-writing-skill and IEEE editorial guidance. The detailed examples are retained in prose_patterns.md; evidence and meaning govern their use.

## A1. Claim ceiling and floor

State what the evidence supports, with the conditions that make it true. Do not overclaim, fabricate, hide negative findings, or unnecessarily weaken an established conclusion. A supported claim may be stated directly. Causal explanation, extrapolation and uncertain interpretation retain appropriate qualification.

A measured observation is not a universal claim; a simulation result is not a measurement. State simulation or analytical support explicitly without automatically surrounding it with vague hedges. For comparisons retain metric, baseline, conditions and any normalization. Attach the actual evidence rather than a stronger adjective.

## A2. Remove defensive padding without losing information

Delete redundant hedge stacks such as “may potentially” or “could possibly” when they express the same uncertainty twice. Multiple distinct conditions or uncertainties may legitimately require multiple qualifiers. Contributions and abstracts still need honest scope and uncertainty; no section is exempt from evidence discipline.

Describe limitations proportionately where readers need them. Avoid repetitive apologies, but repeat an essential condition in a standalone abstract or a separate claim when omission would mislead. A negative result may be reported directly. Do not replace “did not outperform” with an invented advantage or tradeoff. A stated scope boundary is not self-attack.

Interpret a result when it helps the argument and the evidence permits it. If a mechanism is a hypothesis, label it as such. No fixed observation→mechanism→implication template can justify adding an unsupported causal sentence.

## A5. Required disclosure

Preserve material information needed to assess a claim:

- Measured, simulated, analytical or inferred support.
- Evaluation conditions, data splits and relevant measurement methods.
- Comparison baselines, unmatched conditions and normalization.
- Material uncertainty, negative findings and limitations that bound the claim.
- Attribution separating prior literature from this study's results.

Compression must not remove these details merely to reach a word count. Evidence requirements are substantive; sentence rhythm, topic-first order and transition choices are preferences.

## Editorial checks

Use `scripts/prose_gate.py` to locate patterns; it does not assess evidence. BAN findings are local editorial errors to resolve in the applicable prose. AUDIT requires contextual review: `novel`, `robust`, `significant` and similar expressions need a precise basis, not a synonym substitution. Keep a supported, necessary term when appropriate and record material reasons in an annotated/audit result.

COUNT reports length and other heuristics. A sentence over 40 words invites review; it does not automatically fail. Prefer readable engineering prose and varied sentence lengths; preserve technical relationships. Use actual user/venue constraints when stricter formatting is requested.

Check changed prose, fix relevant problems and rerun affected checks once changed. Detailed check tables are optional for ordinary edits. Never claim a gate passed if it was not run, or treat BAN 0 as proof of factual correctness.
