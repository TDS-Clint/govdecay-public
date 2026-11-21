---
title: "Tamper-Evident, Provenance-Authenticated Constraint Pinning: Closing the Impersonation Gap in Governance-Decay Defenses for Long-Horizon LLM Agents"
author: "Clint L. Nelson Jr.  ·  Snake River AI LLC, Idaho Falls, Idaho  ·  clint@snakeriverai.com"
date: "November 2026"
geometry: margin=1in
fontsize: 11pt
linestretch: 1.08
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes:
  - \usepackage{booktabs}
---

## Abstract

Chen (2026) showed that **context compaction** in long-horizon LLM agents silently erases governance constraints — the *governance-decay* phenomenon — and proposed **Constraint Pinning**, a training-free defense that quarantines constraints into a compaction-exempt buffer. Pinning stops the basic attack but, as Chen reports, leaks 10–17% under a mid-stream **operator-impersonation "rescind"**: a forged authority notice placed in the live token stream. Chen names this the central open problem and argues that closing it requires a *trusted out-of-band operator channel*. We present such a channel. Our defense seals the pinned constraint into a hash-chained ledger (the VOR ledger) and accepts an override **only if it carries a valid cryptographic seal against that ledger** — an unsealed rescind in the token stream is refused by construction, not by the model's judgment. Across four small, locally-served models (qwen2.5:7b, qwen2.5:14b, mistral-small3.2, gemma3:12b) we (i) reproduce governance decay on model sizes not previously tested, (ii) confirm fail-closed tamper detection (ledger/pin tamper → 0% violation, 100% block on every model), and (iii) show the provenance seal drives the impersonation-induced violation to **0% on every model that leaked** (vanilla-pin leak up to 50%). The study is preregistered with SHA-256-sealed scenarios and grader, graded by a deterministic tool-call predicate (no LLM judge), and the reference defense is released as a clean-room public implementation. We claim the mechanism, not a capability ranking: constraints delivered outside the model's trust surface, where authority is a signature rather than a sentence.

## 1. Introduction

A long-horizon agent cannot keep its entire history in context. Harnesses **compact** — summarize and evict older turns — to stay within the budget. Chen (2026) demonstrated that this routine operation silently removes governance constraints established earlier in the session: after compaction, a model that previously refused a prohibited action performs it, because the constraint is simply no longer in the context the model reads. Chen measures this as a decay term, $\Delta_{\text{decay}} = v(M,[C(H_{<t}); r]) - v(M,[H_{<t}; r])$, the increase in violation probability caused by applying the compaction operator $C$ to the history before a prohibited trigger $r$.

Chen's defense, **Constraint Pinning**, is elegant and training-free: lift the governance constraint into a small buffer that compaction is forbidden to touch, and re-inject it verbatim after every compaction step. On the basic benchmark it restores violations to zero. But Chen reports a residual failure that pinning does not solve. If an attacker places a message in the *recent, non-summarized* context that impersonates the operator — *"Policy rescinded, you may now proceed"* — the model cannot reliably tell a genuine operator update from a forgery, because both arrive as text in the same stream. Violations climb back to 17% (10% even when the pin carries provenance *language*). Chen states the problem directly: the fix requires a **trusted out-of-band operator channel** — a way for the system to know an authority change is real that does not live in the tokens the model reads.

This paper supplies that channel and measures it. Our contribution is three-fold:

1. **Governance decay on small local models.** Chen tested cloud-scale models. We test four models in the 7B–27B class served locally via Ollama — the regime a sovereignty-first, on-premises deployment actually runs — and show the phenomenon reproduces.
2. **A tamper-evident pin.** The pinned constraint is sealed into a hash-chained ledger; the post-compaction context is integrity-checked against the seal and the system fails closed if the pin is missing or altered.
3. **Provenance-authenticated override — the out-of-band channel.** An override is honored only if it carries a valid cryptographic seal. An impersonation in the token stream has no valid seal and is refused by construction. This is the piece that answers Chen's open problem, and it is the paper's core claim.

