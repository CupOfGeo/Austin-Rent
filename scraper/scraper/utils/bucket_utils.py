import structlog
from google.cloud import storage

logger = structlog.get_logger()


# def get_bucket(bucket_name: str) -> storage.bucket.Bucket:
#     """Returns a GCS bucket."""
#     try:
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(bucket_name)
#         return bucket
#     except Exception as e:
#         logger.error(f"Failed to get bucket: {e}", exc_info=True)

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
    except Exception as e:
        logger.error(f"Failed to upload string to GCS: {e}", exc_info=True)
