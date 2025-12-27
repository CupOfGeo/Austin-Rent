resource "google_cloud_run_v2_job" "scraper" {
  name     = var.service_name
  location = var.gcp_region

  template {
    template {
      service_account = google_service_account.scraper_sa.email

      containers {
        image = "us-central1-docker.pkg.dev/${var.gcp_project}/${var.image_repo}/${var.service_name}:latest"

        resources {
          limits = {
            cpu    = "4"
            memory = "4Gi"
          }
        }

        env {
          name  = "ENVIRONMENT"
          value = "DEV"
        }
        env {
          name  = "CRAWLEE_MAX_USED_CPU_RATIO"
          value = "0.75"
        }
        env {
          name  = "CRAWLEE_MAX_USED_MEMORY_RATIO"
          value = "0.75"
        }
        env {
          name  = "CRAWLEE_PURGE_ON_START"
          value = "true"
        }

        volume_mounts {
          name       = "cloudsql"
          mount_path = "/cloudsql"
        }
      }

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = ["austin-rent:us-central1:austin-rent-db"]
        }
      }
    }

    # Job execution configuration
    task_count  = 1
    parallelism = 1
  }
}

resource "google_cloud_scheduler_job" "scraper_job" {
  name        = "${var.service_name}-cron"
  description = "Trigger Cloud Run scraper job every day at 12 PM"
  schedule    = "0 12 * * *"
  time_zone   = "Etc/UTC"

  http_target {
    http_method = "POST"
    uri         = "https://${var.gcp_region}-run.googleapis.com/v2/projects/${var.gcp_project}/locations/${var.gcp_region}/jobs/${var.service_name}:run"

    oauth_token {
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
  role    = "roles/run.developer"
  member  = "serviceAccount:${google_service_account.scraper_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "scraper_db_password_access" {
  secret_id = "manual-private-key"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.scraper_sa.email}"
}

resource "google_project_iam_member" "cloud_sql_client" {
  project = var.gcp_project
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.scraper_sa.email}"
}
