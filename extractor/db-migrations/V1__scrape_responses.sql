CREATE TABLE scrape_responses (
    scrape_page_id SERIAL PRIMARY KEY,
    file_id UUID NOT NULL,
    requested_url VARCHAR NOT NULL,
    loaded_url VARCHAR NOT NULL,
    building_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    retry_count INTEGER NOT null
);
