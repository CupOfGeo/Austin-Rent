provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

provider "google-beta" {
  project = var.gcp_project
  region  = var.gcp_region
}

# apps
module "scraper_module" {
  source      = "./scraper-module"
  gcp_project = var.gcp_project
  gcp_region  = var.gcp_region
  db_instance = google_sql_database_instance.austin_rent_instance.name
  image_repo  = google_artifact_registry_repository.artifact_repo.name
}

# Shared repo resources
resource "google_artifact_registry_repository" "artifact_repo" {
  provider      = google
  location      = var.gcp_region
  repository_id = "image-repo"
  format        = "DOCKER"
}
