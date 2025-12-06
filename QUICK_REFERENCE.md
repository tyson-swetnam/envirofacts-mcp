# EPA Envirofacts MCP Tool - Quick Reference

## Installation

```bash
pip install -r requirements.txt
```

## Start Server

```bash
python -m src.server
# or
python run_server.py
```

## 6 Available Tools

| Tool | Purpose | Required Params |
|------|---------|----------------|
| `query_epa_data` | General EPA queries | `table_name` |
| `search_superfund_sites` | Find Superfund sites | None (all optional) |
| `search_facilities` | Search facilities | None (all optional) |
| `get_air_quality` | Air quality data | `state` |
| `get_water_quality` | Water quality data | `state` |
| `get_compliance_violations` | Find violations | None (all optional) |

## Common EPA Tables

- `SEMS_SITES` - Superfund sites
- `FRS_FACILITIES` - Facilities
- `AQS_SITES` - Air quality sites
- `NPDES_PERMITS` - Water permits
- `TRI_FACILITY` - Toxic release facilities
- `RCRA_FACILITY` - Hazardous waste
- `NPDES_QNCR_HISTORY` - Water violations

## Filter Operators

- `=` Equal (default)
- `!=` Not equal
- `>` Greater than
- `<` Less than
- `BEGINNING` Starts with
- `CONTAINING` Contains

## Example Queries

### Search Superfund Sites in California
```json
{
  "state": "CA",
  "row_limit": 25
}
```

### Find Facilities with "Chemical" in Name
```json
{
  "facility_name": "Chemical",
  "state": "TX"
}
```

### Air Quality Sites in California
```json
{
  "state": "CA",
  "parameter_code": "44201"
}
```

### Custom Table Query
```json
{
  "table_name": "TRI_FACILITY",
  "filters": [
    {"column": "state_code", "value": "NY"}
  ]
}
```

## Response Format

```json
{
  "success": true,
  "record_count": 42,
  "data": [...],
  "query_url": "https://...",
  "error": null
}
```

## State Codes

Use 2-letter codes: CA, NY, TX, FL, IL, etc.

## Air Quality Parameter Codes

- `44201` - Ozone
- `88101` - PM2.5
- `81102` - PM10
- `42101` - Carbon monoxide
- `42602` - Nitrogen dioxide

## Resources

- [USAGE.md](USAGE.md) - Full usage guide
- [EPA API Docs](https://www.epa.gov/enviro/envirofacts-data-service-api-v1)
- [examples/](examples/) - Sample queries
