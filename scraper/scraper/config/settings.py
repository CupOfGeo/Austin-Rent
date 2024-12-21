import enum
import os

from pydantic import Field
from pydantic_settings import BaseSettings
from yarl import URL
import sqlalchemy

from scraper.config.secret_manager import set_env_vars

if os.getenv("ENVIRONMENT") == "LOCAL":
    set_env_vars("./configs/local.yaml")
else:
    set_env_vars("./configs/dev.yaml")


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

    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    # This one actually gets set first by the cloud run deploy script.
    environment: str = Field("LOCAL", validation_alias="ENVIRONMENT")
    gcp_project: str = Field("austin-rent", validation_alias="GCP_PROJECT")

    db_host: str = Field("0.0.0.0", validation_alias="DB_HOST")
    db_port: int = Field(5432, validation_alias="DB_PORT")
    db_user: str = Field("scraper_app", validation_alias="DB_USER")
    # set by secret_manager
    db_pass: str = Field("", validation_alias="DB_PASS")
    db_name: str = Field("scraper", validation_alias="DB_NAME")
    db_echo: bool = Field(True, validation_alias="DB_ECHO")

    debug_building_limit: int = Field(0, validation_alias="DEBUG_BUILDING_LIMIT")

    logging_level: str = Field("INFO", validation_alias="LOGGING_LEVEL")
    webserver_port: int = Field(8080, validation_alias="WEBSERVER_PORT")

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        # local postgres URL schema
        if self.environment == 'LOCAL':
            return URL.build(
                scheme="postgresql+asyncpg",
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_pass,
                path=f"/{self.db_name}",
            )

        # gcp cloud sql has a different connection url schema
        return sqlalchemy.engine.url.URL.create(
            drivername="postgresql+asyncpg",
            username=settings.db_user,
            password=settings.db_pass,
            database=settings.db_name,
            query={"unix_sock": "/cloudsql/austin-rent:us-central1:austin-rent-db"}) #/.s.PGSQL.5432


settings = Settings()
