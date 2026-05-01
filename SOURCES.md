# Sources and Calibration Anchors

Every parameter in the simulation traces to a specific paper or dataset. This file is the master reference. Code comments cite this file by section number.

## Production side

### Task elasticity σ
- **Range:** 1.1–2.0
- **Default:** 1.5
- **Source:** Acemoglu & Restrepo (2022), "Tasks, Automation, and the Rise in U.S. Wage Inequality," *Econometrica* 90(5): 1973–2016. Table 3 reports σ estimates from 1.4 to 1.8 across specifications.
- **Cross-check:** Humlum (2019), "Robot Adoption and Labor Market Dynamics," reports task elasticities ~1.3–1.5 in Danish manufacturing.
- **Note:** Cobb-Douglas (σ=1) used as fallback for Stage 5 calibration; revisit whether two-sector model is needed.

### Initial automation threshold I (2025 baseline)
- **Default:** 0.26
- **Source:** Calibrated to match US 2025 labor share = 56% (BLS) given other parameters. No direct empirical observation.
- **Sensitivity:** I in [0.20, 0.32] tested.

### Automation expansion rate dI/dt
- **Default:** 0.012/year (Patchwork); 0.018 (SF Consensus); 0.030 (extreme acceleration)
- **Source:** Acemoglu, Autor, Dorn, Hanson, Price (2014), "Return of the Solow Paradox? IT, Productivity, and Employment in US Manufacturing," AER P&P. Implied automation rate from displacement effect calculations ~1pp/year cumulative.
- **Cross-check:** Acemoglu (2024), "The Simple Macroeconomics of AI," NBER WP 32487, implies ~1.5pp/year displacement rate under Goldman Base.

### Reinstatement rate dN/dt
- **Default:** 0.005/year (Patchwork); 0.012 (Participatory)
- **Source:** Acemoglu & Restrepo (2019), "Automation and New Tasks," *Journal of Economic Perspectives* 33(2): 3-30. Historical reinstatement rate calibrated from new-task creation in BLS occupational data.

### AI productivity growth rate (TFP)
- **Default:** 0.005–0.040/year depending on scenario
- **Slow Diffusion:** 0.001 (Acemoglu 2024)
- **Goldman Base:** 0.015 (Briggs & Kodnani, Goldman Sachs Research, 2023)
- **SF Consensus:** 0.030–0.050 (IMF SDN/2026/001 acceleration scenario)

## Firm markup distribution

### Mean (sales-weighted) markup, 2020 baseline
- **Default:** 1.22
- **Source:** De Loecker, Eeckhout, Unger (2020), "The Rise of Market Power and the Macroeconomic Implications," *QJE* 135(2): 561-644. Fig 4 reports US sales-weighted average markup ~1.22 in 2020.

### Markup dispersion (std of log)
- **Default:** 0.30
- **Source:** Calibrated so 99th-percentile markup ≈ 2.0, matching DLEU 2020 Fig 6.

### Markup growth rate
- **Default:** 0.005/year
- **Source:** DLEU 2020. Mean markup rose from 1.18 (1980) to 1.22 (2020), implying ~0.001/yr historical, but accelerated post-2010 to ~0.003-0.005/yr.
- **Pillar 5 dampening:** 0.40 (open-weights creates competitive pressure on frontier-AI markups)

### Profit share of value added (2020 baseline)
- **Implied:** 0.17–0.18
- **Source:** Karabarbounis & Neiman (2014), "The Global Decline of the Labor Share," *QJE*; Barkai (2020), "Declining Labor and Capital Shares," *Journal of Finance*. US pure profit share ~13–18% depending on methodology.

## Labor market

