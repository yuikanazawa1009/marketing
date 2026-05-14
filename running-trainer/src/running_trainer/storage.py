"""トレーニング計画のJSON永続化."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

DATA_FILE = Path.home() / ".running_trainer" / "plan.json"


@dataclass
class Workout:
    day: str  # ISO date "YYYY-MM-DD"
    type: str  # easy / interval / tempo / long / rest
    distance_km: float
    note: str = ""
    done: bool = False


@dataclass
class Plan:
    name: str
    goal: str = ""
    workouts: list[Workout] = field(default_factory=list)


def load() -> Plan | None:
    if not DATA_FILE.exists():
        return None
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return Plan(
        name=raw["name"],
        goal=raw.get("goal", ""),
        workouts=[Workout(**w) for w in raw.get("workouts", [])],
    )


def save(plan: Plan) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(asdict(plan), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def today_iso() -> str:
    return date.today().isoformat()
