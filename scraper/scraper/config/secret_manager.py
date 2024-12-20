"""
This function retrieves a single age private key from Google Cloud Secret Manager.
This was inspired by how sealed secrets work in kubernetes.
This allows developers to add any secret they want without having to worry about managing gcp or github secrets.
"""

import base64
import os
import subprocess
import tempfile
from typing import Optional

import structlog
import yaml
from google.cloud import secretmanager

logger = structlog.get_logger()


def get_gcp_secret(secret_id: str, version_id: str = "latest") -> Optional[str]:
    """
    Retrieve a secret from Google Cloud Secret Manager.

    :param secret_id: The ID of the secret.
    :param version_id: The version of the secret (default is "latest").
    :return: The secret value as a string.
    """
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


def load_yaml(yaml_file_path: str) -> dict:
    try:
        with open(yaml_file_path, "r") as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)
    except Exception as e:
        raise Exception(f"Error loading YAML file: {e}")
    return yaml_content


def decrypt_value(encrypted_value: str, private_key_secret: str) -> str:
    encrypted_bytes = base64.b64decode(encrypted_value)
    result = subprocess.run(
        ["age", "--decrypt", "--identity", private_key_secret],
        input=encrypted_bytes,
        capture_output=True,
    )
    if result.returncode != 0:
        raise Exception(f"Decryption failed: {result.stderr}")
    return result.stdout.strip().decode("utf-8")


def set_env_vars(yaml_file_path: str) -> dict:
    private_key_secret = get_gcp_secret("manual-private-key")
    yaml_content = load_yaml(yaml_file_path)
    secrets = yaml_content.get("secrets", {})
    envs = yaml_content.get("env_vars", {})
    for key, value in envs.items():
        os.environ[key] = os.getenv(key, value)
    # secrets overwrites env_vars
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(private_key_secret.encode())
        temp_file_path = temp_file.name
    for key, encrypted_value in secrets.items():
        decrypted_value = decrypt_value(encrypted_value, temp_file_path)
        os.environ[key] = decrypted_value
