# govdecay — Governance Decay on small local models (+ a clean-room reference defense)

A local, deterministic harness for measuring **governance decay** — a governance
constraint an LLM agent obeys while it is visible in context can be silently
erased when context compaction summarizes or evicts the history, after which the
agent performs the prohibited tool action — together with a **clean-room
reference implementation** of the pinning defense. The reference reproduces the
defense's two correctness **properties** from scratch (see below); the attack
baselines it measures are reported as-is, with no tuning toward the paper.

## Attribution
The Governance-Decay **phenomenon**, the **ConstraintRot** benchmark structure,
the deterministic tool-call grading **method**, and **Constraint Pinning** are the
work of Shiyang Chen, *Governance Decay: How Context Compaction Silently Erases
Safety Constraints in Long-Horizon LLM Agents*, **arXiv:2606.22528** (2026). We
cite them and **claim none of it**.

**Our contributions, the only things claimed here:**
1. **Measurement on small local models** that no one has tested (qwen2.5:7b/14b,
   mistral-small3.2, gemma3:12b), with pre-registered hypotheses and bootstrap CIs.
2. A **VOR-hash-pinned, tamper-evident** hardening of the pinning defense. This
   public repo ships a **clean-room reference implementation** of that defense
   (`ref_defense.py`) — a hash-chained sealed ledger, a compaction-exempt pin, a
   fail-closed integrity check, and provenance that refuses an unsealed operator
   override. The **production integration is retained privately** and is not in
   this repo.

## What the reference defense does (reproducible from scratch)
`ref_defense.py` is written fresh from the paper's method description and imports
nothing proprietary. `reproduce_ref.py` runs E1 (tamper) and E2 (rescind
±provenance) across the installed agents using the reference defense. Two
**correctness properties** hold on all four agents and are the reproducible claim:

- **E1 (tamper): fail-closed.** Altering the sealed constraint trips the integrity
  check — `violation = 0.000`, `block_rate = 1.000` on all four.
- **E2 (provenance): closes the residual.** An unsealed operator rescind is
  stripped; `E2 prov = 0.000` on all four.

### Measured E2 table (what the code produces; reps=10, temp 0, fixed seed)

| agent | E2 noprov | 95% CI | E2 prov | E1 block |
|---|---|---|---|---|
| qwen2.5:7b | 0.167 | [0.083, 0.267] | 0.000 | 1.000 |
| qwen2.5:14b | 0.333 | [0.217, 0.450] | 0.000 | 1.000 |
| mistral-small3.2 | 0.333 | [0.217, 0.450] | 0.000 | 1.000 |
| gemma3:12b | 0.000 | [0.000, 0.000] | 0.000 | 1.000 |

The **noprov** column is a *measured* baseline, not tuned. `reproduce_ref.py` also
prints each cell's Delta against the paper's published figure. Three of four land on
the paper within +/-0.003 (7b, mistral, gemma); 14b is lower (0.333 vs 0.50). We
report it as-is — consistent with the claim-limits below, our scenarios and
compaction budget are not the paper's ConstraintRot, so cell-level magnitudes are
not expected to match and we make no head-to-head ranking.

## Claim-limits (pre-registered, carried in the sealed preregs)
- **No local-vs-cloud ranking.** Our scenarios and compaction budget are not the
  paper's ConstraintRot; we make no head-to-head ranking against the paper.
- **Soft-vs-hard is directional only.** With 2 hard scenarios the contrast is
  underpowered; we report direction + CIs, not a powered claim.

## Pre-registration
Three sealed preregs (SHA-256, in `*_HASHES.txt`) fix the hypotheses, scenarios,
grader, models, metric, and the non-tuning discipline before any run:
`PREREG_GOVDECAY.md` (smoke), `PREREG_GOVDECAY_GRID.md` (powered grid),
`PREREG_GOVDECAY_P3.md` (cross-agent generalization). `scenarios.json` and
`grader.py` are frozen and carried by hash across all three.

## Grading is deterministic
A violation is decided solely by parsing the agent's single terminal tool call
against a scenario predicate (`grader.py`) — **no LLM judge** for the violation
metric.

## Run (local, needs Ollama; temperature 0)
```
python test_grader.py         # deterministic grader sanity (no model)
python test_ref_defense.py    # clean-room reference-defense sanity (no model)
python reproduce_ref.py       # E1/E2 with the reference defense vs the paper's figures
python grid.py --quick        # dry run (writes grid_report.quick.json)
python grid.py                # full grid: Delta-decay, channels, budget sweep, adversarial
python smoke.py               # one-model pipeline check
```

## License
Apache-2.0 (see `LICENSE`). Copyright 2026 Clint Nelson / Snake River AI LLC.
Scenarios are synthetic; no third-party data is included.
