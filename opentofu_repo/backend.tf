terraform {
  required_version = ">= 1.0.0"

  backend "gcs" {
    bucket = var.tofu_backend_bucket_name
    prefix = "tofu/state"
  }
}


resource "google_storage_bucket" "tofu_backend" {
  project                     = var.gcp_project
  name                        = var.tofu_backend_bucket_name
  location                    = var.gcp_region
  storage_class               = var.storage_class
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}
