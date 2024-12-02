resource "google_cloud_run_service" "scraper" {
  name     = "scraper"
  location = "us-central1"
  template {
    spec {
      service_account_name = google_service_account.scraper_sa.email
      containers {
        image = "us-central1-docker.pkg.dev/austin-rent/image-repo/bs-crawler:latest"
        ports {
          container_port = 8080
        }
      }
    }
  }
}


resource "google_service_account" "scraper_sa" {
  account_id   = "scraper-sa"
  display_name = "Scraper Cloud Run Service Account"
}

resource "google_storage_bucket_iam_member" "storage" {
  bucket = google_storage_bucket.scraper_responses.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.scraper_sa.email}"
}