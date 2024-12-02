# WIF stuff - https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions
resource "google_iam_workload_identity_pool" "main" {
  project                   = var.gcp_project
  workload_identity_pool_id = "github-pool"
  display_name              = "GitHub pool"
}

resource "google_iam_workload_identity_pool_provider" "main" {
  project                            = var.gcp_project
  workload_identity_pool_id          = google_iam_workload_identity_pool.main.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub provider"
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.aud"        = "assertion.aud"
    "attribute.repository" = "assertion.repository"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
  attribute_condition = "attribute.repository == '${var.github_organization_repo}'"
}

resource "google_service_account" "gh_sa" {
  account_id   = "github-sa"
  display_name = "Github Service Account"
}

resource "google_project_iam_member" "editor" {
  project = var.gcp_project
  member  = "serviceAccount:${google_service_account.gh_sa.email}"
  role    = "roles/editor"
}

resource "google_project_iam_member" "pubsub" {
  project = var.gcp_project
  member  = "serviceAccount:${google_service_account.gh_sa.email}"
  role    = "roles/pubsub.admin"
}

resource "google_project_iam_member" "iam" {
  project = var.gcp_project
  member  = "serviceAccount:${google_service_account.gh_sa.email}"
  role    = "roles/iam.securityAdmin"
}

resource "google_project_iam_member" "secretmanager" {
  project = var.gcp_project
  member  = "serviceAccount:${google_service_account.gh_sa.email}"
  role    = "roles/secretmanager.secretAccessor"
}

resource "google_project_iam_member" "artifactregistry" {
  project = var.gcp_project
  member  = "serviceAccount:${google_service_account.gh_sa.email}"
  role    = "roles/artifactregistry.writer"
}

resource "google_service_account_iam_binding" "workload_identity_user_binding" {
  service_account_id = google_service_account.gh_sa.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.main.name}/attribute.repository/${var.github_organization_repo}",
  ]
}
