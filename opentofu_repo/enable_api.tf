resource "google_project_service" "sql_admin_api" {
  project            = var.gcp_project
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute_engine_api" {
  project            = var.gcp_project
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}