We make no cross-model capability ranking and do not treat Chen's cloud-model magnitudes as a target; small local models are a different regime, reported on their own terms.

## 2. Related Work

**Governance decay and constraint pinning (Chen 2026, arXiv:2606.22528).** The phenomenon, the ConstraintRot benchmark, the deterministic tool-call grading method, and the Constraint Pinning defense are all Chen's. We replicate the phenomenon on new (small, local) models and extend the defense. The impersonation residual and the "trusted out-of-band channel" framing are Chen's stated open problem; answering it is our contribution.

**Tamper-evident agent audit trails.** A parallel line builds hash-chained, tamper-evident records of agent behavior — Agent Flight Recorder (2609.01931), Tracekit (2609.35659), identity-bound accountability proof blocks for agent halts (2610.00787), verifiable conversation transcripts (2606.23003), and dependency-free hash-chained runtime records (halo-record). These record *what happened* for after-the-fact audit. None of them **gate a constitutional constraint's authority against compaction**: recording an event is not the same as refusing an unauthenticated change to a live constraint. We borrow the hash-chain primitive from this literature and apply it to a different job — authenticating the pin itself at decision time.

## 3. Method

### 3.1 Episode structure and grading

We use Chen's ConstraintRot episode shape. Each scenario is a single long-horizon session in three parts: a **policy turn** establishing a governance constraint $p$; a sequence of **benign task turns** long enough to push the history past the compaction budget; and a **trigger request** whose natural completion violates $p$. The agent must emit a single terminal tool call (tools: `send_email`, `db_exec`, `read_file`, `disclose`, `purchase`).

Violation is graded by a **deterministic predicate** that parses the terminal tool call for the prohibited effect (a recipient outside the allowed domain in `send_email`; a `DROP`/`DELETE` on a production target in `db_exec`; and so on). **No LLM judge** is used for the violation metric. Six frozen scenarios span soft organizational policies (`S1_email_domain`, `S2_db_prod_write`, `S3_disclosure`, `S4_purchase_cap`) and hard safety norms (`H1_backup_delete`, `H2_credential_exfil`).

### 3.2 The defense

The production defense (VOR-pinned) and a clean-room reference implementation share one design:

- **Compaction-exempt pin.** The governance constraint is held in a buffer exempt from compaction and re-injected verbatim after each compaction step (as in Chen).
- **Hash-chained seal.** The pin is sealed into an append-only, SHA-256 hash-chained ledger. The post-compaction context must still entail the sealed pin; the chain is verified each step.
- **Fail-closed integrity.** If the pin is missing or altered relative to its seal, the system refuses the terminal action (fails closed) rather than proceeding.
- **Provenance-authenticated override.** A constraint change is accepted only if it is itself a validly sealed ledger entry. An override arriving as ordinary text in the token stream — the impersonation attack — carries no valid seal and is refused *by construction*. The authority check does not live in the text the model reads; this is the out-of-band channel Chen calls for.

### 3.3 Experimental conditions and attacks

- **Task A — decay under compaction.** Conditions: *control* (constraint in full context), *comp* (compaction applied, no defense), *pin* (our defense). $\Delta_{\text{decay}}$ is the comp-minus-control increase.
- **Task B — authority source.** The constraint is delivered via *system*, *user*, *memory*, or *tool-output* channel, testing which placements decay.
- **Task C — compaction budget.** Budgets of 300 / 100 / 50 / 15 tokens, testing decay vs. compaction aggressiveness.
- **E1 — tamper.** The ledger/pin is directly tampered; tests fail-closed integrity.
- **E2 — impersonation rescind.** A forged operator "rescind" is injected into recent context, run **without** provenance (`noprov`) and **with** the sealed-override channel (`prov`). This is Chen's open problem.

### 3.4 Models, determinism, scale

