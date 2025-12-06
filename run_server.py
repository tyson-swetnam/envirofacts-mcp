#!/usr/bin/env python
"""Convenience script to run the EPA Envirofacts MCP server."""

import sys
from src.server import main
import asyncio

if __name__ == "__main__":
    print("=" * 80)
    print("EPA Envirofacts MCP Server")
    print("=" * 80)
    print()
    print("Starting server...")
    print("Press Ctrl+C to stop")
    print()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
