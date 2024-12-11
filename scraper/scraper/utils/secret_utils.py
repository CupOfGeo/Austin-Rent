import structlog
from google.cloud import secretmanager

logger = structlog.get_logger()


def get_secret(secret_id: str, version_id: str = "latest") -> str:
    """
    Retrieve a secret from Google Cloud Secret Manager.

    :param secret_id: The ID of the secret.
    :param version_id: The version of the secret (default is "latest").
    :return: The secret value as a string.
    """
    # get_secret() is used by settings so we cant import it hard code so its not breakings
    gcp_project = "austin-rent"
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = client.secret_path(gcp_project, secret_id)
        response = client.access_secret_version(
            request={"name": f"{name}/versions/latest"}
        )
        decode = response.payload.data.decode("UTF-8")
        return decode

    except Exception as e:
        logger.error("Failed to retrieve secret", secret_id=secret_id, error=e)
        return None