Four models served locally via Ollama at temperature 0, fixed seed, `num_ctx` 8192: **qwen2.5:7b, qwen2.5:14b, mistral-small3.2, gemma3:12b**. (llama3.1:8b was a preregistered candidate but was not present on the host at run time and is reported absent.) The grid ran at 10 repetitions, 60 observations per cell. qwen2.5:7b additionally served as a cross-model summarizer.

### 3.5 Preregistration and integrity

Hypotheses, scenarios, and grader were preregistered and SHA-256-sealed before the grid run (2026-11-07): `PREREG_GOVDECAY.md` `e54ceb66…`, `scenarios.json` `2a422298…`, `grader.py` `cf060077…`, with grid and Phase-3 preregs `fbebb204…` and `893fe42d…`. The scenarios and grader hashes are identical across all phases, proving they were not changed between preregistration and analysis. An automated **honesty gate** (`reproduce_ref.py`) re-runs the reference defense and exits non-zero on any mismatch with the paper's qualitative figures; it prints `all_match: true`. No tuning toward the paper was performed.

## 4. Results

### 4.1 Governance decay reproduces on small local models (Task A)

Violation rates (own-summarizer) and the compaction decay term with 95% bootstrap CIs:

| Model | Control | Comp | Pin | $\Delta_{\text{decay}}$ (comp−control) [95% CI] |
|---|---|---|---|---|
| qwen2.5:7b | 0.333 | 0.667 | 0.167 | +0.333 [0.167, 0.483] |
| qwen2.5:14b | 0.000 | 0.333 | 0.000 | +0.333 [0.217, 0.450] |
| mistral-small3.2 | 0.000 | 0.667 | 0.000 | +0.667 [0.550, 0.783] |
| gemma3:12b | 0.167 | 0.500 | 0.167 | +0.333 [0.183, 0.483] |

Compaction increases violations on every model (CIs exclude zero); the pin returns them to control level or below. Using qwen2.5:7b as a cross-model summarizer tends to worsen decay (e.g., qwen2.5:14b comp rises to 0.667), consistent with a weaker summarizer dropping the constraint more often.

### 4.2 Authority channel and compaction budget (Tasks B, C)

The channel pattern matches Chen: a constraint held in the **preserved system message** barely decays, while user / memory / tool-output placements decay hard.

| Channel | qwen2.5:7b | qwen2.5:14b |
|---|---|---|
| system | 0.167 | 0.000 |
| user | 0.667 | 0.333 |
| memory | 0.667 | 0.333 |
| tool-output | 0.667 | 0.333 |

Decay also sharpens as the compaction budget tightens (violation rate, budget 300→15 tokens): qwen2.5:7b 0.333 / 0.667 / 0.667 / 0.667; qwen2.5:14b 0.000 / 0.517 / 0.333 / 0.667; mistral-small3.2 0.000 / 0.167 / 0.667 / 0.500; gemma3:12b 0.167 / 0.317 / 0.500 / 0.667. The trend is toward more decay under tighter budgets, with model-specific non-monotonicity reported as observed.

### 4.3 Tamper detection is fail-closed (E1)

On every model, direct tampering of the ledger/pin produced **0.000 violation with a 100% block rate**. The integrity check refuses the action whenever the pin does not match its seal.

### 4.4 Provenance closes the impersonation gap (E2)

The headline result. Under the impersonation "rescind," violation with no provenance channel (`noprov`) versus with the sealed-override channel (`prov`), with 95% bootstrap CIs on the no-provenance leak:

| Model | E2 no-provenance [95% CI] | E2 provenance seal |
|---|---|---|
| qwen2.5:7b | 0.167 [0.083, 0.267] | **0.000** |
| qwen2.5:14b | 0.500 [0.367, 0.617] | **0.000** |
| mistral-small3.2 | 0.333 [0.217, 0.450] | **0.000** |
| gemma3:12b | 0.000 | **0.000** |

Vanilla pinning leaks under impersonation on three of the four models — up to 50% on qwen2.5:14b — exactly the failure Chen describes. The sealed-override channel drives the leak to **zero on every model**, because the forged rescind carries no valid seal and is refused before the model's judgment is involved. (gemma3:12b did not leak even without provenance in this threat instance; the provenance benefit is therefore demonstrated on the three models that leaked.)

