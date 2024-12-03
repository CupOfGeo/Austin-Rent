resource "google_sql_database" "scraper" {
  name     = "scraper"
  instance = var.db_instance
}
