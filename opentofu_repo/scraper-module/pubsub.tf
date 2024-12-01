resource "google_pubsub_topic" "dev_scraper_topic" {
  name = "dev-scraper-topic"
}

resource "google_pubsub_subscription" "dev_scraper_subscription" {
  name  = "dev-scraper-subscription"
  topic = google_pubsub_topic.dev_scraper_topic.name
}
