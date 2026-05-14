"""running-trainer CLI."""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta

from .storage import DATA_FILE, Plan, Workout, load, save, today_iso
from .db import set_config
from .sources import oura as oura_src
from .sources import strava as strava_src
from .summary import build_context
from .advisor import chat as advisor_chat


def cmd_init(args: argparse.Namespace) -> int:
    plan = Plan(name=args.name, goal=args.goal or "")
    save(plan)
    print(f"作成しました: {plan.name} ({DATA_FILE})")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    plan = load()
    if plan is None:
        print("プランがありません。先に `running-trainer init` を実行してください。", file=sys.stderr)
        return 1
    plan.workouts.append(
        Workout(day=args.day, type=args.type, distance_km=args.km, note=args.note or "")
    )
    plan.workouts.sort(key=lambda w: w.day)
    save(plan)
    print(f"追加: {args.day} {args.type} {args.km}km")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    plan = load()
    if plan is None:
        print("プランがありません。", file=sys.stderr)
        return 1
    print(f"# {plan.name}" + (f" — 目標: {plan.goal}" if plan.goal else ""))
    if not plan.workouts:
        print("(メニューなし)")
        return 0
    upcoming_only = args.upcoming
    today = today_iso()
    total = 0.0
    for w in plan.workouts:
        if upcoming_only and w.day < today:
            continue
        mark = "[x]" if w.done else "[ ]"
        line = f"{mark} {w.day}  {w.type:<8} {w.distance_km:>5.1f}km"
        if w.note:
            line += f"  // {w.note}"
        print(line)
        total += w.distance_km
    print(f"--- 合計: {total:.1f}km")
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    plan = load()
    if plan is None:
        print("プランがありません。", file=sys.stderr)
        return 1
    target = args.day or today_iso()
    hits = [w for w in plan.workouts if w.day == target]
    if not hits:
        print(f"{target} のメニューが見つかりません。", file=sys.stderr)
        return 1
    for w in hits:
        w.done = True
    save(plan)
    print(f"完了: {target} ({len(hits)}件)")
    return 0


def cmd_week(args: argparse.Namespace) -> int:
    plan = load()
    if plan is None:
        print("プランがありません。", file=sys.stderr)
        return 1
    today = date.today()
    start = today - timedelta(days=today.weekday())  # 月曜
    end = start + timedelta(days=6)
    print(f"今週 ({start} 〜 {end})")
    total = 0.0
    for w in plan.workouts:
        if start.isoformat() <= w.day <= end.isoformat():
            mark = "[x]" if w.done else "[ ]"
            print(f"  {mark} {w.day}  {w.type:<8} {w.distance_km:.1f}km")
            total += w.distance_km
    print(f"  週間合計: {total:.1f}km")
    return 0


def cmd_auth_oura(args: argparse.Namespace) -> int:
    set_config("oura_token", args.token)
    print("OURAトークンを保存しました。")
    return 0


def cmd_auth_strava(args: argparse.Namespace) -> int:
    if args.code:
        tok = strava_src.exchange_code(args.client_id, args.client_secret, args.code)
        strava_src.save_initial_tokens(args.client_id, args.client_secret, tok)
        print("Stravaトークンを保存しました。")
        return 0
    print("以下のURLをブラウザで開いて承認し、リダイレクト先URLの `code=` 値を取得してください:\n")
    print(strava_src.authorize_url(args.client_id))
    print("\n取得したコードで再度実行:")
    print(f"  running-trainer auth strava --client-id {args.client_id} "
          f"--client-secret <SECRET> --code <CODE>")
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    targets = args.source or ["oura", "strava"]
    if "oura" in targets:
        try:
            n = oura_src.sync(days=args.days)
            print(f"OURA: {n}日分を同期")
        except Exception as e:
            print(f"OURA同期失敗: {e}", file=sys.stderr)
    if "strava" in targets:
        try:
            n = strava_src.sync(days=args.days)
            print(f"Strava: {n}件のアクティビティを同期")
        except Exception as e:
            print(f"Strava同期失敗: {e}", file=sys.stderr)
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    print(build_context(days=args.days))
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    msg = " ".join(args.message) if args.message else None
    if not msg:
        print("質問を入力してください。例: running-trainer chat \"明日のメニューは?\"", file=sys.stderr)
        return 1
    try:
        print(advisor_chat(msg, days=args.days))
    except Exception as e:
        print(f"相談失敗: {e}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="running-trainer", description="ランニング計画管理")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="新しいプランを作成")
    pi.add_argument("name", help="プラン名 (例: フルマラソンSub4)")
    pi.add_argument("--goal", help="目標 (例: 2026-10-15 サブ4)")
    pi.set_defaults(func=cmd_init)

    pa = sub.add_parser("add", help="メニューを追加")
    pa.add_argument("day", help="日付 YYYY-MM-DD")
    pa.add_argument("type", choices=["easy", "interval", "tempo", "long", "rest"])
    pa.add_argument("km", type=float, help="距離 km")
    pa.add_argument("--note", help="メモ")
    pa.set_defaults(func=cmd_add)

    pl = sub.add_parser("list", help="メニュー一覧")
    pl.add_argument("--upcoming", action="store_true", help="今日以降のみ")
    pl.set_defaults(func=cmd_list)

    pd = sub.add_parser("done", help="メニューを完了にする")
    pd.add_argument("--day", help="日付 (省略時は今日)")
    pd.set_defaults(func=cmd_done)

    pw = sub.add_parser("week", help="今週のメニュー")
    pw.set_defaults(func=cmd_week)

    # --- データ連携 ---
    auth = sub.add_parser("auth", help="外部サービスの認証")
    auth_sub = auth.add_subparsers(dest="auth_cmd", required=True)

    ao = auth_sub.add_parser("oura", help="OURAパーソナルアクセストークンを設定")
    ao.add_argument("--token", required=True)
    ao.set_defaults(func=cmd_auth_oura)

    as_ = auth_sub.add_parser("strava", help="Strava OAuth認証")
    as_.add_argument("--client-id", required=True)
    as_.add_argument("--client-secret")
    as_.add_argument("--code", help="承認URLから取得した認可コード")
    as_.set_defaults(func=cmd_auth_strava)

    psync = sub.add_parser("sync", help="OURA/Stravaからデータ同期")
    psync.add_argument("--days", type=int, default=60)
    psync.add_argument("--source", action="append", choices=["oura", "strava"],
                       help="指定したソースのみ同期 (省略時は全部)")
    psync.set_defaults(func=cmd_sync)

    psum = sub.add_parser("summary", help="直近のトレーニング/コンディション集計")
    psum.add_argument("--days", type=int, default=28)
    psum.set_defaults(func=cmd_summary)

    pchat = sub.add_parser("chat", help="Claudeにメニューを相談")
    pchat.add_argument("message", nargs="+", help="質問内容")
    pchat.add_argument("--days", type=int, default=28, help="参照する直近日数")
    pchat.set_defaults(func=cmd_chat)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
