# Development Plan: EPA Envirofacts MCP Tool

## Project Goal

Create a Model Context Protocol (MCP) server that enables Claude to query and retrieve environmental data from the EPA Envirofacts Data Service API through natural language interactions.

## Overview

This MCP tool will bridge Claude and the EPA Envirofacts API, allowing users to:
- Query environmental data using natural language
- Search for Superfund sites, hazardous waste facilities, and contamination records
- Retrieve air quality, water quality, and compliance information
- Access facility data and environmental violations

## Architecture

### MCP Server Components

1. **Server Implementation** (`src/mcp_server.py`)
   - MCP protocol handler
   - Tool registration and routing
   - Request/response formatting
   - Error handling and logging

2. **EPA API Client** (`src/epa_api_client.py`)
   - HTTP client for EPA Envirofacts API
   - Query construction and validation
   - Response parsing and normalization
   - Rate limiting and retry logic

3. **Data Models** (`src/models.py`)
   - Pydantic models for EPA data structures
   - Request validation schemas
   - Response data types
   - Type hints for all public interfaces

4. **Query Builder** (`src/query_builder.py`)
   - Natural language to API query translation
   - Parameter extraction and validation
   - Query optimization
   - Multi-table query support

5. **Utilities** (`src/utils.py`)
   - Data formatting helpers
   - Geographic code lookups (FIPS codes, ZIP codes)
   - Date/time handling
   - Response pagination

## MCP Tools to Implement

### 1. `query_epa_data`
**Purpose**: General-purpose EPA data query tool

**Inputs**:
- `data_system` (required): Which EPA system (AQS, ICIS, RCRAInfo, TRI, etc.)
- `table_name` (required): Specific table to query
- `filters` (optional): Dictionary of column/value filters
- `output_format` (optional): JSON, XML, or CSV (default: JSON)
- `row_limit` (optional): Maximum rows to return (default: 100)

**Output**: Structured environmental data from EPA

### 2. `search_superfund_sites`
**Purpose**: Specialized search for Superfund sites

**Inputs**:
- `state` (optional): Two-letter state code
- `county` (optional): County name
- `zip_code` (optional): ZIP code
- `site_name` (optional): Site name (partial match supported)
- `status` (optional): Site status filter

**Output**: List of Superfund sites with key details

### 3. `search_facilities`
**Purpose**: Find facilities by location or characteristics

**Inputs**:
- `facility_name` (optional): Facility name (partial match)
- `state` (optional): State code
- `zip_code` (optional): ZIP code
- `industry_code` (optional): SIC or NAICS code
- `latitude` (optional): Coordinate with radius
- `longitude` (optional): Coordinate with radius
- `radius_miles` (optional): Search radius

**Output**: Facility records from FRS

### 4. `get_air_quality`
**Purpose**: Retrieve air quality monitoring data

**Inputs**:
- `state` (required): State code
- `county` (optional): County code
- `parameter_code` (optional): Pollutant code (e.g., ozone, PM2.5)
- `start_date` (optional): Beginning of date range
- `end_date` (optional): End of date range

**Output**: Air quality measurements from AQS

### 5. `get_water_quality`
**Purpose**: Retrieve water quality and discharge data

**Inputs**:
- `state` (required): State code
- `facility_id` (optional): NPDES permit number
- `pollutant` (optional): Pollutant name or code
- `start_date` (optional): Beginning of date range
- `end_date` (optional): End of date range

**Output**: Water quality data from ICIS-NPDES

### 6. `get_compliance_violations`
**Purpose**: Search for environmental violations and enforcement

**Inputs**:
- `state` (optional): State code
- `facility_name` (optional): Facility name
- `violation_type` (optional): Type of violation
- `start_date` (optional): Beginning of date range
- `end_date` (optional): End of date range

**Output**: Compliance and enforcement records

## Implementation Phases

### Phase 1: Foundation (Week 1)

**Setup**:
- [ ] Initialize Python project with poetry or pip
- [ ] Install MCP SDK and dependencies
- [ ] Set up project structure (src/, tests/, examples/)
- [ ] Configure linting (ruff/black) and type checking (mypy)
- [ ] Create basic README and documentation

**Core Infrastructure**:
- [ ] Implement basic MCP server skeleton
- [ ] Create EPA API client with basic HTTP functionality
- [ ] Add logging and error handling framework
- [ ] Write configuration management (API base URL, timeouts, etc.)

**Deliverable**: Working MCP server that can start and accept connections

### Phase 2: Basic Query Functionality (Week 2)

**EPA API Integration**:
- [ ] Implement query builder for basic EPA API queries
- [ ] Add support for column filters and operators
- [ ] Implement response parsing for JSON format
- [ ] Add pagination handling

**MCP Tools**:
- [ ] Implement `query_epa_data` tool
- [ ] Add input validation and error messages
- [ ] Test with multiple EPA data systems
- [ ] Document query patterns and examples

**Testing**:
- [ ] Unit tests for query builder
- [ ] Integration tests with live EPA API
- [ ] Mock tests for offline development

**Deliverable**: Working general-purpose query tool

### Phase 3: Specialized Tools (Week 3)

**High-Level Tools**:
- [ ] Implement `search_superfund_sites`
- [ ] Implement `search_facilities`
- [ ] Implement `get_air_quality`
- [ ] Implement `get_water_quality`

**Data Enhancement**:
- [ ] Add geographic code lookup utilities (FIPS codes)
- [ ] Implement data normalization and formatting
- [ ] Add result filtering and sorting
- [ ] Create data summary capabilities

