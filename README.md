# envirofacts-mcp

A Model Context Protocol (MCP) server for querying the EPA Envirofacts Data Service API. Get environmental data about Superfund sites, contamination records, air/water quality, and facility information directly in Claude.

## Quick Start with Claude Desktop

### 1. Clone and install

```bash
git clone <repository-url>
cd superfund-dust
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Claude Desktop

Add to your Claude Desktop config file:

| OS | Config file location |
|----|---------------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "envirofacts-mcp": {
      "command": "/absolute/path/to/superfund-dust/venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/absolute/path/to/superfund-dust"
    }
  }
}
```

**Important:** Replace `/absolute/path/to/superfund-dust` with your actual project path.

### 3. Restart Claude Desktop

The EPA tools will appear in your available tools (look for the 🔌 icon).

### 4. Start querying

Ask Claude:
- "Find all Superfund sites in California"
- "What are the air quality monitoring sites in New York?"
- "Show environmental violations in Texas"

---

## Running Locally as an MCP Server

### Option 1: Using the convenience script

```bash
source venv/bin/activate
python run_server.py
```

### Option 2: Running as a module

```bash
source venv/bin/activate
python -m src.server
```

The server communicates via stdio using the Model Context Protocol. It's designed to be launched by MCP clients (like Claude Desktop) rather than exposing an HTTP endpoint.

### Testing the server

```bash
# Run the example queries
python -m examples.sample_queries

# Run tests
pip install -e ".[dev]"
pytest -v
```

---

## Overview

This MCP server provides a bridge between Claude and the EPA Envirofacts API, enabling natural language queries about environmental data.

**EPA API Documentation:** https://www.epa.gov/enviro/envirofacts-data-service-api-v1

No API key required - the EPA Envirofacts API is public.

## Features

- Query EPA environmental databases
- Search for Superfund sites by location, name, or status
- Retrieve facility contamination data
- Access compliance and enforcement information
- Filter results by various environmental parameters

## Development Setup

### Environment variables (optional)

```bash
cp .env.example .env
# Edit .env to customize:
# EPA_API_BASE_URL=https://data.epa.gov/efservice
# EPA_REQUEST_TIMEOUT=30
# LOG_LEVEL=INFO
```

### Install for development

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest -v
pytest tests/test_query_builder.py  # specific test file
```

## Available Tools

The MCP server provides 6 specialized tools:

1. **query_epa_data** - General-purpose EPA table queries
2. **search_superfund_sites** - Find Superfund sites by location or name
3. **search_facilities** - Search EPA facility registry
4. **get_air_quality** - Retrieve air quality monitoring data
5. **get_water_quality** - Get water discharge and quality data
6. **get_compliance_violations** - Search environmental violations

See [USAGE.md](USAGE.md) for detailed documentation and examples.

## Usage with Claude

Once configured, you can ask Claude natural language questions:

- "Find all Superfund sites in California"
- "List hazardous waste facilities in Texas"
- "What are the air quality monitoring sites in New York?"
- "Show environmental violations in Illinois"
- "Get water discharge permits in Florida"

## API Response Handling

The tool processes EPA Envirofacts API responses and formats data for Claude integration, handling:
- Multiple data formats (JSON, XML, CSV)
- Pagination of large result sets
- Error handling and rate limiting
- Data validation and transformation

## Development

### Project Structure

```
superfund-dust/
├── README.md              # This file
├── USAGE.md              # Detailed usage guide
├── PLAN.md               # Development plan
├── CLAUDE.md             # Claude Code guidance
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project configuration
├── mcp_config.json       # MCP configuration example
├── src/
│   ├── __init__.py
│   ├── server.py         # MCP server implementation
│   ├── tools.py          # Tool implementations
│   ├── epa_api_client.py # EPA API client
│   ├── query_builder.py  # Query construction
│   ├── models.py         # Data models
│   ├── config.py         # Configuration
│   └── utils.py          # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_query_builder.py
│   ├── test_models.py
│   └── test_utils.py
└── examples/
    ├── README.md
    └── sample_queries.py
```

### Key Components

- **MCP Server** (`server.py`): Implements the Model Context Protocol interface
- **Tools** (`tools.py`): All 6 EPA query tools
- **API Client** (`epa_api_client.py`): HTTP client for EPA Envirofacts API
- **Query Builder** (`query_builder.py`): Constructs EPA API queries
- **Models** (`models.py`): Pydantic data validation models
- **Utilities** (`utils.py`): Helper functions for state codes, dates, etc.

## Claude Code Configuration

For Claude Code (CLI), add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "envirofacts-mcp": {
      "command": "/absolute/path/to/superfund-dust/venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/absolute/path/to/superfund-dust"
    }
  }
}
```

Restart Claude Code after making changes.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | Check Python 3.8+, activate venv, run `pip install -r requirements.txt` |
| Claude can't connect | Verify absolute paths in config, use full path to venv Python |
| Import errors | Run `pip install -e .` from project root |
| EPA API errors | Check internet, test with `curl https://data.epa.gov/efservice/` |

**Test the server independently:**
```bash
python -m src.server
```

## Contributing

Contributions are welcome! Please:
1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Test against the EPA API

## License

[Specify appropriate license]

## Resources

- [EPA Envirofacts Data Service](https://www.epa.gov/enviro/envirofacts-data-service-api-v1)
- [EPA Environmental Data](https://www.epa.gov/enviro/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)

## Support

For issues with the EPA API, consult the official documentation at https://www.epa.gov/enviro/envirofacts-data-service-api-v1

For issues with this tool, create an issue in the repository.
