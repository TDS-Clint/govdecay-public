#!/usr/bin/env python3
"""One-time repair for a grid_report.json contaminated by --quick (reps=1) cells.

Keeps only FULL-reps cells (n == reps * n_scenarios), migrates their keys to the
new reps-suffixed format, and drops every under-reps cell so the resumed grid
recomputes them. Run once, then re-run `python grid.py`.

  python purge_grid.py --reps 10
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--report", default=os.path.join(HERE, "grid_report.json"))
    args = ap.parse_args()

    if not os.path.exists(args.report):
        print("no report at %s — nothing to purge (a fresh run will be clean)" % args.report)
        return 0
    nscen = len(json.load(open(os.path.join(HERE, "scenarios.json")))["scenarios"])
    expected = args.reps * nscen
    report = json.load(open(args.report, encoding="utf-8"))
    cells = report.get("cells", {})

    kept, dropped = {}, []
    suffix = "|r%d" % args.reps
    for k, v in cells.items():
        if v.get("n") == expected:
            nk = k if k.endswith(suffix) else k + suffix
            kept[nk] = v
        else:
            dropped.append((k, v.get("n")))

    report["cells"] = kept
    tmp = args.report + ".tmp"
    json.dump(report, open(tmp, "w"), indent=2)
    os.replace(tmp, args.report)

    print("expected full-reps n = %d (reps=%d × %d scenarios)" % (expected, args.reps, nscen))
    print("KEPT  %d full-reps cell(s):" % len(kept))
    for k in sorted(kept):
        print("   %s  (n=%d)" % (k, kept[k]["n"]))
    print("DROPPED %d under-reps / contaminated cell(s):" % len(dropped))
    for k, n in sorted(dropped):
        print("   %s  (n=%s)" % (k, n))
    print("\nNow run:  python grid.py   (it will recompute the dropped cells at full reps)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
