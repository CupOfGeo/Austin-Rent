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
