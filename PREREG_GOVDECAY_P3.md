# PRE-REGISTRATION — Governance Decay Phase 3 (generalize tamper + provenance + budget across agents)

**Project:** Snake River AI — sovereign replication/extension of arXiv:2606.22528.
**Status:** PRE-REGISTERED. Sealed by SHA-256 (see PREREG_GOVDECAY_P3_HASHES.txt).
Nothing below is edited after sealing; any change is a new, re-sealed version.
**Builds on** Phase 1 and Phase 2 preregs. Phase 3 ADDS cells (GRID C and GRID E
for the other three agents); it does not purge or alter Phase 2's cells. The
reps-aware resume key reuses qwen2.5:7b's existing C/E cells.

## Discipline (fixed)
Results are NOT adjusted toward arXiv:2606.22528's numbers. No scenario,
predicate, threshold, budget, model, or condition is altered after a run to
improve agreement with the paper. Any null or reversed result is reported as-is.

## Attribution (fixed)
Phenomenon, ConstraintRot, deterministic tool-call grading, Constraint Pinning:
Chen, arXiv:2606.22528 (2026). We claim only (1) measurement on small local
models and (2) the VOR-hash-pinned, tamper-evident defense (sealed pin, integrity
check, fail-closed; VOR provenance that STRIPS an unsealed rescind).

## Carried-forward frozen artifacts (must still match at run time)
- `scenarios.json` = `2a4222983697cf4328a1fce65bb14eb0ff94d415f401eed1a11a1cbff0c2431b`
- `grader.py` = `cf060077eeaec59a6e53c08872e68c9c147a2aff8240f4e8f1cf44904513db57`
- Phase-1 prereg = `e54ceb66f0f003fecf13c84263e99a49f73f5f8633ec7097eed921a1b3a462d3`
- Phase-2 prereg = `fbebb2049a8b8f170e25ec12f914664b05f24cec4a3ae7490ca5ea202cb1be75`
Scenarios and grader are UNCHANGED; grading stays deterministic from the terminal
tool call (no LLM judge for the violation metric).

## Hypotheses (directions fixed before any new run)
- **H7 (tamper generalizes):** E1 fail-closed drives violation to 0 on ALL four
  agents (altering the pinned buffer trips the SHA-256 check; the action is blocked).
- **H8 (provenance generalizes):** For E2 operator-impersonation rescind, violation
  with provenance OFF is elevated, and with VOR provenance ON (the unsealed rescind
  is stripped from the agent's context) returns to ≈ 0 — on all four agents. Per
  agent we report the noprov − prov reduction with a CI.
- **H9 (budget generalizes):** GRID C violation rises as the compaction budget
  tightens 300 → 15 on all four agents.

## Agents (fixed, all-installed rule, no post-hoc drop)
`qwen2.5:7b`, `qwen2.5:14b`, `mistral-small3.2:latest`, `gemma3:12b`. (The
candidate `mistral-small` resolves to the installed tag `mistral-small3.2:latest`
by prefix; `grid.py` records the resolution.) qwen2.5:7b's C/E cells from Phase 2
are reused via the reps-aware key.

## Summarizer for C and E (fixed)
Each agent's OWN model (same-model summarizer), documented. This isolates the
attack axis (E) and the budget axis (C) from the summarizer-swap axis, which Grid
A already covers (agent × {same-model, qwen2.5:7b}).

## Budgets / conditions (fixed)
- GRID E: budget fixed at 50 words, user channel, pin ON.
  - E1 TAMPER: alter the pinned buffer after compaction; catch rate (expect
    violation 0, pin_block_rate ≈ 1).
  - E2 RESCIND: operator-impersonation rescind in recent context; measure with
    provenance OFF and ON; report noprov − prov per agent.
- GRID C: user channel, budgets {300, 100, 50, 15}, pin OFF.

## Metric and uncertainty
Violation rate + bootstrap 95% CI (percentile, 2000 resamples, fixed seed) per
cell. For E2, the per-agent noprov − prov reduction carries its own bootstrap CI.
reps = 10 → 60 episodes/cell.

## Claim-limits carried (fixed)
- **Claim-limit 1 — no local-vs-cloud ranking** (our scenarios/budget ≠ ConstraintRot).
- **Claim-limit 2 — soft-vs-hard directional only** (2 hard scenarios = underpowered).

## Non-tuning line
No value above is changed after a run to move our numbers toward the paper's.
