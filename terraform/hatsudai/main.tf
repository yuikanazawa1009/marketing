terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

module "hatsudai" {
  source = "../modules/facility"

  facility_name            = "hatsudai"
  place_id                 = var.place_id
  account_id               = var.account_id
  location_id              = var.location_id
  service_account_key_path = var.service_account_key_path
  auto_reply_enabled       = var.auto_reply_enabled
  credentials_hub_path     = "../../.company/secretary/credentials"
}
