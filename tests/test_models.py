"""Tests for data models."""

import pytest
from pydantic import ValidationError

from src.models import (
    EPAQueryRequest,
    QueryFilter,
    QueryOperator,
    SuperfundSiteSearch,
    FacilitySearch,
)


class TestModels:
    """Test Pydantic models."""

    def test_query_filter_creation(self):
        """Test creating query filters."""
        filter_obj = QueryFilter(column="state_code", value="CA")
        assert filter_obj.column == "state_code"
        assert filter_obj.value == "CA"
        assert filter_obj.operator == QueryOperator.EQUAL

    def test_query_filter_with_operator(self):
        """Test filter with custom operator."""
        filter_obj = QueryFilter(
            column="name", value="Chemical", operator=QueryOperator.CONTAINING
        )
        assert filter_obj.operator == QueryOperator.CONTAINING

    def test_epa_query_request(self):
        """Test EPA query request model."""
        request = EPAQueryRequest(table_name="SEMS_SITES", row_limit=50)
        assert request.table_name == "SEMS_SITES"
        assert request.row_limit == 50
        assert request.filters is None

    def test_epa_query_request_with_filters(self):
        """Test query request with filters."""
        filters = [QueryFilter(column="state_code", value="NY")]
        request = EPAQueryRequest(table_name="FRS_FACILITIES", filters=filters)
        assert len(request.filters) == 1
        assert request.filters[0].column == "state_code"

    def test_row_limit_validation(self):
        """Test row limit validation."""
        # Valid limits
        request = EPAQueryRequest(table_name="TEST", row_limit=1)
        assert request.row_limit == 1

        request = EPAQueryRequest(table_name="TEST", row_limit=10000)
        assert request.row_limit == 10000

        # Invalid limits
        with pytest.raises(ValidationError):
            EPAQueryRequest(table_name="TEST", row_limit=0)

        with pytest.raises(ValidationError):
            EPAQueryRequest(table_name="TEST", row_limit=10001)

    def test_superfund_site_search(self):
        """Test Superfund site search model."""
        search = SuperfundSiteSearch(state="CA", county="Los Angeles")
        assert search.state == "CA"
        assert search.county == "Los Angeles"
        assert search.row_limit == 100  # default

    def test_facility_search(self):
        """Test facility search model."""
        search = FacilitySearch(state="TX", facility_name="Chemical Plant")
        assert search.state == "TX"
        assert search.facility_name == "Chemical Plant"

    def test_facility_search_with_coordinates(self):
        """Test facility search with geographic coordinates."""
        search = FacilitySearch(latitude=34.05, longitude=-118.25, radius_miles=10)
        assert search.latitude == 34.05
        assert search.longitude == -118.25
        assert search.radius_miles == 10

    def test_state_code_validation(self):
        """Test state code length validation."""
        # Valid 2-letter code
        search = SuperfundSiteSearch(state="CA")
        assert search.state == "CA"

        # Invalid - too long
        with pytest.raises(ValidationError):
            SuperfundSiteSearch(state="CALIFORNIA")
