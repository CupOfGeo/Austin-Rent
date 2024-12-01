#resource "google_compute_instance" "web-server" {
#  name         = "test-webserver"
#  machine_type = var.machine_type
#  zone         = var.zone
#
#  tags = ["http-server"]
#
#  boot_disk {
#    initialize_params {
##            image = "debian-cloud/debian-11"
#      image = var.web-image
#    }
#  }
#
#  network_interface {
#    network = "default"
#    access_config {
#
#    }
#  }
#
#  #  metadata_startup_script = "echo hi > /test.txt"
#  #  metadata_startup_script = file("./apache2.sh")
#
#  scheduling {
#    preemptible       = true
#    automatic_restart = false
#  }
#
#  #  from https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance
#  #  service_account {
#  #    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
#  #    email  = google_service_account.default.email
#  #    scopes = ["cloud-platform"]
#  #  }
#}


# resource "google_cloud_run_service" "scraper_server" {
#   name     = "scraper-server"
#   location = "us-central1"
#   template {
#     spec {
#       containers {
#         image = var.scraper_server_image
#         ports {
#           container_port = 8080
#         }
#       }
#     }
#   }
# }

# output "scraper_server_url" {
#   value = google_cloud_run_service.scraper_server.status[0].url
# }


# Create a service account for Cloud Run
# resource "google_service_account" "cloud_run_sa" {
#   account_id   = "cloud-run-sa"
#   display_name = "Cloud Run Service Account"
# }

# Grant the Cloud Run service account permissions to write to the bucket
# resource "google_storage_bucket_iam_member" "cloud_run_bucket_writer" {
#   bucket = google_storage_bucket.scraper_responses.name
#   role   = "roles/storage.objectCreator"
#   member = "serviceAccount:${google_service_account.cloud_run_sa.email}"
# }


# Update the Cloud Run service to use the new service account
# resource "google_cloud_run_service" "my_service" {
#   name     = "my-cloud-run-service"
#   location = var.gcp_region

#   template {
#     spec {
#       service_account_name = google_service_account.cloud_run_sa.email
#       containers {
#         image = "gcr.io/${var.gcp_project}/my-cloud-run-image"
#       }
#     }
#   }
# }