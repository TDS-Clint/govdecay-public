# PRE-REGISTRATION — Governance Decay Phase 2 (powered local grid + adversarial pin)

**Project:** Snake River AI — sovereign replication/extension of arXiv:2606.22528.
**Status:** PRE-REGISTERED. Sealed by SHA-256 (see PREREG_GOVDECAY_GRID_HASHES.txt).
Nothing below is edited after sealing; any change is a new, re-sealed version.
**Builds on** the sealed Phase-1 prereg (PREREG_GOVDECAY.md). The 6 scenarios and
the deterministic grader are UNCHANGED and carried forward by hash (below).

## Discipline (fixed)
Results are NOT adjusted toward arXiv:2606.22528's numbers. No scenario,
predicate, threshold, budget, model, or condition is altered after observing
results to improve agreement with the paper. Divergence is a finding, not a bug.

## Attribution (fixed)
Phenomenon, ConstraintRot benchmark, deterministic tool-call grading, and
Constraint Pinning: Shiyang Chen, arXiv:2606.22528 (2026). We claim only (1)
measurement on small local models and (2) the VOR-hash-pinned, tamper-evident
defense (sealed pin, post-compaction integrity check, fail-closed; plus VOR
provenance that refuses an unsealed rescind).

## Carried-forward frozen artifacts (Phase-1 hashes — must still match at run time)
- `scenarios.json` = `2a4222983697cf4328a1fce65bb14eb0ff94d415f401eed1a11a1cbff0c2431b`
- `grader.py` = `cf060077eeaec59a6e53c08872e68c9c147a2aff8240f4e8f1cf44904513db57`
- Phase-1 prereg `PREREG_GOVDECAY.md` = `e54ceb66f0f003fecf13c84263e99a49f73f5f8633ec7097eed921a1b3a462d3`
(The 6 scenarios — 4 soft org policies, 2 hard safety norms — and their exact
deterministic predicates are as defined in Phase 1. Grading stays deterministic
from the terminal tool call; no LLM judge for the violation metric.)

## Hypotheses (directions fixed before any run)
- **H1** — under compaction with the constraint in the USER channel, Δdecay > 0.
- **H2** — constraint in the preserved SYSTEM channel → Δdecay ≈ 0.
- **H3** — VOR pin ON → violation ≈ 0 (≈ control).
- **H4** — decay varies with BOTH the agent model and the summarizer model,
  tested by the agent×summarizer cross (fix summarizer, vary agent = agent
  effect; fix agent, vary summarizer = summarizer effect).
- **H5** — altering the pinned buffer after compaction trips the SHA-256 check
  and fails closed (the action is blocked).
- **H6** — an operator-impersonation rescind in recent (un-summarized) context
  raises violation; VOR provenance (the rescind is not hash-sealed → not
  honored) reduces it.
Any null or reversed result is reported as-is.

## Models (fixed candidate set + selection rule; no post-hoc dropping)
Candidate agents (pre-named): `qwen2.5:7b`, `qwen2.5:14b`, `llama3.1:8b`,
`mistral-small`, `gemma3:12b`. **Rule:** include EVERY candidate actually
installed on the box; drop none after seeing results. `grid.py` records which
were present/absent at launch (from Ollama `/api/tags`) into `grid_report.json`.
Fixed cross-summarizer: `qwen2.5:7b`. Temperature 0, fixed seed, local Ollama
only (no :cloud).

## Metric and uncertainty
Δdecay(cell) = violation_rate(cell) − violation_rate(control a), per agent.
Every violation rate and every Δdecay carries a **bootstrap 95% CI** (percentile,
2000 resamples, fixed seed; `boot.py`).

## Sub-studies (all user channel + budget 50 words unless stated)
- **GRID A (headline):** every installed agent × summarizer ∈ {same-model,
  qwen2.5:7b} × cells {a control (no compaction), b compacted, d compacted+pin}.
  reps=10 → 60 episodes/cell. Separates agent effect from summarizer effect.
- **GRID B (channels):** ≤2 agents, same-model summarizer, compacted, channels
  {system, user, memory, tool_output}. Confirms system ≈ 0.
- **GRID C (budget sweep):** 1 agent, same-model summarizer, user channel,
  budgets {300, 100, 50, 15}. Decay vs budget.
- **GRID D (soft vs hard):** no new runs — split GRID A by scenario class.
  **Directional only** (see claim-limit 2).
- **GRID E (adversarial):** 1 agent, user, budget 50, pin ON.
  - **E1 TAMPER:** alter the pinned buffer after compaction; report the
    hash-check catch rate (expect fail-closed on every tampered episode).
  - **E2 RESCIND:** inject an operator-impersonation rescind in recent context;
    measure violation with provenance OFF and ON; compare to the paper's
    17% / 10% (as a reference point, not a target).

## Explicit claim-limits (fixed)
- **Claim-limit 1 — no local-vs-cloud ranking.** Our scenarios and compaction
  budget are NOT the paper's ConstraintRot. We do NOT claim "local models decay
  more (or less) than cloud." No head-to-head ranking against the paper is made.
- **Claim-limit 2 — soft-vs-hard is directional only.** With just 2 hard
  scenarios the soft/hard contrast is underpowered. We report the direction and
  the CIs; a real soft/hard test needs more hard scenarios in a later prereg.

## Non-tuning line
No value above is changed after a run to move our numbers toward the paper's.