**Testing**:
- [ ] Test each specialized tool with real queries
- [ ] Validate data accuracy and completeness
- [ ] Performance testing with large result sets

**Deliverable**: Complete set of specialized query tools

### Phase 4: Advanced Features (Week 4)

**Enhancements**:
- [ ] Implement `get_compliance_violations`
- [ ] Add multi-table join capabilities
- [ ] Implement caching for frequently accessed data
- [ ] Add retry logic and rate limiting
- [ ] Support for XML and CSV output formats

**User Experience**:
- [ ] Improve error messages with helpful suggestions
- [ ] Add query validation with clear feedback
- [ ] Implement data export helpers
- [ ] Create usage examples and tutorials

**Testing**:
- [ ] End-to-end testing scenarios
- [ ] Error handling and edge cases
- [ ] Performance optimization
- [ ] Documentation review

**Deliverable**: Production-ready MCP tool

## Technical Specifications

### Dependencies

**Core**:
- `mcp` - Model Context Protocol SDK
- `httpx` - Modern HTTP client with async support
- `pydantic` - Data validation and settings

**Development**:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-httpx` - HTTP mocking
- `ruff` - Linting and formatting
- `mypy` - Type checking

### Configuration

**Environment Variables**:
- `EPA_API_BASE_URL` - Base URL for EPA API (default: https://data.epa.gov/efservice)
- `EPA_REQUEST_TIMEOUT` - Request timeout in seconds (default: 30)
- `EPA_MAX_RETRIES` - Maximum retry attempts (default: 3)
- `EPA_CACHE_TTL` - Cache time-to-live in seconds (default: 3600)
- `LOG_LEVEL` - Logging level (default: INFO)

### Data Handling

**Response Processing**:
1. Validate API response status
2. Parse response based on format (JSON/XML/CSV)
3. Normalize data structures
4. Apply pagination if needed
5. Format for MCP response
6. Include metadata (query time, record count, etc.)

**Error Handling**:
- Network errors: Retry with exponential backoff
- API errors: Parse error message and provide helpful context
- Validation errors: Return clear explanation of invalid parameters
- Rate limiting: Implement respectful backoff and inform user

### Query Optimization

**Best Practices**:
- Use row limits to prevent overwhelming responses
- Implement smart defaults for common queries
- Cache geographic lookups (state codes, FIPS codes)
- Batch related queries when possible
- Provide query preview/explanation before execution

## Testing Strategy

### Unit Tests
- Query builder logic
- Data parsing and normalization
- Filter construction
- Parameter validation
- Utility functions

### Integration Tests
- Live EPA API queries (limited to avoid rate limits)
- Response parsing for all supported formats
- Error handling with actual API errors
- Pagination across multiple pages

### End-to-End Tests
- Complete user workflows
- Natural language to query translation
- Multi-step data retrieval
- Error recovery scenarios

### Test Data
- Create fixtures for common EPA response formats
- Mock API responses for offline testing
- Test cases for edge cases and errors
- Performance benchmarks

## Documentation

### User Documentation
- Quick start guide
- Tool reference with examples
- Common query patterns
- Troubleshooting guide
- EPA data dictionary references

### Developer Documentation
- Architecture overview
- API client implementation
- Adding new tools
- Testing guidelines
- Contributing guide

### Examples
- Basic queries for each data system
- Complex multi-filter searches
- Geographic searches
- Time-series data retrieval
- Data export workflows

## Success Criteria

### Functionality
- [ ] All 6 MCP tools implemented and tested
- [ ] Successful queries across all major EPA data systems
- [ ] Proper error handling and user feedback
- [ ] Performance acceptable for typical queries (< 5 seconds)

### Quality
- [ ] 80%+ test coverage
- [ ] All tests passing
- [ ] Type hints on all public interfaces
- [ ] No critical linting errors

### Documentation
- [ ] Complete README with setup instructions
- [ ] Examples for all tools
- [ ] API reference documentation
- [ ] Troubleshooting guide

### User Experience
- [ ] Clear, actionable error messages
- [ ] Intuitive tool naming and parameters
- [ ] Helpful query suggestions
- [ ] Comprehensive examples

## Future Enhancements

**Potential Features**:
- Async query execution for better performance
- Query result caching and refresh
- Data visualization support
- Advanced filtering with boolean logic
- Saved queries and templates
- Data export to common formats (Excel, SQLite)
- Integration with other environmental APIs
- Geographic visualization support
- Trend analysis and aggregation tools
- Automated data quality checks

## Resources

- [EPA Envirofacts API Documentation](https://www.epa.gov/enviro/envirofacts-data-service-api-v1)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [EPA Data Dictionary](https://www.epa.gov/enviro/envirofacts-data-dictionary)
- [EPA Data Systems Overview](https://www.epa.gov/enviro/)

## Timeline

- **Week 1**: Foundation and infrastructure
- **Week 2**: Basic query functionality
- **Week 3**: Specialized tools
- **Week 4**: Advanced features and polish
- **Total**: 4 weeks to production-ready tool

## Notes

- EPA API has no authentication, simplifying implementation
- No official rate limits documented, but be respectful with requests
- Data freshness varies by system - some are near real-time, others updated quarterly
- Consider implementing local caching for frequently accessed reference data
- Test thoroughly with various geographic scopes and time ranges
- Document any API quirks or inconsistencies discovered during development