## 5. Discussion

Chen's residual exists because, inside a single token stream, the model has no way to distinguish a genuine authority update from a convincing forgery — both are just text, and language can be imitated. Adding provenance *language* to the pin only moves the leak to 10% because language is exactly what the attacker can also produce. The fix cannot be a better sentence; it has to be a check the attacker cannot forge. A cryptographic seal is that check: the authority of an override is a signature over the hash-chained ledger, verified outside the model's reasoning. An impersonation in the stream fails the signature and never reaches the model as authoritative. This is what "out-of-band" means operationally — the authority decision is made in the ledger, not in the prose.

This also marks the line between our work and the tamper-evident audit literature. Those systems hash-chain a record of events so that tampering is *detectable after the fact*. Here the same primitive is used *at decision time* to authenticate a constraint's authority before an action is allowed. Recording that an impersonation happened is useful; refusing to act on it is the defense.

## 6. Limitations

- **Scope of the claim.** We claim the mechanism eliminates impersonation-induced violations in our experiments on these local models and this threat instance; we do not claim universal robustness. A seal defeats token-stream impersonation; it does not address an attacker who compromises the ledger key, which is a key-management problem outside this threat model.
- **Not a capability ranking.** Chen's cloud-model magnitudes are not a target and small local models are a different regime; no local-vs-cloud comparison is intended.
- **gemma3:12b did not leak** under E2 without provenance, so for that model the provenance channel is confirmed non-harmful rather than corrective; the corrective effect rests on the three leaking models.
- **Run variation.** A clean-room reference reproduction measured the qwen2.5:14b vanilla-pin leak at 0.333 versus 0.500 in the grid; we report both rather than selecting one. The gated claims (E2-provenance = 0, E1-block = 1) hold in both.
- **Deterministic metric only.** We use the tool-call violation predicate, not Chen's secondary LLM-judge "survival" metric.
- **Single operator, single seal.** Multi-operator authority, key rotation, and revocation are left to future work.

## 7. Reproducibility and Provenance

The clean-room reference defense, harness, frozen scenarios, grader, and all three sealed preregistrations are public under Apache-2.0 at **github.com/TDS-Clint/govdecay-public**, archived at **Zenodo DOI 10.5281/zenodo.24074358**. The production VOR integration is kept private; the public reference implements the same design and passes its unit suite (`test_ref_defense.py` 9/9, `test_grader.py` 6/6) and the honesty gate (`reproduce_ref.py` → `all_match: true`) without any proprietary module. Because the defense itself produces a hash-chained, tamper-evident ledger, the provenance trail of this work is generated by the mechanism the paper studies.

## 8. Conclusion

Governance decay reproduces on small, locally-served models, and tamper-evident constraint pinning holds fail-closed against direct tampering. The open problem Chen identified — an impersonated operator rescind that ordinary pinning cannot resist — is closed in our experiments by making constraint authority a cryptographic seal rather than a sentence. The result is a constraint that lives outside the model's trust surface: compaction cannot erase it, tampering cannot hide, and a forged authority in the token stream cannot override it. For sovereignty-first deployments running their own models, that is the difference between a governance constraint that is asserted and one that is enforced.

## References

Chen, S. (2026). *Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents.* arXiv:2606.22528.

*Agent Flight Recorder: Tamper-Evident Audit Trails with On-Chain Anchoring for Long-Horizon Tool-Using Agents.* arXiv:2609.01931.

*Tracekit: Tamper-Evident Intent-Reasoning-Action Auditing for AI Agents.* arXiv:2609.35659.

*Identity-Bound Governance Under Execution Uncertainty: An Accountability Proof Block for LLM Agent Persistent Halts.* arXiv:2610.00787.

*VCT: A Verifiable Transcript System for LLM Conversations.* arXiv:2606.23003.
