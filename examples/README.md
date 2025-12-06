# EPA Envirofacts MCP Tool - Examples

This directory contains example queries and usage patterns for the EPA Envirofacts MCP tool.

## Running Examples

```bash
# From the project root
python -m examples.sample_queries
```

## Example Queries

### 1. Search Superfund Sites

Find Superfund sites in a specific state:

```python
result = await tools.search_superfund_sites(state="CA", row_limit=10)
```

Search by site name (partial match):

```python
result = await tools.search_superfund_sites(
    site_name="Mining",
    status="Final"
)
```

### 2. Search Facilities

Find facilities by name:

```python
result = await tools.search_facilities(
    facility_name="Chemical",
    state="TX"
)
```

Search by location:

```python
result = await tools.search_facilities(
    zip_code="90210",
    row_limit=20
)
```

### 3. Air Quality Data

Get air quality monitoring sites:

```python
result = await tools.get_air_quality(
    state="CA",
    parameter_code="44201",  # Ozone
    row_limit=50
)
```

### 4. Water Quality Data

Get NPDES permits:

```python
result = await tools.get_water_quality(
    state="FL",
    pollutant="nitrogen"
)
```

### 5. General EPA Queries

Query any EPA table:

```python
result = await tools.query_epa_data(
    table_name="TRI_FACILITY",
    filters=[
        {"column": "state_code", "value": "NY"},
        {"column": "industry_sector", "value": "Manufacturing", "operator": "CONTAINING"}
    ],
    row_limit=100
)
```

### 6. Compliance Violations

Search for violations:

```python
result = await tools.get_compliance_violations(
    state="IL",
    facility_name="Steel",
    row_limit=25
)
```

## Common EPA Tables

- **SEMS_SITES**: Superfund sites
- **FRS_FACILITIES**: Facility Registry
- **AQS_SITES**: Air quality monitoring sites
- **NPDES_PERMITS**: Water discharge permits
- **TRI_FACILITY**: Toxic Release Inventory facilities
- **NPDES_QNCR_HISTORY**: Water quality violations
- **RCRA_FACILITY**: Hazardous waste facilities

## Response Format

All tools return JSON with this structure:

```json
{
  "success": true,
  "record_count": 42,
  "data": [...],
  "query_url": "https://data.epa.gov/efservice/...",
  "error": null
}
```

## Tips

- Use row_limit to control response size (default: 100, max: 10000)
- State codes must be two-letter abbreviations (e.g., "CA", "NY")
- Partial matches use the CONTAINING operator
- Check query_url in responses to see the actual EPA API call
