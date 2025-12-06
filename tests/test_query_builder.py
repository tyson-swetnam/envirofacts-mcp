"""Tests for EPA query builder."""

import pytest

from src.models import OutputFormat, QueryFilter, QueryOperator
from src.query_builder import EPAQueryBuilder


class TestEPAQueryBuilder:
    """Test query builder functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.builder = EPAQueryBuilder(base_url="https://data.epa.gov/efservice")

    def test_simple_query_construction(self):
        """Test building a simple query."""
        url = self.builder.build_simple_query(
            table_name="SEMS_SITES", column="state_code", value="CA", row_limit=10
        )

        assert "SEMS_SITES" in url
        assert "state_code" in url
        assert "CA" in url
        assert "rows/0:10" in url
        assert "JSON" in url

    def test_query_with_filters(self):
        """Test query with multiple filters."""
        filters = [
            QueryFilter(column="state_code", value="CA"),
            QueryFilter(column="status", value="Final"),
        ]

        url = self.builder.build_query_url(table_name="SEMS_SITES", filters=filters, row_limit=50)

        assert "SEMS_SITES" in url
        assert "state_code" in url
        assert "CA" in url
        assert "status" in url
        assert "Final" in url
        assert "rows/0:50" in url

    def test_query_with_containing_operator(self):
        """Test query with CONTAINING operator."""
        filters = [
            QueryFilter(column="site_name", value="Mining", operator=QueryOperator.CONTAINING)
        ]

        url = self.builder.build_query_url(table_name="SEMS_SITES", filters=filters)

        assert "site_name" in url
        assert "CONTAINING" in url
        assert "Mining" in url

    def test_query_with_pagination(self):
        """Test query with offset pagination."""
        url = self.builder.build_query_url(
            table_name="FRS_FACILITIES", row_limit=100, offset=100
        )

        assert "rows/100:200" in url

    def test_different_output_formats(self):
        """Test different output formats."""
        # JSON
        url = self.builder.build_query_url(
            table_name="SEMS_SITES", output_format=OutputFormat.JSON
        )
        assert "JSON" in url

        # XML
        url = self.builder.build_query_url(
            table_name="SEMS_SITES", output_format=OutputFormat.XML
        )
        assert "XML" in url

        # CSV
        url = self.builder.build_query_url(
            table_name="SEMS_SITES", output_format=OutputFormat.CSV
        )
        assert "CSV" in url

    def test_query_url_format(self):
        """Test that generated URL has correct base format."""
        url = self.builder.build_simple_query(table_name="TEST_TABLE", column="id", value="123")

        assert url.startswith("https://data.epa.gov/efservice")
        assert "TEST_TABLE" in url
