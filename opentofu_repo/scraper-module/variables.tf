# custom variables for the scraper module
variable "service_name" {
  type        = string
  description = "The name of the Google Cloud Run service to create"
  default     = "scraper"
}

# pass in variables from main
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

variable "db_instance" {
  type        = string
  description = "The name of the Google SQL instance to create"
  default     = "austin-rent-db"
}
variable "image_repo" {
  type        = string
  description = "The name of the Google Container Registry to use"
  default     = "image-repo"
}
