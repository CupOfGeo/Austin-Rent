resource "google_storage_bucket" "scraper_responses" {
  location = var.gcp_region
  name     = "scraper-responses"
  project  = var.gcp_project
  uniform_bucket_level_access = true
}

resource "google_storage_notification" "bucket_notification" {
  bucket         = google_storage_bucket.scraper_responses.name
  topic          = google_pubsub_topic.dev_scraper_topic.id
  event_types    = ["OBJECT_FINALIZE"]
  payload_format = "JSON_API_V1"
  depends_on     = [ google_pubsub_topic_iam_member.storage_topic_publisher ]
}

data "google_storage_project_service_account" "default" {
  project = var.gcp_project
}

resource "google_pubsub_topic_iam_member" "storage_topic_publisher" {
  topic  = google_pubsub_topic.dev_scraper_topic.name
  role   = "roles/pubsub.admin"
  member = "serviceAccount:${data.google_storage_project_service_account.default.email_address}"
}
