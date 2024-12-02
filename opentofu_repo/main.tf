provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
  zone    = "us-central1-c"
}

# apps 
module "scraper_module" {
  source      = "./scraper-module"
  gcp_project = var.gcp_project
  gcp_region  = var.gcp_region
  db_instance = google_sql_database_instance.austin_rent_instance.name
}

# Shared repo resources
resource "google_artifact_registry_repository" "artifact_repo" {
  provider      = google
  location      = var.gcp_region
  repository_id = "image-repo"
  format        = "DOCKER"
}

resource "google_sql_database_instance" "austin_rent_instance" {
  name             = "austin-rent-db"
  database_version = "POSTGRES_15"
  region           = var.gcp_region

  settings {
    tier = "db-f1-micro"
  }
}

data "google_secret_manager_secret_version" "scraper_db_password_value" {
  secret  = "scraper-db-password"
  project = var.gcp_project
}

resource "google_sql_user" "user" {
  name     = "admin"
  instance = google_sql_database_instance.austin_rent_instance.name
  password = data.google_secret_manager_secret_version.scraper_db_password_value.secret_data
}
