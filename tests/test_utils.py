"""Tests for utility functions."""

import pytest

from src.utils import (
    get_state_code,
    get_air_quality_parameter,
    format_date,
    summarize_epa_response,
)


class TestUtils:
    """Test utility functions."""

    def test_get_state_code_from_code(self):
        """Test getting state code from a code."""
        assert get_state_code("CA") == "CA"
        assert get_state_code("ca") == "CA"
        assert get_state_code("NY") == "NY"

    def test_get_state_code_from_name(self):
        """Test getting state code from name."""
        assert get_state_code("california") == "CA"
        assert get_state_code("California") == "CA"
        assert get_state_code("new york") == "NY"
        assert get_state_code("texas") == "TX"

    def test_get_state_code_invalid(self):
        """Test invalid state names."""
        with pytest.raises(ValueError):
            get_state_code("invalid")

        with pytest.raises(ValueError):
            get_state_code("ZZ")

    def test_get_air_quality_parameter(self):
        """Test getting air quality parameter codes."""
        assert get_air_quality_parameter("ozone") == "44201"
        assert get_air_quality_parameter("pm2.5") == "88101"
        assert get_air_quality_parameter("PM2.5") == "88101"
        assert get_air_quality_parameter("co") == "42101"

    def test_get_air_quality_parameter_unknown(self):
        """Test unknown pollutant."""
        assert get_air_quality_parameter("unknown") is None

    def test_format_date_valid(self):
        """Test date formatting with valid dates."""
        assert format_date("2024-01-15") == "2024-01-15"
        assert format_date("2023-12-31") == "2023-12-31"

    def test_format_date_invalid(self):
        """Test date formatting with invalid dates."""
        with pytest.raises(ValueError):
            format_date("2024/01/15")

        with pytest.raises(ValueError):
            format_date("01-15-2024")

        with pytest.raises(ValueError):
            format_date("invalid")

    def test_summarize_epa_response_empty(self):
        """Test summarizing empty response."""
        summary = summarize_epa_response([])
        assert summary["total"] == 0
        assert summary["sample"] == []

    def test_summarize_epa_response_with_data(self):
        """Test summarizing response with data."""
        data = [
            {"id": 1, "name": "Site A"},
            {"id": 2, "name": "Site B"},
            {"id": 3, "name": "Site C"},
        ]

        summary = summarize_epa_response(data, max_items=2)
        assert summary["total"] == 3
        assert summary["sample_count"] == 2
        assert len(summary["sample"]) == 2
        assert "id" in summary["available_fields"]
        assert "name" in summary["available_fields"]
