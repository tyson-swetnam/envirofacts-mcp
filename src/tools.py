"""Tool implementations for EPA Envirofacts MCP server."""

import json
import logging
from typing import Any, Dict, List, Optional

from .epa_api_client import EPAAPIClient
from .models import (
    AirQualitySearch,
    EPAQueryRequest,
    FacilitySearch,
    OutputFormat,
    QueryFilter,
    QueryOperator,
    SuperfundSiteSearch,
    ViolationSearch,
    WaterQualitySearch,
)

logger = logging.getLogger(__name__)


class EPATools:
    """EPA Envirofacts tool implementations."""

    def __init__(self):
        """Initialize EPA tools."""
        self.client = EPAAPIClient()

    async def query_epa_data(
        self,
        table_name: str,
        filters: Optional[List[Dict[str, str]]] = None,
        output_format: str = "JSON",
        row_limit: int = 100,
    ) -> str:
        """Query EPA data from any table.

        Args:
            table_name: Name of the EPA table to query
            filters: List of filter dictionaries with 'column', 'value', and optional 'operator'
            output_format: Output format (JSON, XML, CSV)
            row_limit: Maximum rows to return

        Returns:
            JSON string with query results
        """
        try:
            # Build filter list
            filter_list = []
            if filters:
                for f in filters:
                    operator = QueryOperator(f.get("operator", "="))
                    filter_list.append(
                        QueryFilter(column=f["column"], value=f["value"], operator=operator)
                    )

            # Create request
            request = EPAQueryRequest(
                table_name=table_name,
                filters=filter_list if filter_list else None,
                output_format=OutputFormat(output_format),
                row_limit=row_limit,
            )

            # Execute query
            response = await self.client.execute_query(request)

            return json.dumps(
                {
                    "success": response.success,
                    "record_count": response.record_count,
                    "data": response.data,
                    "query_url": response.query_url,
                    "error": response.error_message,
                },
                indent=2,
            )

        except Exception as e:
            logger.error(f"Error in query_epa_data: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    async def search_superfund_sites(
        self,
        state: Optional[str] = None,
        county: Optional[str] = None,
        zip_code: Optional[str] = None,
        site_name: Optional[str] = None,
        status: Optional[str] = None,
        row_limit: int = 100,
    ) -> str:
        """Search for Superfund (NPL) sites.

        Args:
            state: Two-letter state code
            county: County name
            zip_code: ZIP code
            site_name: Site name (partial match supported)
            status: Site status
            row_limit: Maximum results

        Returns:
            JSON string with Superfund sites
        """
        try:
            # Build filters based on provided parameters
            filters = []

            if state:
                filters.append(QueryFilter(column="state_code", value=state.upper()))

            if county:
                filters.append(
                    QueryFilter(column="county_name", value=county, operator=QueryOperator.CONTAINING)
                )

            if zip_code:
                filters.append(QueryFilter(column="zip", value=zip_code))

            if site_name:
                filters.append(
                    QueryFilter(column="site_name", value=site_name, operator=QueryOperator.CONTAINING)
                )

            if status:
                filters.append(QueryFilter(column="status", value=status))

            # Query SEMS_SITES table (Superfund Enterprise Management System)
            request = EPAQueryRequest(
                table_name="SEMS_SITES",
                filters=filters if filters else None,
                output_format=OutputFormat.JSON,
                row_limit=row_limit,
            )

            response = await self.client.execute_query(request)

            return json.dumps(
                {
                    "success": response.success,
                    "record_count": response.record_count,
                    "sites": response.data,
                    "query_url": response.query_url,
                    "error": response.error_message,
                },
                indent=2,
            )

        except Exception as e:
            logger.error(f"Error in search_superfund_sites: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    async def search_facilities(
        self,
        facility_name: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        industry_code: Optional[str] = None,
        row_limit: int = 100,
    ) -> str:
        """Search for facilities in the Facility Registry System.

        Args:
            facility_name: Facility name (partial match)
            state: Two-letter state code
            zip_code: ZIP code
            industry_code: SIC or NAICS industry code
            row_limit: Maximum results

        Returns:
            JSON string with facilities
        """
        try:
            filters = []

            if facility_name:
                filters.append(
                    QueryFilter(
                        column="primary_name", value=facility_name, operator=QueryOperator.CONTAINING
                    )
                )

            if state:
                filters.append(QueryFilter(column="state_code", value=state.upper()))

            if zip_code:
                filters.append(QueryFilter(column="postal_code", value=zip_code))

            if industry_code:
                filters.append(QueryFilter(column="sic_code", value=industry_code))

            # Query FRS_FACILITIES table
            request = EPAQueryRequest(
                table_name="FRS_FACILITIES",
                filters=filters if filters else None,
                output_format=OutputFormat.JSON,
                row_limit=row_limit,
            )

            response = await self.client.execute_query(request)

            return json.dumps(
                {
                    "success": response.success,
                    "record_count": response.record_count,
                    "facilities": response.data,
                    "query_url": response.query_url,
                    "error": response.error_message,
                },
                indent=2,
            )

        except Exception as e:
            logger.error(f"Error in search_facilities: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    async def get_air_quality(
        self,
        state: str,
        county: Optional[str] = None,
        parameter_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        row_limit: int = 100,
    ) -> str:
        """Get air quality monitoring data.

        Args:
            state: Two-letter state code (required)
            county: County code
            parameter_code: Pollutant parameter code
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            row_limit: Maximum results

        Returns:
            JSON string with air quality data
        """
        try:
            filters = [QueryFilter(column="state_code", value=state.upper())]

            if county:
                filters.append(QueryFilter(column="county_code", value=county))

            if parameter_code:
                filters.append(QueryFilter(column="parameter_code", value=parameter_code))

            if start_date:
                filters.append(
                    QueryFilter(column="sample_date", value=start_date, operator=QueryOperator.GREATER_THAN)
                )

            # Query AQS_SITES or AQS_ANNUAL_SUMMARIES table
            request = EPAQueryRequest(
                table_name="AQS_SITES",
                filters=filters,
                output_format=OutputFormat.JSON,
                row_limit=row_limit,
            )

            response = await self.client.execute_query(request)

            return json.dumps(
                {
                    "success": response.success,
                    "record_count": response.record_count,
                    "air_quality_data": response.data,
                    "query_url": response.query_url,
                    "error": response.error_message,
                },
                indent=2,
            )

        except Exception as e:
            logger.error(f"Error in get_air_quality: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    async def get_water_quality(
        self,
        state: str,
        facility_id: Optional[str] = None,
        pollutant: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        row_limit: int = 100,
    ) -> str:
        """Get water quality and discharge data.

        Args:
            state: Two-letter state code (required)
            facility_id: NPDES permit number
            pollutant: Pollutant name or code
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            row_limit: Maximum results

        Returns:
            JSON string with water quality data
        """
        try:
            filters = [QueryFilter(column="state_code", value=state.upper())]

            if facility_id:
                filters.append(QueryFilter(column="npdes_id", value=facility_id))

            if pollutant:
                filters.append(
                    QueryFilter(column="pollutant_desc", value=pollutant, operator=QueryOperator.CONTAINING)
                )

            # Query ICIS-NPDES table
            request = EPAQueryRequest(
                table_name="NPDES_PERMITS",
                filters=filters,
                output_format=OutputFormat.JSON,
                row_limit=row_limit,
            )

            response = await self.client.execute_query(request)

            return json.dumps(
                {
                    "success": response.success,
                    "record_count": response.record_count,
                    "water_quality_data": response.data,
                    "query_url": response.query_url,
                    "error": response.error_message,
                },
                indent=2,
            )

        except Exception as e:
            logger.error(f"Error in get_water_quality: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    async def get_compliance_violations(
        self,
        state: Optional[str] = None,
        facility_name: Optional[str] = None,
        violation_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        row_limit: int = 100,
    ) -> str:
        """Get environmental compliance violations.

        Args:
            state: Two-letter state code
            facility_name: Facility name (partial match)
            violation_type: Type of violation
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            row_limit: Maximum results

        Returns:
            JSON string with violation data
        """
        try:
            filters = []

            if state:
                filters.append(QueryFilter(column="state_code", value=state.upper()))

            if facility_name:
                filters.append(
                    QueryFilter(
                        column="facility_name", value=facility_name, operator=QueryOperator.CONTAINING
                    )
                )

            if violation_type:
                filters.append(
                    QueryFilter(
                        column="violation_type", value=violation_type, operator=QueryOperator.CONTAINING
                    )
                )

            # Query ICIS_VIOLATIONS or NPDES_QNCR_HISTORY table
            request = EPAQueryRequest(
                table_name="NPDES_QNCR_HISTORY",
                filters=filters if filters else None,
                output_format=OutputFormat.JSON,
                row_limit=row_limit,
            )

            response = await self.client.execute_query(request)

            return json.dumps(
                {
                    "success": response.success,
                    "record_count": response.record_count,
                    "violations": response.data,
                    "query_url": response.query_url,
                    "error": response.error_message,
                },
                indent=2,
            )

        except Exception as e:
            logger.error(f"Error in get_compliance_violations: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)
