import pytest
from datetime import datetime
from notification.main import create_discord_embed, format_discord_message

def test_create_discord_embed_minimal():
    """Test creating a minimal Discord embed."""
    embed = create_discord_embed(
        title="Test Title",
        description="Test Description"
    )
    
    assert embed["title"] == "Test Title"
    assert embed["description"] == "Test Description"
    assert embed["color"] == 0x00FF00  # Default green color

def test_create_discord_embed_full():
    """Test creating a Discord embed with all fields."""
    test_time = "2024-12-29T15:36:00Z"
    embed = create_discord_embed(
        title="Full Test",
        description="Full Description",
        color="red",
        url="https://example.com",
        fields=[
            {"name": "Field1", "value": "Value1", "inline": True}
        ],
        author={
            "name": "Test Author",
            "url": "https://author.com",
            "icon_url": "https://author.com/icon.png"
        },
        thumbnail_url="https://thumb.com/img.png",
        image_url="https://image.com/img.png",
        footer={"text": "Footer Text", "icon_url": "https://footer.com/icon.png"},
        timestamp=test_time
    )
    
    assert embed["title"] == "Full Test"
    assert embed["description"] == "Full Description"
    assert embed["color"] == 0xFF0000  # Red
    assert embed["url"] == "https://example.com"
    assert len(embed["fields"]) == 1
    assert embed["author"]["name"] == "Test Author"
    assert embed["thumbnail"]["url"] == "https://thumb.com/img.png"
    assert embed["image"]["url"] == "https://image.com/img.png"
    assert embed["footer"]["text"] == "Footer Text"
    assert embed["timestamp"] == test_time

def test_format_discord_message_simple():
    """Test formatting a simple message."""
    message_data = {
        "title": "Simple Test",
        "description": "Simple Description",
        "color": "blue"
    }
    
    result = format_discord_message(message_data)
    
    assert len(result["embeds"]) == 1
    assert result["embeds"][0]["title"] == "Simple Test"
    assert result["embeds"][0]["color"] == 0x0000FF  # Blue

def test_format_discord_message_with_mention():
    """Test formatting a message with @everyone mention."""
    message_data = {
        "title": "Alert",
        "description": "Important alert",
        "mention_everyone": True
    }
    
    result = format_discord_message(message_data)
    
    assert "content" in result
    assert result["content"] == "@everyone"
    assert result["allowed_mentions"] == {"parse": ["everyone"]}

def test_format_discord_message_custom_bot():
    """Test formatting a message with custom bot settings."""
    message_data = {
        "title": "Custom Bot Test",
        "description": "Testing custom bot settings",
        "username": "Test Bot",
        "avatar_url": "https://test.com/avatar.png"
    }
    
    result = format_discord_message(message_data)
    
    assert result["username"] == "Test Bot"
    assert result["avatar_url"] == "https://test.com/avatar.png"
