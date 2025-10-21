"""DOCX file ingestor for parsing Microsoft Word documents.

This module provides the DocxIngestor class for parsing DOCX files containing
quotes in paragraph format.
"""

from typing import List

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class DocxIngestor(IngestorInterface):
    """Ingestor for DOCX files containing quotes.

    This class handles parsing of Microsoft Word DOCX files where quotes
    are stored in paragraph format.

    Attributes:
        allowed_extensions: List containing 'docx' extension.
    """

    allowed_extensions = ["docx"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse DOCX file and return list of QuoteModel objects.
        
        This method parses DOCX files by extracting text from paragraphs
        and looking for quotes in the format "quote text - author".

        Expected format: "Quote text" - Author in each paragraph

        Args:
            path: Path to the DOCX file to parse.
            
        Returns:
            List[QuoteModel]: List of quote objects extracted from the DOCX file.
            
        Raises:
            RuntimeError: If python-docx library is not installed.
            ValueError: If the DOCX file cannot be parsed.
        """
        quotes: List[QuoteModel] = []
        try:
            from docx import Document  # Local import to keep optional dependency
        except ImportError as exc:
            raise RuntimeError("python-docx is required to parse docx files") from exc

        try:
            doc = Document(path)
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                if "-" not in text:
                    continue
                
                # Split by last occurrence of " - " or just "-"
                if " - " in text:
                    body, author = text.rsplit(" - ", 1)
                else:
                    body, author = text.rsplit("-", 1)
                
                # Clean up body (remove quotes and extra spaces)
                body = body.strip(' "').strip()
                author = author.strip()
                
                if body and author:  # Only add if both parts exist
                    quotes.append(QuoteModel(body, author))
        except Exception as e:
            raise ValueError(f"Error parsing DOCX file {path}: {e}") from e
        return quotes
