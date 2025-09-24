A GO microservice that will receive messages and post them to discord webhook.

# Set up 
go to your discord server settings and get the discord webhook url.
save that as `DISCORD_URL=https://discord.com/api/webhooks/` in the .env file.


```bash
curl --location 'http://127.0.0.1:8080/message' \
--header 'Content-Type: text/plain' \
--data '{
    "title": "Test Title",
    "description": "Test Description",
    "app_name": "scraper",
    "color": 16711680,
    "timestamp": "2023-10-10T10:10:10Z",
    "fields": {
        "Field1": "Value1",
        "Field2": "Value2"
    }
}'
```

```
docker build notification 
```