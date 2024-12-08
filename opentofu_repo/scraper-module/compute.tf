# TODO look into google_cloud_run_v2_service
resource "google_cloud_run_service" "scraper" {
  name     = "scraper"
  location = "us-central1"
  template {
    spec {
      service_account_name = google_service_account.scraper_sa.email
      containers {
        image = "us-central1-docker.pkg.dev/austin-rent/image-repo/scraper:latest"
        ports {
          container_port = 8080
        }
      }
    }
  }
}

resource "google_cloud_scheduler_job" "scraper_job" {
  name             = "scraper-job"
  description      = "Trigger Cloud Run scraper service every day at 12 PM"
  schedule         = "0 12 * * *"  # Cron expression for 12 PM daily
  time_zone        = "Etc/UTC"     # Adjust the time zone if needed

  http_target {
    http_method = "POST"
    uri         = google_cloud_run_service.scraper.status[0].url
    oidc_token {
      service_account_email = google_service_account.scraper_sa.email
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

resource "google_project_iam_member" "scheduler_invoker" {
  project = var.gcp_project
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.scraper_sa.email}"
}
