variable "place_id" {
  description = "Shibuya Google Place ID"
  type        = string
}

variable "account_id" {
  description = "Google My Business アカウント ID"
  type        = string
}

variable "location_id" {
  description = "Shibuya ロケーション ID"
  type        = string
}

variable "service_account_key_path" {
  description = "サービスアカウント JSON キーファイルのパス"
  type        = string
  sensitive   = true
}

variable "auto_reply_enabled" {
  description = "自動返信機能の有効化"
  type        = bool
  default     = false
}
