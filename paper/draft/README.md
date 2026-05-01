# White Paper Draft

The current white paper draft was produced during the chat-based collaboration that preceded this repository. It exists as a `.docx` file outside this repo (last filename: `Participatory_AI_Economy_Nebulai_WhitePaper.docx`) and is approximately 17 pages long.

## Contents of the existing draft

The `.docx` draft contains the following sections (current state):

1. **Title page** — "The Participatory AI Economy: A Framework for Accelerated AI Development, Broadly Owned"
2. **Table of contents**
3. **Executive Summary**
4. **Part I — The Inflection: Why the Default Trajectory Fails**
5. **Part II — The Architecture: Six Pillars of a Participatory AI Economy**
6. **Part III — How the Pillars Compound**
7. **Part IV — Implementation by Country Tier**
8. **Part V — The Capitalist Case**
9. **Part VI — A Phased Pathway, 2026–2032**
10. **Conclusion: An Invitation**

## Sections drafted in chat but not yet in the docx

These sections were drafted in the chat session and need to be incorporated:

- **Status Quo Diagnostic** (the four-scenario "empty quadrant" analysis) — destined for Part I or as a new Part 0
- **Organic Convergence** (documenting how sovereign AI is already being built without the citizen-facing layers) — destined for a new Part II
- **AI and Global Order** (the geopolitical stability analysis with Ukraine/Gaza/Iran/Romania evidence) — destined for a new section between current Parts IV and V
- **Adoption Equilibrium** (the median-voter analysis across regions) — destined for Part V or a new section
- **The Bismarck Calculation** (the defensive incentive argument; coerced-redistribution counterfactual) — destined for Part V or a new section
- **Literature and Antecedents** (situating the framework in Korinek-Stiglitz, CIP, Saksena, Acemoglu-Restrepo) — destined for after Part II
- **Methodology** (technical companion describing the simulation) — destined for an appendix or companion paper
- **Limitations** (the explicit list from `paper/sections/peer_review_critique.md`) — destined for a methodology appendix or companion paper

## Workflow for revising the paper

After the simulation reaches v0.5 (Session 5–6 of roadmap), the paper revision workflow is:

1. Open the existing `.docx` draft
2. Section by section, identify which figures and numbers need updating from the simulation output
3. Replace stylized chat-session numbers with actual model output (with confidence intervals)
4. Add the new sections listed above in their proper locations
5. Add the methodology and limitations sections as a final appendix or as a published-alongside companion technical paper
6. External methodology review (Korinek, CIP, Convergence Analysis) before publication

## Where the markdown sections live

Drafts of new sections, as they're produced during simulation development, go in `paper/sections/` with the filename pattern `XX_section_name.md`. These can be merged back into the `.docx` (or a new master document) at publication time.

## Format note

The original `.docx` was produced with full Nebulai brand styling:
- Purple #7C3AED for section headings, accent rules
- Indigo #1E1B4B for titles, H3s, table header backgrounds
- Lavender #F5F3FF for callout backgrounds
- Calibri throughout
- Justified body text

When generating new figures in `src/analysis/chart_builders.py`, match this palette for consistency.
