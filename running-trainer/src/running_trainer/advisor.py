"""Claude APIを使ったトレーニング相談."""
from __future__ import annotations

import os

from anthropic import Anthropic

from .summary import build_context

MODEL = "claude-sonnet-4-6"

SYSTEM = """あなたはエビデンスベースのランニングコーチです。
ユーザーの過去のトレーニング履歴 (Strava) と日々のコンディション (OURA) を踏まえて、
- リカバリー状態 (HRV, Readiness, 安静時心拍, 睡眠)
- 直近の負荷 (週間距離, 強度, 連続日数)
- ユーザーが述べる目標や主観
を統合し、安全で具体的な次のメニューや調整を提案してください。

回答ルール:
- まず観察 (データから読み取れること) を3-5点で示す
- 次に推奨メニュー (距離・ペース・強度) を具体的に提示する
- 最後に注意点や代替案を述べる
- オーバートレーニングや疲労兆候があれば率直に休養を勧める
- 日本語で簡潔に答える
"""


def chat(user_message: str, days: int = 28) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY が未設定です。")
    client = Anthropic(api_key=api_key)
    context = build_context(days=days)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": f"{context}\n\n---\n# 質問\n{user_message}",
            }
        ],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
