# EPA Envirofacts MCP Tool - Usage Guide

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd superfund-dust
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env if you need custom settings
```

## Running the MCP Server

The MCP server can be run directly or configured with Claude Desktop/CLI.

### Direct Execution

```bash
python -m src.server
```

### Configuration with Claude Desktop

Add to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "epa-envirofacts": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/superfund-dust"
    }
  }
}
```

### Configuration with Claude CLI

Add to your MCP settings file:

```json
{
  "epa-envirofacts": {
    "command": "python -m src.server",
    "workingDirectory": "/path/to/superfund-dust"
  }
}
```

## Available Tools

### 1. query_epa_data

General-purpose EPA data query for any table.

**Parameters**:
- `table_name` (required): EPA table name
- `filters` (optional): Array of filter objects
- `output_format` (optional): JSON, XML, or CSV
- `row_limit` (optional): Max rows (default: 100)

**Example**:
```json
{
  "table_name": "TRI_FACILITY",
  "filters": [
    {"column": "state_code", "value": "CA"},
    {"column": "industry_sector", "value": "Manufacturing", "operator": "CONTAINING"}
  ],
  "row_limit": 50
}
```

### 2. search_superfund_sites

Search for Superfund (NPL) sites.

**Parameters**:
- `state` (optional): Two-letter state code
- `county` (optional): County name
- `zip_code` (optional): ZIP code
- `site_name` (optional): Site name (partial match)
- `status` (optional): Site status
- `row_limit` (optional): Max rows

**Example**:
```json
{
  "state": "CA",
  "site_name": "Mining",
  "row_limit": 25
}
```

### 3. search_facilities

Search EPA-registered facilities.

**Parameters**:
- `facility_name` (optional): Name (partial match)
- `state` (optional): State code
- `zip_code` (optional): ZIP code
- `industry_code` (optional): SIC/NAICS code
- `row_limit` (optional): Max rows

**Example**:
```json
{
  "facility_name": "Chemical",
  "state": "TX",
  "row_limit": 20
}
```

### 4. get_air_quality

Retrieve air quality monitoring data.

**Parameters**:
- `state` (required): State code
- `county` (optional): County code
- `parameter_code` (optional): Pollutant code (44201=Ozone, 88101=PM2.5)
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `row_limit` (optional): Max rows

**Example**:
```json
{
  "state": "CA",
  "parameter_code": "44201",
  "row_limit": 50
}
```

### 5. get_water_quality

Get water quality and discharge data.

**Parameters**:
- `state` (required): State code
- `facility_id` (optional): NPDES permit number
- `pollutant` (optional): Pollutant name
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `row_limit` (optional): Max rows

**Example**:
```json
{
  "state": "FL",
  "pollutant": "nitrogen"
}
```

### 6. get_compliance_violations

Search environmental violations.

**Parameters**:
- `state` (optional): State code
- `facility_name` (optional): Name (partial match)
- `violation_type` (optional): Violation type
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `row_limit` (optional): Max rows

**Example**:
```json
{
  "state": "IL",
  "facility_name": "Steel",
  "row_limit": 30
}
```

## Common EPA Tables

- **SEMS_SITES**: Superfund sites
- **FRS_FACILITIES**: Facility registry
- **AQS_SITES**: Air quality monitoring sites
- **NPDES_PERMITS**: Water discharge permits
- **TRI_FACILITY**: Toxic release inventory
- **RCRA_FACILITY**: Hazardous waste facilities
- **GHG_EMITTERS**: Greenhouse gas emitters
- **NPDES_QNCR_HISTORY**: Water violations
- **ICIS_FACILITIES**: Compliance tracking

## Filter Operators

- `=` - Equal (default)
- `!=` - Not equal
- `>` - Greater than
- `<` - Less than
- `BEGINNING` - Starts with
- `CONTAINING` - Contains substring

## Response Format

All tools return JSON with this structure:

```json
{
  "success": true,
  "record_count": 42,
  "data": [...],
  "query_url": "https://data.epa.gov/efservice/...",
  "error": null,
  "metadata": {
    "table": "SEMS_SITES",
    "format": "JSON"
  }
}
```

## Tips & Best Practices

1. **Start with small row limits** when exploring data
2. **Use state codes** (two letters) not full state names
3. **Check the query_url** in responses to debug issues
4. **Use CONTAINING operator** for partial text matches
5. **Combine filters** to narrow results effectively
6. **Reference EPA documentation** for table schemas and codes

## Troubleshooting

### Empty Results
- Verify state codes are uppercase two-letter abbreviations
- Check that column names match EPA table schema
- Try broader filters (use CONTAINING instead of exact match)
- Increase row_limit in case data exists beyond default

### Timeout Errors
- Reduce row_limit for large datasets
- Add more specific filters to narrow results
- Check EPA API status (may be temporarily unavailable)

### Invalid Table Names
- Verify table name spelling and capitalization
- Consult EPA Envirofacts documentation for valid tables
- Use query_epa_data for custom tables

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_query_builder.py
```

## Running Examples

```bash
# Run sample queries
python -m examples.sample_queries
```

## Additional Resources

- [EPA Envirofacts API Documentation](https://www.epa.gov/enviro/envirofacts-data-service-api-v1)
- [EPA Data Dictionary](https://www.epa.gov/enviro/envirofacts-data-dictionary)
- [MCP Documentation](https://modelcontextprotocol.io/)
