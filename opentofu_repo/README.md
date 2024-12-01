https://www.terraform-best-practices.com/naming

# Initial Setup
Made a new GCP project Austin-Rent
Install https://opentofu.org/docs/intro/install/standalone/

Note: Install gcloud outside of the git repo. I put it in the home directory.
Install https://cloud.google.com/sdk/docs/install#linux


```
gcloud iam service-accounts create tofu-admin --display-name "Tofu admin account"

gcloud projects add-iam-policy-binding austin-rent --member "serviceAccount:tofu-admin@austin-rent.iam.gserviceaccount.com" --role "roles/editor"

gcloud iam service-accounts keys create ~/tofu-key.json --iam-account tofu-admin@austin-rent.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding austin-rent \
  --member="serviceAccount:tofu-admin@austin-rent.iam.gserviceaccount.com" \
  --role="roles/pubsub.admin"

gcloud projects add-iam-policy-binding austin-rent \
  --member="serviceAccount:tofu-admin@austin-rent.iam.gserviceaccount.com" \
  --role="roles/iam.securityAdmin"

gcloud projects add-iam-policy-binding austin-rent \
  --member="serviceAccount:tofu-admin@austin-rent.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```
Moved that key to secrets folder.


## Enabling services 
```
gcloud services enable artifactregistry.googleapis.com --project=austin-rent
gcloud services list --enabled --project=austin-rent
```

I first commented out the backend and created the bucket applied then uncommented it and reapplied.


# Managing secrets
We'll create a new gcp secret with gcloud and then read the value with tofu

```bash
echo -n "your-secure-password" | gcloud secrets create db-password --data-file=-
```

```
data "google_secret_manager_secret_version" "db_password" {
  secret  = "db-password"
  project = "your-project-id"
}

resource "google_sql_user" "user" {
  name     = "admin"
  instance = google_sql_database_instance.instance.name
  password = data.google_secret_manager_secret_version.db_password.secret_data
}
```