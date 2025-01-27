import os
import json
import base64
import structlog
from flask import Flask, request
import requests
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure logging for GCP
def configure_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

configure_logging()
logger = structlog.get_logger()

# Configuration
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")

RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))

# Discord color constants
DISCORD_COLORS = {
    "red": 0xFF0000,
    "green": 0x00FF00,
    "blue": 0x0000FF,
    "yellow": 0xFFFF00,
    "purple": 0x800080,
    "orange": 0xFFA500,
}

app = Flask(__name__)

def format_discord_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a simple message into Discord's embed format.
    
    Expected input format:
    {
        "title": "Process Finished :check:",
        "description": "finished doing X thing at Y timestamp",
        "color": "green"
    }
    """
    # Get color value, default to green if not specified or invalid
    color_name = message_data.get("color", "green").lower()
    color_value = DISCORD_COLORS.get(color_name, DISCORD_COLORS["green"])
    
    # Create Discord embed format
    return {
        "embeds": [{
            "title": message_data.get("title", "Notification"),
            "description": message_data.get("description", ""),
            "color": color_value
        }]
    }

def send_to_discord(message_data: dict, attempt: int = 1) -> bool:
    """
    Send message to Discord webhook with retry logic.
    
    Args:
        message_data: The message payload to send to Discord
        attempt: Current attempt number
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        # Format message for Discord
        discord_message = format_discord_message(message_data)
        
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=discord_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        response.raise_for_status()
        logger.info("discord_message_sent", 
                   status_code=response.status_code,
                   attempt=attempt,
                   title=message_data.get("title"))
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error("discord_message_failed",
                    error=str(e),
                    attempt=attempt,
                    max_attempts=RETRY_ATTEMPTS,
                    title=message_data.get("title"))
        if attempt < RETRY_ATTEMPTS:
            logger.info("retrying_discord_message", next_attempt=attempt + 1)
            return send_to_discord(message_data, attempt + 1)
        return False

@app.route("/", methods=["POST"])
def handle_pubsub_message():
    """Handle Pub/Sub push messages."""
    envelope = request.get_json()
    
    if not envelope:
        logger.error("no_payload_received")
        return "No payload received", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        logger.error("invalid_payload_format", envelope=envelope)
        return "Invalid payload format", 400

    pubsub_message = envelope["message"]
    
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        try:
            data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
            message_data = json.loads(data)
            
            log = logger.bind(
                message_id=pubsub_message.get("messageId", "unknown"),
                publish_time=pubsub_message.get("publishTime", "unknown")
            )
            
            log.info("processing_message", title=message_data.get("title"))
            
            if send_to_discord(message_data):
                log.info("message_processed_successfully")
                return "Message processed successfully", 200
            else:
                log.error("message_processing_failed")
                return "Failed to process message", 500
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.error("message_processing_error",
                        error=str(e),
                        error_type=type(e).__name__)
            # Don't retry for malformed messages
            return "Invalid message format", 200
            
        except Exception as e:
            logger.error("unexpected_error",
                        error=str(e),
                        error_type=type(e).__name__)
            # Return 500 so Cloud Run will retry
            return "Internal error", 500
    
    return "No message data", 400

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=PORT)