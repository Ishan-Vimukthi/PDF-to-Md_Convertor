"""
PDF to Markdown Conversion Service using Docling.

This module provides the core conversion logic using IBM's Docling engine
for high-accuracy PDF parsing with superior table, layout, and reading order detection.
"""

import logging
from pathlib import Path
from typing import Optional

from docling.document_converter import DocumentConverter, ConversionStatus
from docling.exceptions import ConversionError

logger = logging.getLogger(__name__)


class ConverterService:
    """
    Service class for converting PDF files to Markdown format using Docling.
    
    This class encapsulates the Docling conversion logic and provides
    error handling for corrupted or invalid PDF files.
    """
    
    def __init__(self):
        """
        Initialize the DocumentConverter instance.
        
        The converter is initialized once and reused for multiple conversions
        to improve performance.
        """
        self._converter: Optional[DocumentConverter] = None
    
    @property
    def converter(self) -> DocumentConverter:
        """
        Lazy initialization of the DocumentConverter.
        
        Returns:
            DocumentConverter: The Docling converter instance.
        """
        if self._converter is None:
            self._converter = DocumentConverter()
        return self._converter
    
    def convert_pdf_to_markdown(self, pdf_path: str) -> str:
        """
        Convert a PDF file to Markdown format.
        
        Args:
            pdf_path: Path to the temporary PDF file to convert.
            
        Returns:
            str: The converted Markdown content.
            
        Raises:
            FileNotFoundError: If the PDF file does not exist.
            ValueError: If the file is not a valid PDF or is corrupted.
            RuntimeError: If the conversion fails for any other reason.
        """
        pdf_file_path = Path(pdf_path)
        
        # Validate file exists
        if not pdf_file_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Validate file is not empty
        if pdf_file_path.stat().st_size == 0:
            logger.error(f"PDF file is empty: {pdf_path}")
            raise ValueError(f"PDF file is empty: {pdf_path}")
        
        try:
            logger.info(f"Starting conversion for file: {pdf_path}")
            
            # Perform the conversion using Docling
            conversion_result = self.converter.convert(pdf_file_path)
            
            # Check conversion status
            if conversion_result.status != ConversionStatus.SUCCESS:
                error_msg = f"Conversion failed with status: {conversion_result.status}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Extract Markdown from the conversion result
            if conversion_result.document is None:
                error_msg = "Conversion succeeded but no document was produced"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Export to Markdown format
            markdown_content = conversion_result.document.export_to_markdown()
            
            if not markdown_content:
                logger.warning(f"Conversion produced empty Markdown for: {pdf_path}")
            
            logger.info(f"Successfully converted {pdf_path} to Markdown")
            return markdown_content
            
        except ConversionError as e:
            error_msg = f"Docling conversion error: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
            
        except Exception as e:
            error_msg = f"Unexpected error during conversion: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e


# Singleton instance for reuse across requests
converter_service = ConverterService()
