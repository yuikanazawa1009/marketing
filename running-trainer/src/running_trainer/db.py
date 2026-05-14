"""SQLite schema & helpers."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path.home() / ".running_trainer" / "data.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS activities (
    id               TEXT PRIMARY KEY,    -- "<source>:<external_id>"
    source           TEXT NOT NULL,
    start_date       TEXT NOT NULL,        -- ISO date YYYY-MM-DD
    start_datetime   TEXT NOT NULL,        -- ISO 8601
    type             TEXT,
    name             TEXT,
    distance_km      REAL,
    moving_time_s    INTEGER,
    elapsed_time_s   INTEGER,
    elevation_gain_m REAL,
    avg_hr           REAL,
    max_hr           REAL,
    avg_pace_s_per_km REAL,
    suffer_score     REAL,
    raw_json         TEXT
);
CREATE INDEX IF NOT EXISTS idx_activities_date ON activities(start_date);

CREATE TABLE IF NOT EXISTS daily_metrics (
    date             TEXT PRIMARY KEY,     -- YYYY-MM-DD
    readiness_score  INTEGER,
    sleep_score      INTEGER,
    total_sleep_min  INTEGER,
    hrv_ms           REAL,
    resting_hr       INTEGER,
    body_temp_delta  REAL,
    raw_json         TEXT
);

CREATE TABLE IF NOT EXISTS config (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""


@contextmanager
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def get_config(key: str) -> str | None:
    with connect() as c:
        row = c.execute("SELECT value FROM config WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None


def set_config(key: str, value: str) -> None:
    with connect() as c:
        c.execute(
            "INSERT INTO config(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


def upsert_activity(row: dict) -> None:
    cols = list(row.keys())
    placeholders = ",".join("?" for _ in cols)
    updates = ",".join(f"{c}=excluded.{c}" for c in cols if c != "id")
    sql = (
        f"INSERT INTO activities ({','.join(cols)}) VALUES ({placeholders}) "
        f"ON CONFLICT(id) DO UPDATE SET {updates}"
    )
    with connect() as c:
        c.execute(sql, [row[c_] for c_ in cols])


def upsert_daily_metric(row: dict) -> None:
    cols = list(row.keys())
    placeholders = ",".join("?" for _ in cols)
    updates = ",".join(f"{c}=excluded.{c}" for c in cols if c != "date")
    sql = (
        f"INSERT INTO daily_metrics ({','.join(cols)}) VALUES ({placeholders}) "
        f"ON CONFLICT(date) DO UPDATE SET {updates}"
    )
    with connect() as c:
        c.execute(sql, [row[c_] for c_ in cols])
