#!/usr/bin/env python3
"""Minimal local Ollama chat client. Local only — http://127.0.0.1:11434.

Temperature 0 for reproducibility. No cloud, no other host.
"""
import json
import urllib.request

OLLAMA = "http://127.0.0.1:11434"


def chat(model, messages, temperature=0.0, timeout=180):
    """messages: [{"role": "system"|"user"|"assistant", "content": "..."}].
    Returns the assistant text. Deterministic (temp 0, fixed seed)."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "seed": 7, "num_ctx": 8192},
    }
    req = urllib.request.Request(
        OLLAMA + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        obj = json.loads(r.read().decode("utf-8"))
    return obj["message"]["content"]


def word_count(text):
    return len(str(text).split())
