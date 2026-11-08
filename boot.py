#!/usr/bin/env python3
"""Percentile bootstrap CIs — pure stdlib, fixed seed, reproducible.

Self-contained (no cross-repo import). Used for a 95% CI on every violation
rate and every Delta_decay in the grid.
"""
import random

B_DEFAULT = 2000
SEED = 7


def ci_rate(flags, B=B_DEFAULT, alpha=0.05, seed=SEED):
    """Bootstrap 95% CI for a proportion. flags: list of 0/1.
    Returns (point, lo, hi)."""
    n = len(flags)
    if n == 0:
        return 0.0, 0.0, 0.0
    point = sum(flags) / n
    rng = random.Random(seed)
    means = []
    for _ in range(B):
        s = sum(flags[rng.randrange(n)] for _ in range(n))
        means.append(s / n)
    means.sort()
    lo = means[int((alpha / 2) * B)]
    hi = means[min(B - 1, int((1 - alpha / 2) * B))]
    return point, lo, hi


def ci_diff(flags_cell, flags_control, B=B_DEFAULT, alpha=0.05, seed=SEED):
    """Bootstrap 95% CI for Delta = rate(cell) - rate(control).
    Returns (delta_point, lo, hi)."""
    nc, n0 = len(flags_cell), len(flags_control)
    if nc == 0 or n0 == 0:
        return 0.0, 0.0, 0.0
    point = sum(flags_cell) / nc - sum(flags_control) / n0
    rng = random.Random(seed)
    diffs = []
    for _ in range(B):
        a = sum(flags_cell[rng.randrange(nc)] for _ in range(nc)) / nc
        b = sum(flags_control[rng.randrange(n0)] for _ in range(n0)) / n0
        diffs.append(a - b)
    diffs.sort()
    lo = diffs[int((alpha / 2) * B)]
    hi = diffs[min(B - 1, int((1 - alpha / 2) * B))]
    return point, lo, hi


def fmt(triple):
    p, lo, hi = triple
    return "%.3f [%.3f, %.3f]" % (p, lo, hi)
