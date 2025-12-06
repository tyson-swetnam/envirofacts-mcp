"""EPA Envirofacts API client."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx

from .config import settings
from .models import EPAQueryRequest, EPAQueryResponse, OutputFormat
from .query_builder import EPAQueryBuilder

logger = logging.getLogger(__name__)


class EPAAPIError(Exception):
    """Exception for EPA API errors."""

    pass


class EPAAPIClient:
    """Client for interacting with EPA Envirofacts API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
    ):
        """Initialize EPA API client.

        Args:
            base_url: Base URL for EPA API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url or settings.epa_api_base_url
        self.timeout = timeout or settings.epa_request_timeout
        self.max_retries = max_retries or settings.epa_max_retries
        self.query_builder = EPAQueryBuilder(base_url=self.base_url)

    async def execute_query(self, request: EPAQueryRequest) -> EPAQueryResponse:
        """Execute an EPA API query.

        Args:
            request: Query request specification

        Returns:
            Query response with data

        Raises:
            EPAAPIError: If query fails after retries
        """
        query_url = self.query_builder.build_from_request(request)
        logger.info(f"Executing EPA query: {query_url}")

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(query_url)
                    response.raise_for_status()

                    # Parse response based on format
                    if request.output_format == OutputFormat.JSON:
                        data = response.json()
                    elif request.output_format == OutputFormat.CSV:
                        # For CSV, return as text
                        data = [{"csv_data": response.text}]
                    elif request.output_format == OutputFormat.XML:
                        # For XML, return as text
                        data = [{"xml_data": response.text}]
                    else:
                        data = response.json()

                    # Handle EPA API returning empty list or error
                    if not data:
                        data = []

                    return EPAQueryResponse(
                        success=True,
                        data=data,
                        record_count=len(data),
                        query_url=query_url,
                        metadata={
                            "table": request.table_name,
                            "format": request.output_format.value,
                        },
                    )

            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    return EPAQueryResponse(
                        success=False,
                        data=[],
                        record_count=0,
                        query_url=query_url,
                        error_message=f"HTTP error: {e.response.status_code} - {e.response.text}",
                    )
                await asyncio.sleep(2**attempt)  # Exponential backoff

            except httpx.RequestError as e:
                logger.warning(f"Request error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    return EPAQueryResponse(
                        success=False,
                        data=[],
                        record_count=0,
                        query_url=query_url,
                        error_message=f"Request error: {str(e)}",
                    )
                await asyncio.sleep(2**attempt)

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return EPAQueryResponse(
                    success=False,
                    data=[],
                    record_count=0,
                    query_url=query_url,
                    error_message=f"Unexpected error: {str(e)}",
                )

        # Should not reach here
        return EPAQueryResponse(
            success=False,
            data=[],
            record_count=0,
            query_url=query_url,
            error_message="Max retries exceeded",
        )

    async def query_table(
        self,
        table_name: str,
        filters: Optional[Dict[str, str]] = None,
        row_limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query an EPA table with simple filters.

        Args:
            table_name: Name of the table to query
            filters: Dictionary of column:value filters
            row_limit: Maximum rows to return

        Returns:
            List of records

        Raises:
            EPAAPIError: If query fails
        """
        from .models import QueryFilter

        filter_list = []
        if filters:
            for column, value in filters.items():
                filter_list.append(QueryFilter(column=column, value=str(value)))

        request = EPAQueryRequest(
            table_name=table_name,
            filters=filter_list if filter_list else None,
            row_limit=row_limit,
        )

        response = await self.execute_query(request)

        if not response.success:
            raise EPAAPIError(response.error_message or "Query failed")

        return response.data
