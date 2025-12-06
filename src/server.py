"""EPA Envirofacts MCP Server."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import EPATools

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("epa-envirofacts-mcp")

# Create server instance
app = Server("epa-envirofacts-mcp")

# Create tools instance
epa_tools = EPATools()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available EPA tools."""
    return [
        Tool(
            name="query_epa_data",
            description="""Query any EPA Envirofacts table with custom filters.

            Use this for general-purpose EPA data queries when you know the specific table name.
            Supports multiple filter operators (=, !=, >, <, BEGINNING, CONTAINING).

            Example tables: SEMS_SITES, FRS_FACILITIES, AQS_SITES, NPDES_PERMITS, TRI_FACILITY""",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the EPA table to query (e.g., SEMS_SITES, FRS_FACILITIES)",
                    },
                    "filters": {
                        "type": "array",
                        "description": "List of filters to apply",
                        "items": {
                            "type": "object",
                            "properties": {
                                "column": {"type": "string", "description": "Column name"},
                                "value": {"type": "string", "description": "Value to match"},
                                "operator": {
                                    "type": "string",
                                    "enum": ["=", "!=", ">", "<", "BEGINNING", "CONTAINING"],
                                    "default": "=",
                                    "description": "Comparison operator",
                                },
                            },
                            "required": ["column", "value"],
                        },
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["JSON", "XML", "CSV"],
                        "default": "JSON",
                    },
                    "row_limit": {"type": "integer", "default": 100, "minimum": 1, "maximum": 10000},
                },
                "required": ["table_name"],
            },
        ),
        Tool(
            name="search_superfund_sites",
            description="""Search for Superfund (NPL) sites by location or name.

            Superfund sites are contaminated locations requiring long-term cleanup.
            Search by state, county, ZIP code, site name, or status.

            Common statuses: Proposed, Final, Deleted, Removed""",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Two-letter state code (e.g., CA, NY, TX)",
                    },
                    "county": {"type": "string", "description": "County name"},
                    "zip_code": {"type": "string", "description": "ZIP code"},
                    "site_name": {
                        "type": "string",
                        "description": "Site name (partial match supported)",
                    },
                    "status": {"type": "string", "description": "Site status"},
                    "row_limit": {"type": "integer", "default": 100, "minimum": 1, "maximum": 10000},
                },
            },
        ),
        Tool(
            name="search_facilities",
            description="""Search for facilities in the EPA Facility Registry System.

            Find industrial facilities, waste handlers, and regulated entities.
            Search by name, location, or industry code (SIC/NAICS).

            The FRS is a comprehensive database of all EPA-regulated facilities.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_name": {
                        "type": "string",
                        "description": "Facility name (partial match)",
                    },
                    "state": {"type": "string", "description": "Two-letter state code"},
                    "zip_code": {"type": "string", "description": "ZIP code"},
                    "industry_code": {
                        "type": "string",
                        "description": "SIC or NAICS industry code",
                    },
                    "row_limit": {"type": "integer", "default": 100, "minimum": 1, "maximum": 10000},
                },
            },
        ),
        Tool(
            name="get_air_quality",
            description="""Get air quality monitoring data from EPA's Air Quality System (AQS).

            Retrieve ambient air monitoring data including criteria pollutants (ozone, PM2.5, PM10, etc.).
            Data comes from monitoring stations across the US.

            Common parameter codes: 44201 (Ozone), 88101 (PM2.5), 81102 (PM10)""",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Two-letter state code (required)",
                    },
                    "county": {"type": "string", "description": "County code"},
                    "parameter_code": {
                        "type": "string",
                        "description": "Pollutant parameter code (e.g., 44201 for ozone)",
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format",
                    },
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"},
                    "row_limit": {"type": "integer", "default": 100, "minimum": 1, "maximum": 10000},
                },
                "required": ["state"],
            },
        ),
        Tool(
            name="get_water_quality",
            description="""Get water quality and discharge data from EPA's NPDES program.

            Retrieve data on wastewater discharges, permit compliance, and water quality monitoring.
            NPDES (National Pollutant Discharge Elimination System) regulates point source discharges.

            Includes industrial and municipal wastewater discharge data.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Two-letter state code (required)",
                    },
                    "facility_id": {"type": "string", "description": "NPDES permit number"},
                    "pollutant": {"type": "string", "description": "Pollutant name or code"},
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format",
                    },
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"},
                    "row_limit": {"type": "integer", "default": 100, "minimum": 1, "maximum": 10000},
                },
                "required": ["state"],
            },
        ),
        Tool(
            name="get_compliance_violations",
            description="""Get environmental compliance violations and enforcement actions.

            Search for facilities with violations of environmental regulations.
            Includes Clean Water Act, Clean Air Act, and RCRA violations.

            Useful for identifying non-compliant facilities and enforcement history.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {"type": "string", "description": "Two-letter state code"},
                    "facility_name": {
                        "type": "string",
                        "description": "Facility name (partial match)",
                    },
                    "violation_type": {"type": "string", "description": "Type of violation"},
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format",
                    },
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"},
                    "row_limit": {"type": "integer", "default": 100, "minimum": 1, "maximum": 10000},
                },
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        logger.info(f"Tool called: {name} with arguments: {arguments}")

        if name == "query_epa_data":
            result = await epa_tools.query_epa_data(**arguments)
        elif name == "search_superfund_sites":
            result = await epa_tools.search_superfund_sites(**arguments)
        elif name == "search_facilities":
            result = await epa_tools.search_facilities(**arguments)
        elif name == "get_air_quality":
            result = await epa_tools.get_air_quality(**arguments)
        elif name == "get_water_quality":
            result = await epa_tools.get_water_quality(**arguments)
        elif name == "get_compliance_violations":
            result = await epa_tools.get_compliance_violations(**arguments)
        else:
            result = f'{{"success": false, "error": "Unknown tool: {name}"}}'

        return [TextContent(type="text", text=result)]

    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return [TextContent(type="text", text=f'{{"success": false, "error": "{str(e)}"}}')]


async def main():
    """Run the MCP server."""
    logger.info("Starting EPA Envirofacts MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
