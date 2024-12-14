import enum

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from scraper.utils.secret_utils import get_secret

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

    db_host: str = Field("0.0.0.0", validation_alias="DB_HOST")
    db_port: int = Field(5432, validation_alias="DB_PORT")
    db_user: str = Field("scraper_app", validation_alias="DB_USER")
    db_pass: str = Field(get_secret("austin-rent-db_scraper_app"), validation_alias="DB_PASS")
    db_name: str = Field("scraper", validation_alias="DB_NAME")
    db_echo: bool = Field(True, validation_alias="DB_ECHO")

    debug_building_limit: int = Field(1, validation_alias="DEBUG_BUILDING_LIMIT")
    environment: str = Field("LOCAL", validation_alias="ENVIRONMENT")
    gcp_project: str = Field("austin-rent", validation_alias="GCP_PROJECT")
    logging_level: str = Field("INFO", validation_alias="LOGGING_LEVEL")
    webserver_port: int = Field(8080, validation_alias="WEBSERVER_PORT")

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

    # TODO update to SettingConfigDict
    # class ConfigDict:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"


settings = Settings()
