import enum

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import URL

from ..utils.secret_utils import get_secret

load_dotenv(".env")


class Env(str, enum.Enum):
    """Possible Deploy Environments."""

    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    db_host: str = Field("0.0.0.0", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_user: str = Field("admin", env="DB_USER")
    db_pass: str = Field(get_secret("scraper-db-password"), env="DB_PASS")
    db_name: str = Field("scraper", env="DB_NAME")
    db_echo: bool = Field(True, env="DB_ECHO")

    debug_building_limit: int = Field(1, env="DEBUG_BUILDING_LIMIT")
    environment: str = Field("LOCAL", env="ENVIRONMENT")
    gcp_project: str = Field("austin-rent", env="GCP_PROJECT")
    logging_level: str = Field("INFO", env="LOGGING_LEVEL")
    webserver_port: int = Field(8080, env="WEBSERVER_PORT")

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        # local postgres URL schema
        if self.environment == "LOCAL":
            return URL.create(
                drivername="postgresql+asyncpg",
                host=self.db_host,
                port=self.db_port,
                username=self.db_user,
                password=self.db_pass,
                database=self.db_name,
            )

        # gcp cloud sql has a different connection url schema
        return URL.create(
            drivername="postgresql+asyncpg",
            host=f"{self.db_host}?host=/cloudsql/austin-rent:us-central1:austin-rent-db",
            username=self.db_user,
            password=self.db_pass,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
