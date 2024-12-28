CREATE TABLE buildings (
	building_id SERIAL PRIMARY KEY,
	address VARCHAR NOT NULL,
    building_name VARCHAR,
    url VARCHAR not null,
    is_active BOOLEAN default TRUE
);
