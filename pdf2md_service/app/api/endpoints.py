"""
API endpoints for PDF to Markdown conversion.

This module defines the REST API endpoints for converting PDF files to Markdown.
"""

import logging
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.schemas import ConversionResponse, ErrorResponse
from app.services.converter_service import converter_service

logger = logging.getLogger(__name__)

# Create the router with a prefix and tags for OpenAPI documentation
router = APIRouter(prefix="/api/v1", tags=["conversion"])


@router.post(
    "/convert",
    response_model=ConversionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid or corrupted PDF file"},
        422: {"model": ErrorResponse, "description": "Validation error (e.g., missing file)"},
        500: {"model": ErrorResponse, "description": "Internal server error during conversion"},
    },
    summary="Convert PDF to Markdown",
    description="""
    Upload a PDF file and convert it to Markdown format using IBM's Docling engine.
    
    This endpoint provides high-accuracy conversion with superior handling of:
    - Tables and structured data
    - Document layout and formatting
    - Reading order detection
    - Images and figures (referenced in Markdown)
    
    The uploaded file is securely stored in a temporary location and automatically
    cleaned up after conversion, regardless of success or failure.
    """,
)
async def convert_pdf_to_markdown(
    file: Annotated[UploadFile, File(description="PDF file to convert")],
) -> ConversionResponse:
    """
    Convert an uploaded PDF file to Markdown format.
    
    Args:
        file: The PDF file uploaded via multipart/form-data.
        
    Returns:
        ConversionResponse: Contains the original filename and converted Markdown content.
        
    Raises:
        HTTPException: If the file is invalid, corrupted, or conversion fails.
    """
    # Validate file type
    if not file.filename:
        logger.warning("Upload received without a filename")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided",
        )
    
    # Validate file extension (case-insensitive)
    if not file.filename.lower().endswith(".pdf"):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Expected PDF, got: {file.filename}",
        )
    
    temp_file_path = None
    
    try:
        # Read the uploaded file content
        logger.info(f"Processing upload: {file.filename} ({file.size or 'unknown'} bytes)")
        file_content = await file.read()
        
        # Validate file is not empty
        if not file_content or len(file_content) == 0:
            logger.warning(f"Empty file uploaded: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded PDF file is empty",
            )
        
        # Create a secure temporary file
        # Use delete=False so we can explicitly control cleanup
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
            prefix="pdf2md_",
        ) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(file_content)
            temp_file.flush()
        
        logger.debug(f"Saved temporary file: {temp_file_path}")
        
        # Call the conversion service
        logger.info(f"Starting conversion for: {file.filename}")
        markdown_content = converter_service.convert_pdf_to_markdown(temp_file_path)
        
        logger.info(f"Successfully converted: {file.filename}")
        
        return ConversionResponse(
            filename=file.filename,
            markdown=markdown_content,
        )
        
    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF file not found or inaccessible",
        ) from e
        
    except ValueError as e:
        logger.error(f"Value error during conversion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted PDF: {str(e)}",
        ) from e
        
    except RuntimeError as e:
        logger.error(f"Runtime error during conversion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversion failed: {str(e)}",
        ) from e
        
    except Exception as e:
        logger.exception(f"Unexpected error during conversion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        ) from e
        
    finally:
        # Always clean up the temporary file
        if temp_file_path and Path(temp_file_path).exists():
            try:
                Path(temp_file_path).unlink()
                logger.debug(f"Cleaned up temporary file: {temp_file_path}")
            except OSError as e:
                logger.error(f"Failed to clean up temporary file {temp_file_path}: {str(e)}")
