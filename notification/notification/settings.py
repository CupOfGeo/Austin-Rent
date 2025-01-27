import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging configuration
logging_level = os.getenv('LOG_LEVEL', 'INFO')

# Discord configuration
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
discord_username = os.getenv('DISCORD_USERNAME', 'AustinRent Bot')
discord_avatar_url = os.getenv('DISCORD_AVATAR_URL', '')

# Application configuration
retry_attempts = int(os.getenv('RETRY_ATTEMPTS', '3'))

# Discord color constants
DISCORD_COLORS = {
    "red": 0xFF0000,
    "green": 0x00FF00,
    "blue": 0x0000FF,
    "yellow": 0xFFFF00,
    "purple": 0x800080,
    "orange": 0xFFA500,
}
