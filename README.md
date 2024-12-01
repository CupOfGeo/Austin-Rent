# Lets build something that scrapes rent prices on Rainey street and uploads them to a database.

My initial idea of the system.

- Well we gotta start with a list of urls somewhere. Maybe they live in a database 
    [https://700river.com/floorplans/, https://sightmap.com/app/api/v1/8epml7q1v6d/sightmaps/80524, ...]

- Well have a cron job that will basically just select everything from that database and publish messages to a scrape service 

- well make requests to them for now http should be fine and we shouldn't worry about cloning the browser with playwright. This should be its own service that we send messages (url) to and it will save the response to a bucket and pass that id on as a message to

- Extraction service this will given a page and a complex page extract the relevant fields we want from the scraped response. Should be relatively generic so that we can just create new configs per complex (*thinking maybe should do by address*). then save the extraction to the database. if the extraction fails we should save a failed. well have the original scraped response saved to the bucket so we could reprocess it if its a valid page.


Simple One service to rule them all.

- List is hard coded into they code 
- We also do parsing in the code
- save it to the db from here

https://github.com/apify/crawlee-python

# Common readme 
this is the common read me that will spread standards across multiple repos 

## Database 
Postgres dbs 
https://gist.github.com/kyledcline/9b7e864b89c269beb2c34e55fb0903b0

naming convention. 
    - underscores for table_name
    - PK should be table_name_id

Connecting to CloudSQL 
https://cloud.google.com/sql/docs/mysql/connect-auth-proxy
Note: if you are in a dev container use linux 64. Then move it to `mv cloud-sql-proxy ~/.local/bin/`

```
./cloud-sql-proxy --address 0.0.0.0 --port 5432 austin-rent:us-central1:austin-rent-db
```
## Deploy to cloud run 

Main Mermaid diagram

```mermaid
```

# Secrets 

for now I'm fine with just making new ones with gcloud 

TODO this is bad bc the echo will eval anything with a `$`
```bash
echo -n "your-secure-password" | gcloud secrets create db-password --data-file=-
```