### Monopsony parameter ε (firm-specific labor supply elasticity)
- **Range:** 2–6 typical; we use 9–15 in baseline
- **Source:** Azar, Marinescu, Steinbaum (2022), "Labor Market Concentration," *J Human Resources* 57(S): S167-S199. Mean ε ≈ 3 implies wage markdown ~25%; we calibrate higher (ε=9, markdown ~10%) because that's needed to hit the 56% labor share given our markup levels.
- **Cross-check:** Manning (2003), *Monopsony in Motion*. Range of estimates 2–10.
- **Note:** This is the one parameter genuinely chosen for fit rather than from literature midpoint. Sensitivity-tested.

### Skill differential in monopsony
- **Default:** ε_complement = 1.5 × ε_safe
- **Source:** Webber (2015), "Firm Market Power and the Earnings Distribution," *Labour Economics*. Higher-skill workers face less monopsony.

## Capital markets

### Cost of equity (real, baseline)
- **Default:** 0.07
- **Source:** Damodaran (2024), "Implied Equity Risk Premium," NYU Stern. US implied real ERP + risk-free ~7%.

### Cost-of-equity premium per 10% sovereign acquisition
- **Default:** 0.005 (50 bps)
- **Source:** Calibrated from Norwegian GPFG impact studies (Sundaresan & Sushko 2014) and Singapore Temasek effects on listed firm valuations.
- **Note:** Highly uncertain. Sensitivity-tested in range 25–100 bps.

### Capital flight responsiveness
- **Default:** 0.008/year per pp of tax differential, with 0.005 baseline
- **Source:** Bach, Bourdier, Bozio (2014), "L'évaluation économique de l'impôt de solidarité sur la fortune," IPP. French ISF data: ~0.8% of taxable assets per year per pp of effective rate differential.
- **Cross-check:** Brülhart, Gruber, Krapf, Schmidheiny (2022), "Behavioral Responses to Wealth Taxes: Evidence from Switzerland," *AEJ: Economic Policy*. Lower estimates ~0.3-0.5%.

### AI capital depreciation rate
- **Default:** 0.20–0.25/year
- **Source:** McKinsey (2025), "The Cost of Compute"; IEEE ComSoc (2025) hyperscaler depreciation analysis. Frontier GPUs obsolete in 4–7 years (~17–25%/yr); model weights in 1–3 years (~40%/yr).

### Traditional capital depreciation rate
- **Default:** 0.05/year
- **Source:** BLS multifactor productivity series, equipment + structures aggregate.

## Wealth dynamics

### Top-decile differential return premium
- **Default:** 0.020 (200 bps)
- **Source:** Saez & Zucman (2016), "Wealth Inequality in the United States since 1913," *QJE* 131(2): 519-578. Top decile r systematically ~150–250 bps higher than median, attributed to better diversification, hedge fund / PE access, lower fees as fraction of return.
- **Fagereng, Guiso, Malacrino, Pistaferri (2020)**, "Heterogeneity and Persistence in Returns to Wealth," *Econometrica*. Norwegian admin data confirms differential.

### Inheritance rate (top decile to top decile transfer)
- **Default:** Transfers 0.015 of total top-decile wealth per year
- **Source:** Piketty, Postel-Vinay, Rosenthal (2014), "Inherited vs Self-Made Wealth," *Explorations in Economic History*. Inheritance flow ~10-15% of national income annually; we use the share that recirculates within top decile.

## Household saving rates by decile

- **Source:** Saez & Zucman (2016) supplementary data; Mian, Straub, Sufi (2021), "The Saving Glut of the Rich," NBER WP 26941.
- **By decile (1-10):** -0.02, 0.00, 0.01, 0.02, 0.04, 0.06, 0.10, 0.15, 0.22, 0.30
- **Top 1% within top decile:** 0.40

## Initial wealth distribution (US 2025 SCF approximation)

- **Top 1%:** 30.4%
- **Top 10%:** 76.0%
- **Bottom 50%:** ~2.5%
- **Source:** Federal Reserve, Survey of Consumer Finances 2022, projected to 2025.

## Initial labor share (US 2025)

