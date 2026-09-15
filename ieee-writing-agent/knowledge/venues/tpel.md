# Venue Module: IEEE Transactions on Power Electronics (TPEL)

Optional module. Loaded only when `profiles/active_profile.yml` sets `venue: tpel` (bootstrap: `IEEE_VENUE=tpel`). When it is loaded, `manuscript-reviewer` adds a venue-fit dimension and `writing-skill` applies the abstract and evidence expectations below. Without it, the workspace stays venue-neutral and uses `knowledge/ieee_editorial_conventions.md` only.

Reference abbreviation: `IEEE Trans. Power Electron.`

As of 2026-07. Fees, page limits, and submission-system details change. Verify against the current PELS author guidelines (sources at the bottom) before relying on any fee or limit stated here.

## 1. Scope and out-of-scope rejection

- TPEL covers conversion, control, applications, and system integration of electric power using semiconductors and switching devices, focusing on power converters including components and system integration. It publishes modeling/simulation, analysis, design, fabrication, testing/characterization, evaluation/validation, and applications of power-electronic components, converters, converter systems, and system integrations. Review, tutorial, and survey articles are welcome.
- Out-of-scope papers may be summarily rejected. Explicit example from the guidelines: manuscripts "focused solely on physics, theory, materials, design and/or characterization of components, systems, and applications without sufficient and demonstrated content in power electronics."
- Consequence: every TPEL manuscript must state its power-electronics contribution (topology, modulation, control, magnetics, device application, loss modeling, reliability, EMI, thermal management) explicitly, as an application, converter-level payoff, or design implication. Redirect candidates: pure device physics (TED); grid or system level (TSG, TIA); control theory without a converter contribution (TIE, TCST).

## 2. Evidence expectations

- Verbatim from the PELS TPEL page: "Experimental results obtained from a full-hardware test setup are generally required for publication in IEEE Transactions on Power Electronics."
- Workspace interpretation (not an official quote): converter and hardware papers need a measured prototype (hardware-validated). Modeling and characterization papers with power-electronics relevance (magnetics and core-loss models, device or component models, loss estimation, physics-informed or data-driven models for power magnetics) need measured validation data (B–H loops, calorimetric or wattmeter loss measurements), not necessarily a converter prototype. Simulation-only support means the claim status is "needs experimental evidence"; allowed weakened form: "simulation results indicate ...".
- Every performance or accuracy claim states operating conditions (voltage, load, switching frequency or excitation waveform, flux density, frequency, temperature) and the measuring instrument. Comparisons are made at matched conditions or carry a normalization statement.
- Typical validation ladders reviewers expect. Converter papers: operating-principle analysis, design, simulation, hardware prototype, measured waveforms (steady-state, transient), efficiency versus load, loss breakdown, thermal, comparison table versus prior art. Modeling papers: model formulation, identification or training data and protocol, prediction versus measurement across materials, waveforms, frequencies, and temperatures, defined error metrics, comparison versus prior models (Steinmetz variants such as iGSE, Preisach, Jiles–Atherton, neural baselines), power-electronics design implication.
- Reviewer-risk items: missing state-of-the-art comparison table; missing prototype photo and parameter table; "first" or "novel topology" claims without a derivation argument; power-density numbers without a volume definition; control claims without stability or bandwidth evidence; error metrics without definitions; generalization claimed beyond tested materials, waveforms, or frequencies; oscilloscope captures without per-channel scales; text that refers to figure elements by color.

## 3. Paper types, length limits, and charges

- Regular paper: no hard page limit; 10 pages at no charge, then a mandatory overlength charge of $200 per page starting on page 11.
- Letter: four or fewer pages in final form including references; longer manuscripts are not reviewed. Expedited review with reduced revision cycles.
- Correspondence: two pages maximum; corrections no longer than one page.
- Survey/Review/Overview: authors not invited by the EiC must first send a one-page single-column summary to the Admin.
- 2026 IEEE APC list: TPEL is a hybrid OA journal; open-access APC $2,800; overlength $200 per page beyond 10 pages (regular) or 4 pages (letter).
- Page estimation rule (final-files checklist): 3 pages of single-column double-spaced text (no figures, at least 10 pt font) = 1 printed page; 6 figures or tables = 1 printed page; each subfigure part counts separately; always round up.

