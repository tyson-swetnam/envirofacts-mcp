# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) tool that provides a bridge between Claude and the EPA Envirofacts Data Service API. The tool enables natural language queries about environmental data, superfund sites, hazardous waste facilities, and contamination information.

**EPA API Base URL**: https://www.epa.gov/enviro/envirofacts-data-service-api-v1
**No authentication required** for public API access.

## Specialized Agent

This repository includes a specialized Claude Code agent for EPA data queries:

**epa-data-specialist**: Automatically handles EPA Envirofacts API queries, data extraction, and environmental data interpretation. This agent should be used for:
- Constructing EPA API queries
- Retrieving environmental data (air quality, water quality, superfund sites, etc.)
- Interpreting EPA data structures and regulatory context
- Searching for facilities, violations, or contamination records

The agent is automatically available in Claude Code and will be suggested when EPA-related tasks are detected.

## Project Structure

The README describes the intended structure:
- `src/` - MCP tool implementation, API client, and utilities
- `tests/` - Test files for API client
- `examples/` - Sample queries and usage examples

## EPA Data Systems

The Envirofacts API provides access to multiple EPA data systems:
- **AQS** (Air Quality System): Ambient air monitoring data
- **ICIS** (Integrated Compliance Information System): Enforcement and compliance
- **RCRAInfo**: Hazardous waste handler and activity data
- **TRI** (Toxics Release Inventory): Toxic chemical releases
- **SDWA** (Safe Drinking Water): Public water system data
- **FRS** (Facility Registry System): Facility identification and location
- **GHG** (Greenhouse Gas): Emissions reporting

## API Query Format

EPA Envirofacts queries follow this pattern:
```
https://data.epa.gov/efservice/{table_name}/{search_columns}/{output_format}
```

Key query elements:
- Column filters: `/column_name/value`
- Operators: `/BEGINNING`, `/CONTAINING`, `/=`, `/>`, `/<`, `/!=`
- Row limits: `/rows/0:1000`
- Output formats: JSON, XML, CSV

## Implementation Considerations

When building API integrations:
- Handle pagination for large result sets
- Implement error handling for invalid queries, rate limits, and timeouts
- Validate and transform data responses
- Support multiple data formats (JSON, XML, CSV)
- Use state/county FIPS codes for reliable geographic filtering
- Start with FRS facility lookups when searching by location

## Related Documentation

- [EPA Envirofacts Data Service API](https://www.epa.gov/enviro/envirofacts-data-service-api-v1)
- [EPA Environmental Data Portal](https://www.epa.gov/enviro/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
