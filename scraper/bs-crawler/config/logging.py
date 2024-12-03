# Copyright (c) 2024 BlackLocus, Inc. All rights reserved.

import logging

import structlog
import structlog_gcp

logger = structlog.get_logger()


def configure_logging() -> None:
    """
    Configures the logging for the application using a GCP-friendly JSON format.
    """
    structlog.configure(
        processors=structlog_gcp.build_processors(service="scraper"),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
