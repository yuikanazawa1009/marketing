#!/usr/bin/env python3
"""
credentials ハブ化スクリプト
各施設のサービスアカウントキー JSON を .company/secretary/credentials/ に集約する。

使い方:
    python scripts/copy_credentials.py \
        --shibuya  /path/to/shibuya-sa-key.json \
        --hatsudai /path/to/hatsudai-sa-key.json \
        --honmachi /path/to/honmachi-sa-key.json

    # 単一施設だけコピーする場合:
    python scripts/copy_credentials.py --shibuya /path/to/shibuya-sa-key.json
"""

import argparse
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CREDENTIALS_HUB = PROJECT_ROOT / ".company" / "secretary" / "credentials"

FACILITIES = {
    "shibuya":  "shibuya_sa_key.json",
    "hatsudai": "hatsudai_sa_key.json",
    "honmachi": "honmachi_sa_key.json",
}


def copy_credential(facility: str, src_path: str) -> None:
    src = Path(src_path).resolve()
    if not src.exists():
        print(f"[ERROR] ファイルが見つかりません: {src}", file=sys.stderr)
        sys.exit(1)
    if not src.suffix == ".json":
        print(f"[WARN]  JSON ファイルではありません: {src}")

    CREDENTIALS_HUB.mkdir(parents=True, exist_ok=True)
    dst = CREDENTIALS_HUB / FACILITIES[facility]
    shutil.copy2(src, dst)
    dst.chmod(0o600)
    print(f"[OK]    {facility}: {src} -> {dst}")


def verify_hub() -> None:
    """ハブにある credentials の一覧を表示する"""
    print(f"\n--- credentials ハブ確認: {CREDENTIALS_HUB} ---")
    if not CREDENTIALS_HUB.exists():
        print("  (ディレクトリが存在しません)")
        return
    files = sorted(CREDENTIALS_HUB.glob("*.json"))
    if not files:
        print("  (JSON ファイルなし)")
    for f in files:
        size = f.stat().st_size
        print(f"  {f.name}  ({size:,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="各施設の credentials を .company/secretary/credentials/ に集約します"
    )
    for facility in FACILITIES:
        parser.add_argument(
            f"--{facility}",
            metavar="PATH",
            help=f"{facility} サービスアカウント JSON のパス",
        )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="コピーせずにハブの現状を確認するだけ",
    )
    args = parser.parse_args()

    if args.verify:
        verify_hub()
        return

    copied = 0
    for facility in FACILITIES:
        src = getattr(args, facility)
        if src:
            copy_credential(facility, src)
            copied += 1

    if copied == 0:
        parser.print_help()
        print("\n[INFO] コピー対象が指定されていません。--verify で現状確認できます。")
        sys.exit(0)

    verify_hub()
    print(f"\n完了: {copied} 施設分の credentials をコピーしました。")


if __name__ == "__main__":
    main()
