"""Shared helpers for BP computation scripts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSUMPTIONS_PATH = Path(__file__).resolve().parent / "assumptions.yaml"
DATA_DIR = ROOT / "data"
COMPUTED_DIR = DATA_DIR / "computed"


def load_assumptions() -> dict[str, Any]:
    with ASSUMPTIONS_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_computed_dir() -> Path:
    COMPUTED_DIR.mkdir(parents=True, exist_ok=True)
    return COMPUTED_DIR


def write_json(name: str, payload: dict[str, Any]) -> Path:
    ensure_computed_dir()
    path = COMPUTED_DIR / name
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def pct(x: float) -> str:
    return f"{x * 100:.2f}%"


def money_cny(x: float) -> str:
    return f"¥{x:,.0f}"
