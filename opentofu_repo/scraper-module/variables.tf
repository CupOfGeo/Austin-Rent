# define GCP region
variable "gcp_region" {
  type        = string
  description = "GCP region"
  default     = "us-central1"
}

variable "zone" {
  type        = string
  description = "GCP zone"
  default     = "us-central1-a"
}
variable "gcp_project" {
 type        = string
 description = "GCP project name"
}
variable "machine_type" {
  type        = string
  description = "The name of the Google Storage Bucket to create"
  default     = "e2-small"
}

variable "db_instance" {
  type        = string
  description = "The name of the Google SQL instance to create"
  default     = "austin-rent-db"
}

# variable "scraper_server_image" {
#   type        = string
#   description = "image in GAR"
# }
