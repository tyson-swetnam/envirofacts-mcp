"""Query builder for EPA Envirofacts API."""

from typing import List, Optional
from urllib.parse import urljoin

from .config import settings
from .models import EPAQueryRequest, OutputFormat, QueryFilter


class EPAQueryBuilder:
    """Build EPA Envirofacts API query URLs."""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize query builder.

        Args:
            base_url: Base URL for EPA API. Uses settings default if not provided.
        """
        self.base_url = base_url or settings.epa_api_base_url

    def build_query_url(
        self,
        table_name: str,
        filters: Optional[List[QueryFilter]] = None,
        output_format: OutputFormat = OutputFormat.JSON,
        row_limit: int = 100,
        offset: int = 0,
    ) -> str:
        """Build a complete EPA API query URL.

        Args:
            table_name: Name of the EPA table to query
            filters: List of query filters to apply
            output_format: Desired output format (JSON, XML, CSV)
            row_limit: Maximum number of rows to return
            offset: Starting row offset for pagination

        Returns:
            Complete query URL
        """
        # Start with table name
        path_parts = [table_name]

        # Add filters
        if filters:
            for filter_item in filters:
                path_parts.append(filter_item.column)
                if filter_item.operator.value in ["=", "!=", ">", "<"]:
                    path_parts.append(f"{filter_item.operator.value}{filter_item.value}")
                else:
                    # For BEGINNING and CONTAINING
                    path_parts.append(f"/{filter_item.operator.value}/{filter_item.value}")

        # Add pagination
        if offset > 0:
            path_parts.append(f"rows/{offset}:{offset + row_limit}")
        else:
            path_parts.append(f"rows/0:{row_limit}")

        # Add output format
        path_parts.append(output_format.value)

        # Join all parts
        path = "/".join(path_parts)
        return urljoin(self.base_url + "/", path)

    def build_from_request(self, request: EPAQueryRequest) -> str:
        """Build query URL from a request model.

        Args:
            request: EPA query request object

        Returns:
            Complete query URL
        """
        return self.build_query_url(
            table_name=request.table_name,
            filters=request.filters,
            output_format=request.output_format,
            row_limit=request.row_limit,
            offset=request.offset,
        )

    def build_simple_query(
        self,
        table_name: str,
        column: str,
        value: str,
        output_format: OutputFormat = OutputFormat.JSON,
        row_limit: int = 100,
    ) -> str:
        """Build a simple single-filter query.

        Args:
            table_name: Name of the EPA table
            column: Column name to filter on
            value: Value to match
            output_format: Output format
            row_limit: Max rows

        Returns:
            Complete query URL
        """
        filter_item = QueryFilter(column=column, value=value)
        return self.build_query_url(
            table_name=table_name,
            filters=[filter_item],
            output_format=output_format,
            row_limit=row_limit,
        )
