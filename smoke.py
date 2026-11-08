#!/usr/bin/env python3
"""STEP 4 smoke run — ONE agent model, prove the pipeline (not the full grid).

Cells (constraint delivered, then the trigger fires):
  a) full-context, no compaction            (control; expect ~0 — "it's the compactor")
  b) compacted, constraint in USER channel   (expect decay > 0)
  c) compacted, constraint in SYSTEM channel (expect ~0 — system preserved)
  d) compacted, USER channel, PIN ON     (expect ~0 — the sovereign fix)

Delta_decay(cell) = violation_rate(cell) - violation_rate(a).

Run ON THE BOX (needs local Ollama):
  python smoke.py --agent qwen2.5:14b --summarizer qwen2.5:7b --budget 50 --reps 3
Results are NOT to be adjusted toward arXiv:2606.22528's cloud-model numbers.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runner import run_episode

HERE = os.path.dirname(os.path.abspath(__file__))

CELLS = [
    {"name": "a_full_context",   "channel": "user",   "compact_on": False, "pin_on": False},
    {"name": "b_compact_user",   "channel": "user",   "compact_on": True,  "pin_on": False},
    {"name": "c_compact_system", "channel": "system", "compact_on": True,  "pin_on": False},
    {"name": "d_compact_pin",    "channel": "user",   "compact_on": True,  "pin_on": True},
]


def rate(rows):
    return sum(1 for r in rows if r["violation"]) / len(rows) if rows else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="qwen2.5:14b")
    ap.add_argument("--summarizer", default="qwen2.5:7b")
    ap.add_argument("--budget", type=int, default=50, help="compaction word budget B")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--n-filler", type=int, default=12)
    ap.add_argument("--out", default=os.path.join(HERE, "smoke_report.json"))
    args = ap.parse_args()

    scenarios = json.load(open(os.path.join(HERE, "scenarios.json")))["scenarios"]
    ledger = os.path.join(HERE, "pin_ledger.jsonl")
    if os.path.exists(ledger):
        os.remove(ledger)

    all_rows = {c["name"]: [] for c in CELLS}
    pin_overhead = []
    for cell in CELLS:
        for sc in scenarios:
            for _ in range(args.reps):
                r = run_episode(sc, cell["channel"], args.budget, cell["pin_on"],
                                args.agent, args.summarizer, n_filler=args.n_filler,
                                compact_on=cell["compact_on"], ledger_path=ledger)
                all_rows[cell["name"]].append(r)
                if cell["pin_on"]:
                    pin_overhead.append(r["pin_overhead_words"])

    base = rate(all_rows["a_full_context"])
    summary = {
        "agent_model": args.agent, "summarizer_model": args.summarizer,
        "budget_words": args.budget, "reps": args.reps,
        "episodes_per_cell": len(scenarios) * args.reps,
        "ts": time.time(), "cells": {}, "delta_decay": {},
        "pin_overhead_words_mean": (sum(pin_overhead) / len(pin_overhead)) if pin_overhead else 0,
    }
    for c in CELLS:
        vr = rate(all_rows[c["name"]])
        summary["cells"][c["name"]] = {"violation_rate": vr, "n": len(all_rows[c["name"]])}
        summary["delta_decay"][c["name"]] = round(vr - base, 4)

    json.dump({"summary": summary, "rows": all_rows}, open(args.out, "w"), indent=2)

    print("=== GOVERNANCE-DECAY SMOKE (%s) ===" % args.agent)
    print("budget=%d words, reps=%d, %d episodes/cell\n" % (args.budget, args.reps, summary["episodes_per_cell"]))
    for c in CELLS:
        cn = c["name"]
        print("  %-18s violation=%.3f   Delta_decay=%+.3f" %
              (cn, summary["cells"][cn]["violation_rate"], summary["delta_decay"][cn]))
    print("\n  pin overhead (mean words): %.0f" % summary["pin_overhead_words_mean"])
    print("  report: %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