## 4. Manuscript format at submission

- Double column, single spaced, on letter or A4 paper, figures and tables interspersed in the text. Single PDF under 40 MB; standard fonts; no cover page; no page or line numbers.
- Author byline required at all review stages (single-blind). Do not include biographies, photos, or the copyright form in the initial submission.
- Primary email address must be institutional.
- Abstract: 150 to 200 words (TPEL's own guideline), one paragraph, no abbreviations, references, or equations. Multimedia papers add one sentence describing the accompanying content.
- Optional color printing costs $1,045 base plus $275 per color figure; figures must read in grayscale.

## 5. Review process

- Single-blind, minimum two independent reviewers, similarity screening on every submission. Inadequate English "will be grounds for rejection"; an inadequate literature review or inadequate references are also grounds for rejection.
- Submission through the IEEE Author Portal; peer review in ScholarOne; final files through Manuscript Central.
- Editorial contacts (as of 2026-07): EiC Xiongfei Wang (peleditor@ieee.org); TPEL Letters Executive Editor Maryam Saeedifard (PELletters@ieee.org).

## 6. Conference-paper extensions

- Papers previously published at PELS-sponsored conferences (ECCE, APEC, INTELEC, and others) can be considered, but improvements and additions beyond the conference paper are required (IEEE PSPB Operations Manual 8.1.7.E).
- The conference paper must be cited in the references and noted in a footnote to the title on page 1. Multi-part papers are normally discouraged.

## 7. Post-acceptance

- Final files are due within 7 days of acceptance. Only minor editorial changes and small technical clarifications are permitted before final upload; figures and text may not be removed after acceptance; IEEE runs a final similarity check. Early Access appears 3 to 4 weeks after final-file submission.
- Regular papers (not Letters) require a brief biography plus a passport-style photo per author at the final-file stage.

## 8. Venue ecosystem for citation checks

Core venues and their IEEE abbreviations: `IEEE Trans. Power Electron.` (TPEL); `IEEE J. Emerg. Sel. Topics Power Electron.` (JESTPE); `IEEE Trans. Ind. Electron.` (TIE); `IEEE Trans. Ind. Appl.` (TIA); `IEEE Trans. Magn.` (TMAG); `IEEE Trans. Instrum. Meas.` (TIM); `IEEE Open J. Power Electron.`; conferences APEC, ECCE, IPEC/ECCE-Asia, EPE. TPEL reviewers routinely check whether recent (last 3 to 5 years) TPEL and JESTPE work is cited.

## Known unknowns (do not state as fact)

- No TPEL graphical-abstract requirement was found in official guidance.
- Which abstract limit production enforces (TPEL 150–200 vs IEEE-wide 150–250) is unconfirmed; target 150–200.
- Current acceptance rate and review turnaround times are not published on official pages found.
- TPEL's own guidelines PDF shows "IEEE Trans. Power Electronics" in one example; the official abbreviations list specifies "IEEE Trans. Power Electron."; use the official-list form.

## Sources

- TPEL Guidelines for Manuscript Submission (REV 2025): https://www.ieee-pels.org/wp-content/uploads/2025/07/REV-2025-TPEL-Guidelines-for-Manuscript-Submission.pdf
- PELS TPEL page: https://www.ieee-pels.org/publications/transactions-on-power-electronics/
- TPEL Final-Files Checklist (REV Nov 2025): https://www.ieee-pels.org/wp-content/uploads/2025/11/REV-Nov-2025-TPEL-Checklist-and-Guidelines-for-Submitting-Final-Files-for-Paper-Publication.pdf
- IEEE Article Processing Charges List: https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Article-Processing-Charges-List.pdf
- IEEE Author Portal for TPEL: https://ieee.atyponrex.com/submission/dashboard?siteName=tpel-ieee
