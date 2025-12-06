"""Utility functions for EPA Envirofacts MCP tool."""

from typing import Dict, Optional

# Common state codes mapping
STATE_CODES = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
}

# Common EPA parameter codes for air quality
AIR_QUALITY_PARAMETERS = {
    "ozone": "44201",
    "pm2.5": "88101",
    "pm10": "81102",
    "co": "42101",  # Carbon monoxide
    "no2": "42602",  # Nitrogen dioxide
    "so2": "42401",  # Sulfur dioxide
    "lead": "12128",
}


def get_state_code(state_name_or_code: str) -> str:
    """Convert state name to two-letter code.

    Args:
        state_name_or_code: State name or code

    Returns:
        Two-letter state code

    Raises:
        ValueError: If state is not recognized
    """
    state_input = state_name_or_code.strip().lower()

    # If already a valid code, return uppercase
    if len(state_input) == 2 and state_input.upper() in STATE_CODES.values():
        return state_input.upper()

    # Look up by name
    if state_input in STATE_CODES:
        return STATE_CODES[state_input]

    raise ValueError(f"Unknown state: {state_name_or_code}")


def get_air_quality_parameter(pollutant: str) -> Optional[str]:
    """Get EPA parameter code for common air pollutants.

    Args:
        pollutant: Pollutant name (e.g., "ozone", "pm2.5")

    Returns:
        Parameter code or None if not found
    """
    return AIR_QUALITY_PARAMETERS.get(pollutant.lower())


def format_date(date_str: str) -> str:
    """Validate and format date string.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Formatted date string

    Raises:
        ValueError: If date format is invalid
    """
    from datetime import datetime

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")


def summarize_epa_response(data: list, max_items: int = 5) -> Dict:
    """Create a summary of EPA response data.

    Args:
        data: List of response records
        max_items: Maximum items to include in summary

    Returns:
        Dictionary with summary information
    """
    if not data:
        return {"total": 0, "sample": [], "message": "No records found"}

    total = len(data)
    sample = data[:max_items]

    # Get common fields
    if data:
        fields = list(data[0].keys()) if isinstance(data[0], dict) else []
    else:
        fields = []

    return {
        "total": total,
        "sample_count": len(sample),
        "sample": sample,
        "available_fields": fields,
        "message": f"Found {total} records, showing first {len(sample)}",
    }
