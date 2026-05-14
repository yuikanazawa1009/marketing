"""Strava API client with OAuth2 refresh-token flow."""
from __future__ import annotations

import json
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import requests

from ..db import get_config, set_config, upsert_activity

AUTH_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"
API = "https://www.strava.com/api/v3"


def authorize_url(client_id: str) -> str:
    return AUTH_URL + "?" + urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": "http://localhost/exchange_token",
            "approval_prompt": "auto",
            "scope": "read,activity:read_all,profile:read_all",
        }
    )


def exchange_code(client_id: str, client_secret: str, code: str) -> dict:
    r = requests.post(
        TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def _refresh_access_token() -> str:
    client_id = get_config("strava_client_id")
    client_secret = get_config("strava_client_secret")
    refresh_token = get_config("strava_refresh_token")
    expires_at = int(get_config("strava_expires_at") or "0")
    access_token = get_config("strava_access_token")
    if access_token and expires_at - 60 > int(time.time()):
        return access_token
    if not (client_id and client_secret and refresh_token):
        raise RuntimeError("Strava認証情報が未設定です。`running-trainer auth strava` を実行してください。")
    r = requests.post(
        TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=30,
    )
    r.raise_for_status()
    tok = r.json()
    set_config("strava_access_token", tok["access_token"])
    set_config("strava_refresh_token", tok["refresh_token"])
    set_config("strava_expires_at", str(tok["expires_at"]))
    return tok["access_token"]


def save_initial_tokens(client_id: str, client_secret: str, tok: dict) -> None:
    set_config("strava_client_id", client_id)
    set_config("strava_client_secret", client_secret)
    set_config("strava_access_token", tok["access_token"])
    set_config("strava_refresh_token", tok["refresh_token"])
    set_config("strava_expires_at", str(tok["expires_at"]))


def sync(days: int = 60) -> int:
    token = _refresh_access_token()
    after = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp())
    page = 1
    count = 0
    while True:
        r = requests.get(
            f"{API}/athlete/activities",
            headers={"Authorization": f"Bearer {token}"},
            params={"after": after, "per_page": 200, "page": page},
            timeout=30,
        )
        r.raise_for_status()
        items = r.json()
        if not items:
            break
        for a in items:
            moving = a.get("moving_time") or 0
            dist = (a.get("distance") or 0) / 1000.0
            avg_pace = (moving / dist) if dist > 0 else None
            start_dt = a.get("start_date_local") or a.get("start_date") or ""
            upsert_activity(
                {
                    "id": f"strava:{a['id']}",
                    "source": "strava",
                    "start_date": start_dt[:10],
                    "start_datetime": start_dt,
                    "type": a.get("sport_type") or a.get("type"),
                    "name": a.get("name"),
                    "distance_km": round(dist, 3),
                    "moving_time_s": moving,
                    "elapsed_time_s": a.get("elapsed_time"),
                    "elevation_gain_m": a.get("total_elevation_gain"),
                    "avg_hr": a.get("average_heartrate"),
                    "max_hr": a.get("max_heartrate"),
                    "avg_pace_s_per_km": avg_pace,
                    "suffer_score": a.get("suffer_score"),
                    "raw_json": json.dumps(a, ensure_ascii=False),
                }
            )
            count += 1
        page += 1
    return count
