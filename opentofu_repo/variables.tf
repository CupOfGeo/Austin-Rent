# define GCP region
variable "gcp_region" {
  type        = string
  description = "GCP region"
}
variable "gcp_project" {
  type        = string
  description = "GCP project name"
}
variable "gcp_auth_file" {
  type        = string
  description = "GCP authentication file"
}
variable "tofu_backend_bucket_name" {
  type        = string
  description = "The name of the Google Storage Bucket to create"
}
variable "storage_class" {
  type        = string
  description = "The storage class of the Storage Bucket to create"
}
variable "github_organization" {
  type        = string
  description = "The GitHub repository org/repo-name"

}