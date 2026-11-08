#!/usr/bin/env python3
"""Defense backend selector (PUBLIC repo) — the clean-room reference defense.

This public tree ships only the reference implementation of the pinning defense
(ref_defense.ReferenceDefense), re-derived from Chen (2026), arXiv:2606.22528.
It references no production or integration module.
"""
from ref_defense import ReferenceDefense as Defense, tamper_pin  # noqa: F401
