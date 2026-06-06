"""
Pydantic models for request/response validation.

This module defines the data schemas used throughout the API.
"""

from pydantic import BaseModel, Field


class ConversionResponse(BaseModel):
    """
    Response model for successful PDF to Markdown conversion.
    
    Attributes:
        filename: The original name of the uploaded PDF file.
        markdown: The converted Markdown content as a string.
    """
    filename: str = Field(..., description="Original filename of the uploaded PDF")
    markdown: str = Field(..., description="Converted Markdown content")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "filename": "document.pdf",
                    "markdown": "# Document Title\n\nThis is the converted content..."
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """
    Response model for error scenarios.
    
    Attributes:
        detail: A human-readable error message.
        error_type: The type of error that occurred.
    """
    detail: str = Field(..., description="Human-readable error message")
    error_type: str = Field(..., description="Type of error (e.g., 'validation_error', 'conversion_error')")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": "PDF file is corrupted or invalid",
                    "error_type": "conversion_error"
                }
            ]
        }
    }
