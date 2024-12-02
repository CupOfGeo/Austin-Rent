from google.cloud import storage
import structlog

logger = structlog.get_logger()

def upload_file_to_gcs(bucket: storage.bucket.Bucket, source_file_path: str, destination_blob_name: str) -> None:
    """Uploads a file to the specified GCS bucket."""
    try:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)

        logger.info("File content uploaded", source_file_path=source_file_path, destination_blob_name=destination_blob_name)
    except Exception as e:
        logger.error(f"Failed to upload file to GCS: {e}", exc_info=True)


def upload_string_to_gcs(bucket: storage.bucket.Bucket, content: str, destination_blob_name: str) -> None:
    """Uploads a string as a file to the specified GCS bucket."""
    try:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(content)

        logger.info("String content uploaded", destination_blob_name=destination_blob_name)
    except Exception as e:
        logger.error(f"Failed to upload string to GCS: {e}", exc_info=True)

def upload_file_to_gcs_from_memory(bucket: storage.bucket.Bucket, file_content: bytes, destination_blob_name: str) -> None:
    """Uploads a file from memory to the specified GCS bucket."""
    try:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(file_content)

        logger.info("File content uploaded", destination_blob_name=destination_blob_name)
    except Exception as e:
        logger.error(f"Failed to upload file content to GCS: {e}")