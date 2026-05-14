"""OURA Ring API v2 client (personal access token)."""
from __future__ import annotations

import json
from datetime import date, timedelta

import requests

from ..db import get_config, upsert_daily_metric

BASE = "https://api.ouraring.com/v2/usercollection"


def _headers() -> dict:
    token = get_config("oura_token")
    if not token:
        raise RuntimeError("OURAトークン未設定。`running-trainer auth oura --token ...` を実行してください。")
    return {"Authorization": f"Bearer {token}"}


def _get(path: str, params: dict) -> dict:
    r = requests.get(f"{BASE}/{path}", headers=_headers(), params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def sync(days: int = 30) -> int:
    end = date.today()
    start = end - timedelta(days=days)
    params = {"start_date": start.isoformat(), "end_date": end.isoformat()}

    readiness = {d["day"]: d for d in _get("daily_readiness", params).get("data", [])}
    sleep = {d["day"]: d for d in _get("daily_sleep", params).get("data", [])}
    sleep_detail = {d["day"]: d for d in _get("sleep", params).get("data", [])}

    days_seen = set(readiness) | set(sleep) | set(sleep_detail)
    for day in sorted(days_seen):
        r = readiness.get(day, {})
        s = sleep.get(day, {})
        sd = sleep_detail.get(day, {})
        contrib = r.get("contributors", {}) or {}
        upsert_daily_metric(
            {
                "date": day,
                "readiness_score": r.get("score"),
                "sleep_score": s.get("score"),
                "total_sleep_min": (sd.get("total_sleep_duration") or 0) // 60 or None,
                "hrv_ms": sd.get("average_hrv"),
                "resting_hr": sd.get("lowest_heart_rate") or contrib.get("resting_heart_rate"),
                "body_temp_delta": r.get("temperature_deviation"),
                "raw_json": json.dumps({"readiness": r, "sleep": s, "sleep_detail": sd}, ensure_ascii=False),
            }
        )
    return len(days_seen)
