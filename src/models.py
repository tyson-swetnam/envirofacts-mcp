"""Data models for EPA Envirofacts MCP tool."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    """Supported output formats."""

    JSON = "JSON"
    XML = "XML"
    CSV = "CSV"


class QueryOperator(str, Enum):
    """EPA API query operators."""

    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    BEGINNING = "BEGINNING"
    CONTAINING = "CONTAINING"


class EPADataSystem(str, Enum):
    """Major EPA data systems."""

    AQS = "AQS"  # Air Quality System
    ICIS = "ICIS"  # Integrated Compliance Information System
    RCRAINFO = "RCRAINFO"  # Hazardous Waste
    TRI = "TRI"  # Toxics Release Inventory
    SDWA = "SDWA"  # Safe Drinking Water
    FRS = "FRS"  # Facility Registry System
    GHG = "GHG"  # Greenhouse Gas


class QueryFilter(BaseModel):
    """Query filter specification."""

    column: str
    value: str
    operator: QueryOperator = QueryOperator.EQUAL


class EPAQueryRequest(BaseModel):
    """Request model for EPA API queries."""

    table_name: str
    filters: Optional[List[QueryFilter]] = None
    output_format: OutputFormat = OutputFormat.JSON
    row_limit: int = Field(default=100, ge=1, le=10000)
    offset: int = Field(default=0, ge=0)


class SuperfundSiteSearch(BaseModel):
    """Search parameters for Superfund sites."""

    state: Optional[str] = Field(None, max_length=2)
    county: Optional[str] = None
    zip_code: Optional[str] = Field(None, max_length=10)
    site_name: Optional[str] = None
    status: Optional[str] = None
    row_limit: int = Field(default=100, ge=1, le=10000)


class FacilitySearch(BaseModel):
    """Search parameters for facilities."""

    facility_name: Optional[str] = None
    state: Optional[str] = Field(None, max_length=2)
    zip_code: Optional[str] = Field(None, max_length=10)
    industry_code: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius_miles: Optional[float] = Field(None, gt=0, le=100)
    row_limit: int = Field(default=100, ge=1, le=10000)


class AirQualitySearch(BaseModel):
    """Search parameters for air quality data."""

    state: str = Field(max_length=2)
    county: Optional[str] = None
    parameter_code: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    row_limit: int = Field(default=100, ge=1, le=10000)


class WaterQualitySearch(BaseModel):
    """Search parameters for water quality data."""

    state: str = Field(max_length=2)
    facility_id: Optional[str] = None
    pollutant: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    row_limit: int = Field(default=100, ge=1, le=10000)


class ViolationSearch(BaseModel):
    """Search parameters for compliance violations."""

    state: Optional[str] = Field(None, max_length=2)
    facility_name: Optional[str] = None
    violation_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    row_limit: int = Field(default=100, ge=1, le=10000)


class EPAQueryResponse(BaseModel):
    """Response model for EPA API queries."""

    success: bool
    data: List[Dict[str, Any]]
    record_count: int
    query_url: str
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