- **Default:** 0.56
- **Source:** BLS Productivity Program, nonfarm business sector labor share, 2025 Q4.

## Skill exposure to AI

### Distribution of safe / substitute / complement labor
- **Defaults:** 20% / 50% / 30% by population
- **Source:** Webb (2020), "The Impact of Artificial Intelligence on the Labor Market"; Eloundou, Manning, Mishkin, Rock (2023), "GPTs are GPTs," OpenAI/UPenn. ~80% of US workforce has at least 10% AI exposure; ~19% has at least 50% exposure.
- **Cross-check:** IMF Cazzaniga et al. (2024) Gen-AI note: 60% of advanced-economy workforce exposed.

### Distribution by income decile (which deciles have which skill type)
- Decile 1-2: predominantly safe (manual / personal services)
- Decile 3-7: predominantly substitute (clerical / cognitive routine)
- Decile 8-10: predominantly complement (managerial / specialized cognitive)
- **Source:** Frey & Osborne (2017), "The Future of Employment," *Technological Forecasting and Social Change*. Probabilistic mapping of occupations to automation risk; cross-walked to BLS occupation-by-decile distribution.

## Geopolitical stability components

These are illustrative calibrations, not empirically derived. Component weights and base levels are calibrated to recent qualitative observations:

- **Interstate conflict component (current world):** 70/100. Source: Atlantic Council 2026 AI Cold War assessment; Carnegie Endowment 2026 Fog of AI War analysis; documented Ukraine, Gaza, Iran AI deployments.
- **Information warfare component:** 80/100. Source: CIGI 2025 election interference data; Romania 2024 election annulment; deepfake operations documented across 2024–2026 election cycle in 15+ countries.
- **AI arms race component:** 70/100. Source: Stockholm International Peace Research Institute 2025 Yearbook; CSIS 2025 export control analysis; Stargate, French €109B, Saudi HUMAIN, EU InvestAI all documented.

Causal mappings from policy architecture to component scores are theoretical, drawing on Mearsheimer (offensive realism), Ikenberry (liberal international order), Allison (Thucydides Trap). The **literature on whether bipolar splits produce conflict is genuinely contested** — model results should be treated as illustrative.

## Country indicators

