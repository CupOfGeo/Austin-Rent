"""Utility functions for uploading content to Google Cloud Storage."""

import structlog
from google.api_core.exceptions import GoogleAPIError
from google.cloud import storage  # type: ignore[attr-defined, unused-ignore]

logger = structlog.get_logger()


# https://talkiq.github.io/gcloud-aio/index.html async bucket uploads
def upload_string_to_gcs(
    bucket: storage.bucket.Bucket,
    content: str,
    destination_blob_name: str,
    building_id: int,
) -> None:
    """Uploads a string as a file to the specified GCS bucket."""
    try:
        blob = bucket.blob(destination_blob_name)
        # Passes in building_id to pubsub message
        blob.metadata = {"building_id": building_id}
        blob.upload_from_string(content)

        logger.info(
            "String content uploaded",
            destination_blob_name=destination_blob_name,
            building_id=building_id,
        )
    except GoogleAPIError as e:
        logger.error(f"Failed to upload string to GCS: {e}", exc_info=True)
