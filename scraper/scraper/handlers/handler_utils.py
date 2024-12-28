import json
from typing import Optional

import structlog
import uuid6
from crawlee._request import Request

from scraper.utils.bucket_utils import upload_string_to_gcs

logger = structlog.get_logger()


class HandlerDependencies:
    """
    Utility class for handling scraper responses.

    Attributes:
        bucket: The GCS bucket used for storing scraped data.
        response_dao: The Data Access Object for interacting with the scrape response database.
        extractor_dao: The Data Access Object for interacting with the scrape extraction database.
    """

    def __init__(self, bucket, response_dao, extractor_dao):
        self.bucket = bucket
        self.response_dao = response_dao
        self.extractor_dao = extractor_dao

    def save_to_gcs(self, content, building_id) -> uuid6.UUID:
        """
        Creates the file_id and Saves the given content to Google Cloud Storage (GCS) and returns the file ID.

        Args:
            content: The content to be saved to GCS.
            building_id: The ID of the building associated with the content.

        Returns:
            uuid6.UUID: The unique identifier of the saved file.
        """
        file_id = uuid6.uuid8()
        filename = f"{file_id}.json"
        upload_string_to_gcs(self.bucket, json.dumps(content), filename, building_id)
        return file_id

    async def save_scrape_response(
        self, request: Request, cleaned_content
    ) -> Optional[int]:
        building_id = request.user_data.model_extra.get("building_id")
        # Should i use this object instead of a dict?
        # ScrapeResponse(
        #     request.url,
        #     request.loaded_url,
        #     building_id,
        #     request.retry_count,
        #     cleaned_content
        #     )
        scrape_response = {
            "metadata": {
                "requested_url": request.url,
                "loaded_url": request.loaded_url,
                "building_id": building_id,
                "retry_count": request.retry_count,
            },
            "content": cleaned_content,
        }

        try:
            file_id = self.save_to_gcs(scrape_response, building_id)
            scrape_response_id = await self.response_dao.add_scrape_response(
                scrape_response, file_id
            )
            logger.info(
                "Scrape response saved to GCP.",
                scrape_response_id=scrape_response_id,
                url=request.url,
                building_id=building_id,
                file_id=file_id,
            )
            return scrape_response_id
        except Exception as e:
            # We won't raise an error bc then crawlee will retry the request.
            logger.error(
                "Failed to save scrape response to GCP.",
                url={request.url},
                building_id=building_id,
                error=str(e),
            )
            return None
