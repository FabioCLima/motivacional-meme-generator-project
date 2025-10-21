"""QuoteEngine package for parsing quotes from various file formats.

This package provides a unified interface for parsing quotes from different
file types including TXT, CSV, DOCX, and PDF files. It implements the Strategy
and Facade design patterns to provide a clean, extensible architecture.

Main components:
    - Ingestor: Facade class that automatically selects the appropriate parser
    - QuoteModel: Data model representing a quote with body and author
    - Specific ingestors: TextIngestor, CSVIngestor, DocxIngestor, PDFIngestor

Example:
    from QuoteEngine import Ingestor
    quotes = Ingestor.parse("path/to/quotes.txt")
"""

from .ingestor import Ingestor
from .quote_model import QuoteModel

__all__ = ["Ingestor", "QuoteModel"]
