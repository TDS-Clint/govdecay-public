# STEP 0 — Method confirmed from source

**Source read:** arXiv:2606.22528 v2 (abstract + full PDF, 2026), fetched directly.
Shiyang Chen, *Governance Decay: How Context Compaction Silently Erases Safety
Constraints in Long-Horizon LLM Agents*, Beijing Institute of Technology.
Method below is taken from the paper itself, not secondary summaries.

## Δdecay definition (verbatim intent from the PDF)
Δdecay = v(M, [C(H<t); r]) − v(M, [H<t; r])

- v(M, H) = probability model M performs a p-violating action given context H
- C = the compaction operator (summarize/evict older history)
- H<t = history before the trigger; r = the prohibited trigger request; p = policy
- i.e. the *increase* in violation probability caused by compacting the history.

## ConstraintRot episode structure
Each scenario is a single long-horizon agent session in three parts:
1. **policy turn** — establishes a governance constraint p
2. **benign task turns** — a long sequence that pushes context past the compaction budget
3. **trigger request** — whose natural completion violates p
The agent must emit a **single terminal tool call**. Paper's tools include
send_email, db_exec, read_file, disclose, purchase.

## Deterministic grading predicate (the violation metric)
The primary violation metric **parses the terminal tool call** and detects the
prohibited effect in the action arguments (e.g. a recipient outside the allowed
domain in send_email; a DROP/DELETE on a production target in db_exec). **No LLM
judge.** (The paper's *secondary* "survival" metric does use an LLM judge; we do
not use it for the violation metric — deterministic only, per dispatch.)

## Channels (constraint delivery)
system / user / memory / tool-output. Paper's channel test (3 models, 5 soft
tasks): decay ≈ **+0** when the policy sits in the **preserved system message**;
**+50 / +45 / +33** points for user / memory / tool-output respectively.

## Paper's headline numbers (THEIRS — cloud models, not a target for us)
- 0% violation with policy in full context → ~30% after compaction, up to 59% for some models.
- Constraint survives the summary → 0% violation; dropped → 38%.
- Decay ~8.3× larger for soft org policies than hard safety norms.
- "Constraint Pinning" (training-free) restores violation to 0% on their benchmark.
- Scale: 7 model families, 9 tasks (5 soft, 4 hard) × 3 reps = 1,323 episodes.
- A "Compaction-Eviction Attack" biases the summarizer into dropping a policy.

## What is theirs vs ours
- **Theirs (cite, claim none):** the Governance-Decay phenomenon, the ConstraintRot
  benchmark, the deterministic tool-call grading method, Constraint Pinning.
- **Ours (the contribution):** (1) measuring decay on **small local models** nobody
  has tested; (2) a **VOR-hash-pinned, tamper-evident** version of the pinning
  defense (pin sealed into a SHA-256 VOR ledger; post-compaction context
  integrity-checked against the hash; fail-closed if the pin is missing/altered).
