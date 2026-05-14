"""集計とコンテキスト生成."""
from __future__ import annotations

from datetime import date, timedelta

from .db import connect


def _fmt_pace(s_per_km: float | None) -> str:
    if not s_per_km:
        return "-"
    m, s = divmod(int(s_per_km), 60)
    return f"{m}:{s:02d}/km"


def build_context(days: int = 28) -> str:
    """直近 `days` 日のトレーニング/コンディションをLLM向けテキストにまとめる."""
    end = date.today()
    start = end - timedelta(days=days)
    lines: list[str] = []
    lines.append(f"# 過去{days}日のサマリー ({start} 〜 {end})")

    with connect() as c:
        # アクティビティ集計
        acts = c.execute(
            "SELECT * FROM activities WHERE start_date >= ? AND type LIKE '%Run%' "
            "ORDER BY start_date",
            (start.isoformat(),),
        ).fetchall()
        total_km = sum((a["distance_km"] or 0) for a in acts)
        total_time_min = sum((a["moving_time_s"] or 0) for a in acts) / 60
        n = len(acts)
        lines.append(f"\n## ランニング集計")
        lines.append(f"- セッション数: {n}")
        lines.append(f"- 合計距離: {total_km:.1f} km")
        lines.append(f"- 合計時間: {total_time_min:.0f} 分")
        if n:
            lines.append(f"- 平均距離/回: {total_km / n:.1f} km")

        # 週次の積み上げ
        weekly: dict[str, float] = {}
        for a in acts:
            d = date.fromisoformat(a["start_date"])
            week_start = d - timedelta(days=d.weekday())
            weekly[week_start.isoformat()] = weekly.get(week_start.isoformat(), 0) + (a["distance_km"] or 0)
        if weekly:
            lines.append("\n## 週間距離")
            for wk in sorted(weekly):
                lines.append(f"- 週({wk}〜): {weekly[wk]:.1f} km")

        # 直近の主要セッション (最大10件)
        lines.append("\n## 直近セッション (最大10件)")
        for a in acts[-10:]:
            lines.append(
                f"- {a['start_date']}  {a['type']:<8} "
                f"{(a['distance_km'] or 0):.1f}km "
                f"{_fmt_pace(a['avg_pace_s_per_km'])} "
                f"HR avg={a['avg_hr'] or '-'} max={a['max_hr'] or '-'} "
                f"標高+{a['elevation_gain_m'] or 0:.0f}m"
            )

        # OURA メトリクス
        metrics = c.execute(
            "SELECT * FROM daily_metrics WHERE date >= ? ORDER BY date",
            (start.isoformat(),),
        ).fetchall()
        if metrics:
            def avg(key: str) -> float | None:
                vals = [m[key] for m in metrics if m[key] is not None]
                return sum(vals) / len(vals) if vals else None

            lines.append("\n## コンディション (OURA 平均)")
            ravg = avg("readiness_score")
            savg = avg("sleep_score")
            slpmin = avg("total_sleep_min")
            hrv = avg("hrv_ms")
            rhr = avg("resting_hr")
            if ravg: lines.append(f"- Readiness: {ravg:.0f}")
            if savg: lines.append(f"- Sleep score: {savg:.0f}")
            if slpmin: lines.append(f"- 睡眠時間: {slpmin/60:.1f} 時間")
            if hrv: lines.append(f"- HRV: {hrv:.0f} ms")
            if rhr: lines.append(f"- 安静時心拍: {rhr:.0f} bpm")

            lines.append("\n## 直近7日のコンディション推移")
            for m in metrics[-7:]:
                lines.append(
                    f"- {m['date']}  ready={m['readiness_score'] or '-'} "
                    f"sleep={m['sleep_score'] or '-'} "
                    f"HRV={m['hrv_ms'] or '-'} RHR={m['resting_hr'] or '-'}"
                )

    return "\n".join(lines)