For country disaggregation (Session 8), use:
- **Penn World Tables 11.0** for capital stocks, output, labor force
- **World Bank World Development Indicators** for GDP, population
- **OECD AI indicators** (https://oecd.ai) for country-level AI investment, talent, and capacity
- **Stanford AI Index 2025** for foundation model counts by country
- **Atlantic Council GeoTech Center** for sovereign AI strategies inventory

## Data update procedure

When refreshing data:
1. Download to `data/raw/` with a date-stamped filename
2. Update `data/raw/README.md` with the new download date
3. Re-run baseline calibration: `python -m calibration.baseline_2025`
4. If parameters drift more than 5% from previous calibration, document in `ROADMAP.md` decisions log
5. Re-run all scenarios: `python -m src.core.simulator --all-scenarios`
6. Compare results to previous run; note any qualitative changes
7. Update paper figures: `python -m src.analysis.chart_builders --paper`

---

# Addendum (2026-05-01): Additional citations for revised approach

The original `SOURCES.md` above covers the core macro literature for the bespoke
heterogeneous-agent build. The revised approach (multi-model + RDM + comparative
package analysis + game-theoretic robustness, per `PREREGISTRATION.md`) requires
additional anchors. These sources are referenced from the new pillar specifications
in `src/packages/`, the bilateral US-China model, and the methodology section.

## AI economics — beyond Acemoglu-Restrepo

### Korinek body of work (most-aligned researcher per CLAUDE.md)
- **Korinek & Stiglitz (2017)**, "Artificial Intelligence and Its Implications for
  Income Distribution and Unemployment," NBER Chapter; foundational AI-inequality
  framework
- **Korinek & Stiglitz (2021)**, "Artificial Intelligence, Globalization, and
  Strategies for Economic Development," NBER WP 28453
- **Korinek (2024)**, "Scenarios for the Transition to AGI," NBER WP — directly
  applicable scenario-design framework; should be the methodological base for
  scenario specification
- **Korinek & Juelfs (2023)**, "Preparing for the (Non-Existent?) Future of Work,"
  NBER WP 30172 — UBI-relevant

### Growth-side AI macro
- **Aghion, Jones & Jones (2017)**, "Artificial Intelligence and Economic Growth,"
  NBER WP 23928 — counterpoint to displacement-side framing
- **Aghion, Antonin, Bunel & Jaravel (2023)**, "Modern Manufacturing Capital, Labor
  Demand, and Product Market Dynamics," AER

### Empirical productivity effects
- **Brynjolfsson, Li & Raymond (2023)**, "Generative AI at Work," NBER WP 31161 —
  first large-N causal estimate of GenAI productivity (call center study, ~14%
  productivity boost concentrated on low-skill workers)
- **Autor (2022)**, "The Labor Market Impacts of Technological Change: From
  Unbridled Enthusiasm to Qualified Optimism to Vast Uncertainty," NBER WP 30074

### "Shape what AI is" thesis (basis for Package F Build-Different-AI)
- **Acemoglu (2021)**, "Harms of AI," NBER WP 29247
- **Acemoglu & Johnson (2023)**, *Power and Progress: Our Thousand-Year Struggle
  Over Technology and Prosperity*, PublicAffairs — Chapter 11 on AI is the
  intellectual basis for directed-AI policy
- **Mazzucato (2013)**, *The Entrepreneurial State*, Anthem Press
- **Mazzucato (2021)**, *Mission Economy*, Harper Business

## AI governance and global institutions (for Package C CERN-AI)

### CERN-AI / multilateral institution proposals
- **Hausenloy, Miotti & Dennis (2023)**, "Multinational AGI Consortium (MAGIC):
  A Proposal for International Coordination on AI," arXiv:2310.09217 — explicit
  CERN-for-AI design
- **Trager, Harack, Schiff et al. (2023)**, "International Governance of Civilian
  AI: A Jurisdictional Certification Approach," GovAI Working Paper
- **Ho, Trager, Bowman, Heim, Belfield et al. (2023)**, "International Institutions
  for Advanced AI," arXiv:2307.04699
- **Allison & Schmidt (2024)**, "Soft War, Hard War," *Foreign Affairs*; various
  IAEA-for-AI proposals

### AI risk and safety governance
- **Bengio, Hinton, Yao et al. (2024)**, "Managing AI Risks in an Era of Rapid
  Progress," *Science* — most-cited safety governance paper
- **Bengio et al. (2025)**, *International AI Safety Report 2025*, AISI Network
  commission — definitive 2025 baseline for AI risk claims; Bengio chair
- **Anderljung, Hazell & von Knebel (2023)**, "Protecting Society from AI
  Misuse: When Are Restrictions on Capabilities Warranted?" GovAI

### Compute governance (basis for Package D Compute-Centric)
- **Sastry, Heim, Belfield, Anderljung, Brundage et al. (2024)**, "Computing
  Power and the Governance of AI," arXiv:2402.08797 — canonical compute-governance
  paper
- **Heim, Anderljung, Belfield et al. (2024)**, "Compute Funds and Pre-training
  Transparency," GovAI
- **Sevilla, Heim et al. (2024)**, "Training Compute Trends," Epoch AI —
  empirical foundation for compute trajectory

### Open vs closed foundation models (basis for Hypothesis 1 Open-Weights Inversion)
- **Bommasani, Kapoor et al. (2024)**, "Considerations for Governing Open
  Foundation Models," Stanford HAI
- **Kapoor, Bommasani et al. (2024)**, "On the Societal Impact of Open Foundation
  Models," arXiv:2403.07918
- **Solaiman (2023)**, "The Gradient of Generative AI Release," arXiv:2302.04844
- **Seger et al. (2023)**, "Open-Sourcing Highly Capable Foundation Models,"
  Centre for Long-term Resilience
- **DeepSeek-AI (2024–2025)**, DeepSeek V3 and R1 technical reports
- **Qwen Team (2024–2025)**, Qwen 2.5 / Qwen 3 technical reports

## Mechanism design and political economy (for game-theoretic robustness analysis)

- **Ostrom (1990)**, *Governing the Commons*, Cambridge UP — eight design
  principles directly applicable to AI compute and capability as commons;
  methodological frame for Package C and Hypothesis 10
- **Schelling (1960)**, *The Strategy of Conflict*, Harvard UP — focal points
  for coordination equilibria
- **Olson (1965)**, *The Logic of Collective Action*, Harvard UP — coalition
  stability conditions
- **Maskin (2008)**, "Mechanism Design: How to Implement Social Goals," AER
  Nobel Lecture
- **Acemoglu & Robinson (2019)**, *The Narrow Corridor*, Penguin —
  institutional dynamics; relevant to adoption-equilibrium argument
- **Tirole (2017)**, *Economics for the Common Good*, Princeton UP
- **Rodrik (2011)**, *The Globalization Paradox*, Norton — political trilemma
  (sovereignty, democracy, integration: pick two)

## Wealth dynamics — extending Piketty / Saez-Zucman

- **Stansbury & Summers (2020)**, "The Declining Worker Power Hypothesis,"
  Brookings Papers on Economic Activity — alternative to monopsony framing
  of labor share decline
- **Eggertsson, Robbins & Wold (2021)**, "Kaldor and Piketty's Facts: The Rise
  of Monopoly Power in the United States," *Journal of Monetary Economics*
- **Farhi & Gourio (2018)**, "Accounting for Macro-Finance Trends: Market
  Power, Intangibles, and Risk Premia," BPEA
- **Piketty (2020)**, *Capital and Ideology*, Harvard UP

## UBI and Universal Basic Capital (for Package E Direct Redistribution)

- **Sherraden (1991)**, *Assets and the Poor*, M.E. Sharpe — foundational
  Universal Basic Capital case
- **Atkinson (2015)**, *Inequality: What Can Be Done?*, Harvard UP — capital
  endowment proposal directly relevant to redesigning Pillar 1
- **Van Parijs & Vanderborght (2017)**, *Basic Income: A Radical Proposal*,
  Harvard UP
- **Marinescu (2018)**, "No Strings Attached: The Behavioral Effects of US
  Unconditional Cash Transfer Programs," Roosevelt Institute
- **Banerjee, Niehaus & Suri (2019)**, "Universal Basic Income in the
  Developing World," NBER WP 25598
- **OpenResearch UBI Study (2024)** — Y Combinator three-year US RCT results
- **GiveDirectly Long-Term UBI Study** (Kenya, ongoing)

## Active labor market programs (Pillar 4 / reskilling calibration)

- **Card, Kluve & Weber (2018)**, "What Works? A Meta Analysis of Recent Active
  Labor Market Program Evaluations," *JEEA* 16(3): 894–931 — canonical meta-analysis
- **Heckman, LaLonde & Smith (1999)**, "The Economics and Econometrics of
  Active Labor Market Programs," *Handbook of Labor Economics* Vol 3A
- **Cahuc & Carcillo et al.**, German Kurzarbeit / short-time work evaluations
- **Reynolds & Palatucci (2012)**, Trade Adjustment Assistance evaluation

## Antitrust / market power (for Package D structural separation)

- **Khan (2017)**, "Amazon's Antitrust Paradox," *Yale Law Journal* 126(3) —
  foundational structural-separation argument
- **Wu (2018)**, *The Curse of Bigness*, Columbia Global Reports
- **Hovenkamp (2021)**, "Antitrust and Platform Monopoly," *Yale Law Journal*
  130(8)
- **Philippon (2019)**, *The Great Reversal: How America Gave Up on Free
  Markets*, Harvard UP
- **Covarrubias, Gutiérrez & Philippon (2020)**, "From Good to Bad
  Concentration: US Industries over the Past 30 Years," NBER Macroeconomics
  Annual

## Geopolitics of AI (extending the handoff's IR sources)

- **Ding (2024)**, *Technology and the Rise of Great Powers: How Diffusion
  Shapes Economic Competition*, Princeton UP — directly applicable to
  US-China AI competition
- **Doshi (2021)**, *The Long Game: China's Grand Strategy to Displace
  American Order*, Oxford UP
- **Allison (2017)**, *Destined for War: Can America and China Escape
  Thucydides's Trap?*, Houghton Mifflin
- **Mearsheimer (2001, 2014 update)**, *The Tragedy of Great Power Politics*,
  Norton
- **Ikenberry (2020)**, *A World Safe for Democracy*, Yale UP
- **Murray, Maxwell, Cunningham (2024)**, RAND on AI and nuclear strategy
- **CSET / CNAS / Atlantic Council** policy briefs on US-China AI competition

## Robust Decision Making (methodology)

- **Lempert, Popper & Bankes (2003)**, *Shaping the Next One Hundred Years:
  New Methods for Quantitative, Long-Term Policy Analysis*, RAND —
  foundational RDM text
- **Kasprzyk, Nataraj, Reed & Lempert (2013)**, "Many Objective Robust
  Decision Making for Complex Environmental Systems Undergoing Change,"
  *Environmental Modelling & Software* 42
- **Kwakkel & Pruyt (2013)**, "Exploratory Modeling and Analysis," *TFSC*
  80(3) — EMA Workbench
- **Walker, Lempert & Kwakkel (2013)**, "Deep Uncertainty," *Encyclopedia of
  Operations Research and Management Science*

## Methodology / philosophy of macro modeling (limitations section)

- **Lucas (1976)**, "Econometric Policy Evaluation: A Critique," *Carnegie-Rochester*
- **Romer (2016)**, "The Trouble with Macroeconomics," *NYU Working Paper*
- **Blanchard (2018)**, "On the Future of Macroeconomic Models," *JEP* 32(1)

## Q1 2026-specific data sources

- **OECD AI Outlook 2025**
- **Stanford HAI AI Index Annual Report 2025**
- **EU AI Act** primary text + implementing regulations
- **US AI Executive Orders** + AISI publications
- **UK AI Safety Institute** model evaluation publications
- **NIST AI Risk Management Framework**
- **METR** AI capability evaluations
- **Apollo Research** model deception/scheming evaluations
- **Anthropic / OpenAI / DeepMind / Meta / xAI Responsible Scaling Policies**
  (primary sources)

## Aligned organizations / working-paper sources

For ongoing work in this space (where to look for new releases):

- **GovAI** (Centre for the Governance of AI, Oxford) — most directly aligned
- **Convergence Analysis** — already named in handoff; closest precursor on
  sovereign-AI-fund methodology
- **Centre for Long-term Resilience (CLTR, UK)**
- **Future Society** (Paris)
- **Collective Intelligence Project (CIP)** — already named in handoff
- **Brookings AI policy** (Korinek, Larrey, others)
- **CSET** (Georgetown) — China AI, compute, defense applications
- **CNAS** — defense/security framing
- **Carnegie Endowment AI policy** — geopolitical framing
- **RAND AI policy** — RDM-adjacent methodology
- **NBER AI working group**
- **Atlantic Council GeoTech Center** — already named in handoff

---

*Addendum end. Cross-referenced from `PREREGISTRATION.md` §2 (packages),
§3–5 (hypotheses), and from `BASELINE_2026.md` §2 (Q1 2026 shifts).*
