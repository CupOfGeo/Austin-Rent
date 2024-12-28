terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 3.0.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 3.0.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 2.0.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

provider "google-beta" {
  project = var.gcp_project
  region  = var.gcp_region
}


resource "google_sql_database" "scraper" {
  name     = var.service_name
  project  = var.gcp_project
  instance = var.db_instance
}

resource "random_password" "password_app" {
  length  = 24
  special = false
}

resource "google_sql_user" "app" {
  name       = "${var.service_name}_app"
  password   = random_password.password_app.result
  instance   = var.db_instance
  depends_on = [google_sql_database.scraper]
}

resource "google_secret_manager_secret" "app" {
  provider  = google-beta
  secret_id = "${var.db_instance}_${var.service_name}_app"
  replication {
    auto {}
  }
  depends_on = [google_sql_user.app]
}

resource "google_secret_manager_secret_version" "app" {
  provider    = google-beta
  secret      = google_secret_manager_secret.app.id
  secret_data = random_password.password_app.result
}
