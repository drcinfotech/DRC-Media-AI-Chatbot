"""Data catalog - loads from JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


DATA_DIR = Path(__file__).parent.parent / "data"


class Catalog:
    def __init__(self):
        with open(DATA_DIR / "catalog.json", "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def titles(self) -> list[dict]:
        return list(self._data["titles"])

    def title(self, tid: str) -> Optional[dict]:
        for t in self._data["titles"]:
            if t["id"] == tid:
                return t
        return None

    def profiles(self) -> list[dict]:
        return list(self._data["profiles"])

    def profile(self, name: str) -> Optional[dict]:
        n = name.lower()
        for p in self._data["profiles"]:
            if p["name"].lower() == n:
                return p
        return None

    def watchlist(self) -> list[dict]:
        return list(self._data["watchlist"])

    def continue_watching(self) -> list[dict]:
        return list(self._data["continue_watching"])

    def downloads(self) -> list[dict]:
        return list(self._data["downloads"])

    def plans(self) -> list[dict]:
        return list(self._data["plans"])

    def plan(self, plan_id: str) -> Optional[dict]:
        for p in self._data["plans"]:
            if p["id"] == plan_id:
                return p
        return None

    def current_subscription(self) -> dict:
        return dict(self._data["current_subscription"])

    def devices(self) -> list[dict]:
        return list(self._data["devices"])


catalog = Catalog()
