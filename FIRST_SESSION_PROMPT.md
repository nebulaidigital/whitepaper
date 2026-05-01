# First Claude Code Session — Starter Prompt

Copy-paste this when you start your first Claude Code session in this repository.

---

## Prompt to paste

> Read `CLAUDE.md` completely before doing anything else. It contains the full project specification, working agreements, and known pitfalls from the prototype phase.
>
> Then read `ROADMAP.md` to understand the multi-session plan.
>
> Then read `paper/sections/peer_review_critique.md` for the methodological objections this simulation must address, and `SOURCES.md` for the literature anchors for every parameter.
>
> Then read the four prototype files in `prototype/` to understand the starting point. The production module (`s1_production.py`) and firms+labor module (`s2_firms_labor.py`) are validated and ready to port. The integrated dynamic model (`s4_integrated.py`) has known calibration failures documented in `CLAUDE.md`.
>
> For this first session, execute Session 1 of `ROADMAP.md`:
>
> 1. Set up the project environment (`uv` or `poetry`)
> 2. Initialize git, make the first commit ("Initial scaffolding from chat-session handoff")
> 3. Identify and document the actual download URLs for each dataset listed in `data/raw/README.md`
> 4. Download as many of the datasets as you can autonomously (BLS, WID, DLEU, Penn World Tables are public; SCF requires going through the Federal Reserve site but should be possible)
> 5. Create stub data loaders in `src/analysis/data_pipelines/` that read each into a pandas DataFrame
> 6. Run `pytest` (with no tests yet) just to confirm the test infrastructure works
> 7. Update `ROADMAP.md` with what was actually accomplished and what's deferred to Session 2
>
> Important constraints:
> - Don't try to do Session 2 work today. Stay disciplined.
> - Every parameter you encounter should be cited to the relevant entry in `SOURCES.md`. If you find a parameter that isn't in SOURCES.md, add it there before using it.
> - Commit at every meaningful step, not just at the end.
> - If you hit a problem you can't resolve in 30 minutes, document it in `ROADMAP.md` decisions log and move on.
>
> If you discover that any of the documentation in this handoff is wrong, incomplete, or inconsistent, fix it as you go. The handoff was produced under time pressure and is not perfect.

---

## What to expect

Session 1 is mostly mechanical setup work. The real economic modeling starts in Session 2 (porting validated modules) and Session 3 (the Piketty additions to the capital module).

If Claude Code finishes Session 1 quickly and asks if it should continue, say no — let it surface for your review before starting Session 2. The discipline of one focused task per session is what produces good work.

## After Session 1

Open `ROADMAP.md` and confirm the Session 1 status was honestly updated. If the data downloads partially failed, document which ones and why; you may need to acquire some manually.

The next session's prompt is, simply: "Execute Session 2 of `ROADMAP.md`. Read `CLAUDE.md` first if you haven't recently."
