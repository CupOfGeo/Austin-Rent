# Copyright (c) 2024 BlackLocus, Inc. All rights reserved.

import logging

import structlog
import structlog_gcp

from scraper.config.settings import settings

logger = structlog.get_logger()


def configure_logging() -> None:
    """
    Configures the logging for the application using a GCP-friendly JSON format.
    """
    # Convert the logging level from string to the corresponding logging level
    logging_level = getattr(logging, settings.logging_level.upper(), logging.INFO)

    structlog.configure(
        processors=structlog_gcp.build_processors(service="scraper"),
        wrapper_class=structlog.make_filtering_bound_logger(logging_level),
    )
