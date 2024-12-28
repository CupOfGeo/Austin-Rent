import pytest
from scraper.handlers.json_handler import json_extract
import os
import json


@pytest.fixture
def json_content():
    test_data_path = os.path.join(os.path.dirname(__file__), 'resources', 'sightmap.json')
    with open(test_data_path, 'r') as file:
        return json.load(file)

def test_parse_sight_map_content(json_content):
    building_id = 12345  # Example building_id
    scrape_response_id = 67890  # Example scrape_page_id
    extractions = json_extract(json_content, building_id, scrape_response_id)
    
    assert len(extractions) == 300
    assert extractions[0].available == '2024-12-07'
    assert extractions[0].base_rent == 4200
    assert extractions[0].bed_count == 1
    assert extractions[0].bath_count == 1
    assert extractions[0].img_url == "https://cdn.sightmap.com/assets/8e/pm/8epmy950p6d/09/b9/09b9a53ea46242ecf61e08156eb68582.jpg"
    assert extractions[0].sqft == 929
    assert extractions[0].unit_number == "1401"




