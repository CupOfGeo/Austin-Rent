Github actions and workflows this is also its own repo.

The main pipeline should be 

1. Config - this will get the config from the services /infra folder depending on what env its being deployed to default dev.

2. Tag - tags a release when pushed to main.

3. Build - runs test and builds docker image and pushes it to the artifact repo.

4. Deploy - runs flyway migrations and then deploys that image to cloud run. 

When you push to main you will redeploy to dev projects cloud run to deploy to prod you must run the workflow manually with deploy env set to prod. 

