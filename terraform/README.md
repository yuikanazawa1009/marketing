# Porthouses レビュー管理システム - Terraform

施設ごとの Google Business Profile 設定を管理し、
`.company/secretary/credentials/` に設定 JSON を書き出します。

---

## フォルダ構成

```
terraform/
├── modules/
│   └── facility/          ← 共通モジュール
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── shibuya/               ← 渋谷施設
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── hatsudai/              ← 初台施設
├── honmachi/              ← 本町施設
└── .gitignore             ← tfvars・tfstate を除外
```

---

## セットアップ手順

### 1. 変数ファイルを作成

各施設フォルダで example をコピーして実際の値を記入：

```bash
# 例: shibuya
cd terraform/shibuya
cp terraform.tfvars.example terraform.tfvars
# terraform.tfvars を編集して place_id / account_id / location_id 等を入力
```

### 2. SA キーをハブにコピー

```bash
python scripts/copy_credentials.py \
    --shibuya  /path/to/shibuya-sa-key.json \
    --hatsudai /path/to/hatsudai-sa-key.json \
    --honmachi /path/to/honmachi-sa-key.json

# 確認だけしたい場合
python scripts/copy_credentials.py --verify
```

### 3. Terraform apply

```bash
cd terraform/shibuya
terraform init
terraform apply

# hatsudai / honmachi も同様
```

apply 後、`.company/secretary/credentials/shibuya_config.json` が生成されます。

### 4. Python から読み込む

```python
from credentials_hub import load_facility_config, load_sa_credentials

# 設定 JSON（Terraform が生成）
config = load_facility_config("shibuya")
print(config["place_id"])

# Google SA 認証情報
creds = load_sa_credentials("shibuya")

# ハブ全体の状態確認
python .company/porthouses/review-system/credentials_hub.py
```

---

## credentials ハブ

```
.company/secretary/credentials/
├── shibuya_config.json    ← terraform apply が生成（place_id 等）
├── shibuya_sa_key.json    ← copy_credentials.py がコピー（SA キー）
├── hatsudai_config.json
├── hatsudai_sa_key.json
├── honmachi_config.json
└── honmachi_sa_key.json
```

**.gitignore で GitHub への流出を防止済み。**

---

## ファイルの役割

| ファイル | 役割 |
|---|---|
| `terraform.tfvars` | 施設固有の秘密値（**git 除外**） |
| `terraform.tfvars.example` | 記入テンプレート（git 管理） |
| `*_config.json` | Terraform apply が生成する設定（**git 除外**） |
| `*_sa_key.json` | Google SA キー（**git 除外**） |
