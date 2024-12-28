CREATE TABLE scrape_extractions (
    scrape_extraction_id SERIAL PRIMARY KEY,
    building_id INTEGER NOT NULL,
    scrape_response_id INTEGER NOT NULL,
    unit_number TEXT,
    bed_count NUMERIC,
    bath_count NUMERIC,
    sqft NUMERIC,
    base_rent NUMERIC,
    deposit NUMERIC,
    available DATE,
    img_url TEXT,
    additional_attributes JSON
);