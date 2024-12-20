https://www.terraform-best-practices.com/naming

# Initial Setup
Made a new GCP project Austin-Rent
Install https://opentofu.org/docs/intro/install/standalone/

Note: Install gcloud outside of the git repo. I put it in the home directory.
Install https://cloud.google.com/sdk/docs/install#linux

Age keygen
`sudo apt install age`


## WIF setup
https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions

So this service account should be the one that tofu uses in the CI/CD


## Enabling services
TODO do this with tofu
```
gcloud services enable artifactregistry.googleapis.com --project=austin-rent
gcloud services list --enabled --project=austin-rent
```

I first commented out the backend and created the bucket applied then uncommented it and reapplied.


## Database setup
So having a lot of difficulties managing postgres users. all users are granted the role `cloudsqlsuperuser`.
Running this once will grant read/write permissions.
```sql
GRANT USAGE, CREATE ON SCHEMA public TO cloudsqlsuperuser;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO cloudsqlsuperuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO cloudsqlsuperuser;
```

```
GRANT USAGE, SELECT ON SEQUENCE scrape_responses_scrape_page_id_seq TO your_username;
GRANT INSERT, UPDATE, DELETE ON TABLE scrape_responses TO your_username;
```
*TODO* having / managing multiple schema for feature branches

## ?
Im going back and forth between if I should have a dev prod envs bc i want to have a company in a repo but I don't actually want a prod pricing.
you don't want to duplicate everything in prod like we only need one artifact repo ?? right?


#### other
https://github.com/terraform-google-modules 
