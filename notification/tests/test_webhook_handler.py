import json
import base64
import pytest
import responses
from notification.main import app, send_to_discord

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@responses.activate
def test_send_to_discord_success():
    """Test successful Discord webhook call."""
    responses.add(
        responses.POST,
        "https://discord.com/api/webhooks/test",
        json={"success": True},
        status=200
    )
    
    message_data = {
        "title": "Test Message",
        "description": "Test Description"
    }
    
    result = send_to_discord(message_data)
    assert result is True

@responses.activate
def test_send_to_discord_retry():
    """Test Discord webhook retry mechanism."""
    # Add two failures followed by a success
    responses.add(
        responses.POST,
        "https://discord.com/api/webhooks/test",
        json={"error": "Rate limited"},
        status=429
    )
    responses.add(
        responses.POST,
        "https://discord.com/api/webhooks/test",
        json={"error": "Rate limited"},
        status=429
    )
    responses.add(
        responses.POST,
        "https://discord.com/api/webhooks/test",
        json={"success": True},
        status=200
    )
    
    message_data = {
        "title": "Test Message",
        "description": "Test Description"
    }
    
    result = send_to_discord(message_data)
    assert result is True
    assert len(responses.calls) == 3

def test_pubsub_handler_invalid_request(client):
    """Test handling of invalid Pub/Sub messages."""
    response = client.post("/", json={})
    assert response.status_code == 400
    
    response = client.post("/", json={"not_a_message": {}})
    assert response.status_code == 400

def test_pubsub_handler_valid_message(client):
    """Test handling of valid Pub/Sub messages."""
    message_data = {
        "title": "Test Title",
        "description": "Test Description"
    }
    
    pubsub_message = {
        "message": {
            "data": base64.b64encode(json.dumps(message_data).encode()).decode(),
            "messageId": "test-message-id",
            "publishTime": "2024-12-29T15:36:00Z"
        }
    }
    
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            "https://discord.com/api/webhooks/test",
            json={"success": True},
            status=200
        )
        
        response = client.post("/", json=pubsub_message)
        assert response.status_code == 200

def test_pubsub_handler_invalid_json(client):
    """Test handling of invalid JSON in Pub/Sub message."""
    pubsub_message = {
        "message": {
            "data": base64.b64encode(b"invalid json").decode(),
            "messageId": "test-message-id",
            "publishTime": "2024-12-29T15:36:00Z"
        }
    }
    
    response = client.post("/", json=pubsub_message)
    assert response.status_code == 200  # We don't retry invalid messages
