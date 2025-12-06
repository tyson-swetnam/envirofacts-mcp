"""Sample queries demonstrating EPA Envirofacts MCP tool usage."""

import asyncio
import json

from src.tools import EPATools


async def example_queries():
    """Run example EPA queries."""
    tools = EPATools()

    print("=" * 80)
    print("EPA Envirofacts MCP Tool - Sample Queries")
    print("=" * 80)

    # Example 1: Search Superfund sites in California
    print("\n1. Searching for Superfund sites in California...")
    result = await tools.search_superfund_sites(state="CA", row_limit=5)
    data = json.loads(result)
    print(f"Found {data.get('record_count', 0)} sites")
    if data.get("sites"):
        print(f"First site: {data['sites'][0].get('site_name', 'N/A')}")

    # Example 2: Search facilities by name
    print("\n2. Searching for facilities with 'Chemical' in the name...")
    result = await tools.search_facilities(facility_name="Chemical", row_limit=5)
    data = json.loads(result)
    print(f"Found {data.get('record_count', 0)} facilities")

    # Example 3: Get air quality data for Texas
    print("\n3. Getting air quality monitoring sites in Texas...")
    result = await tools.get_air_quality(state="TX", row_limit=5)
    data = json.loads(result)
    print(f"Found {data.get('record_count', 0)} monitoring sites")

    # Example 4: Get water quality permits in Florida
    print("\n4. Getting water discharge permits in Florida...")
    result = await tools.get_water_quality(state="FL", row_limit=5)
    data = json.loads(result)
    print(f"Found {data.get('record_count', 0)} permits")

    # Example 5: General query - TRI facilities
    print("\n5. Querying TRI (Toxics Release Inventory) facilities...")
    result = await tools.query_epa_data(
        table_name="TRI_FACILITY",
        filters=[{"column": "state_code", "value": "NY"}],
        row_limit=5,
    )
    data = json.loads(result)
    print(f"Found {data.get('record_count', 0)} TRI facilities in NY")

    # Example 6: Search for compliance violations
    print("\n6. Searching for compliance violations in Illinois...")
    result = await tools.get_compliance_violations(state="IL", row_limit=5)
    data = json.loads(result)
    print(f"Found {data.get('record_count', 0)} violation records")

    print("\n" + "=" * 80)
    print("Sample queries completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(example_queries())
