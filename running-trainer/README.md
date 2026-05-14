# running-trainer

OURA Ring と Strava (Garminは Strava 経由) からデータを取得し、
過去のトレーニングと体調を統合した上で Claude に **次のメニューを相談できる** ランニング向け CLI。

## できること

- **計画管理**: 週次のメニューを登録・完了管理
- **データ同期**: OURA (Readiness/Sleep/HRV/RHR) + Strava (距離/ペース/HR) を SQLite に蓄積
- **サマリー**: 直近の週間距離・強度・コンディションを集計
- **AI相談**: Claude (claude-sonnet-4-6) に集計コンテキストを渡して具体的なメニュー提案を受ける

## インストール

```bash
pip install -e .
export ANTHROPIC_API_KEY=...   # 相談機能用
```

データは `~/.running_trainer/data.db` (SQLite) と `~/.running_trainer/plan.json` に保存されます。

## セットアップ

### OURA
1. <https://cloud.ouraring.com/personal-access-tokens> で個人アクセストークンを発行
2. 設定:
   ```bash
   running-trainer auth oura --token <TOKEN>
   ```

### Strava (Garminは Garmin→Strava 自動同期に任せる前提)
1. <https://www.strava.com/settings/api> で API アプリを作成 (Authorization Callback Domain は `localhost` でOK)
2. 認可URLを取得:
   ```bash
   running-trainer auth strava --client-id <CLIENT_ID>
   ```
3. 表示された URL をブラウザで開いて承認 → リダイレクト先 URL の `code=` 値をコピー
4. トークン交換:
   ```bash
   running-trainer auth strava --client-id <CLIENT_ID> --client-secret <SECRET> --code <CODE>
   ```

## 使い方

```bash
# データ同期 (デフォルト60日)
running-trainer sync
running-trainer sync --days 90 --source strava

# サマリー表示 (LLMに渡すのと同じコンテキスト)
running-trainer summary --days 28

# 相談
running-trainer chat "今週末にロング走を入れたいけど、コンディション的にどう?"
running-trainer chat "サブ4を狙ってる。次の2週間のメニュー組んで" --days 56
```

### 計画管理 (任意)

```bash
running-trainer init "フルマラソンSub4" --goal "2026-10-15 サブ4"
running-trainer add 2026-04-12 long 20
running-trainer week
running-trainer done
```

## アーキテクチャ

```
src/running_trainer/
├── cli.py            # argparse エントリ
├── db.py             # SQLite (activities / daily_metrics / config)
├── storage.py        # plan.json (手動の計画)
├── sources/
│   ├── oura.py       # OURA v2 API
│   └── strava.py     # Strava OAuth + activities API
├── summary.py        # 集計 → LLM向けテキスト生成
└── advisor.py        # Claude API (claude-sonnet-4-6)
```

## 注意点

- Garmin の個人向け公式APIは無いため、Garmin → Strava 自動同期を有効にしておくと
  Strava経由でGarminのアクティビティも取得できます。
- Strava API には日次/15分単位のレート制限があります。`sync` の頻度に注意。
- OURA トークンや Strava の client_secret は SQLite (`config` テーブル) に平文保存されます。
  共有マシンでは扱いに注意してください。
