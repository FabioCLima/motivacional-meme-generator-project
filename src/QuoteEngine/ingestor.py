"""Facade ingestor for selecting appropriate file parsers.

This module provides the main Ingestor class that implements the Facade pattern
to provide a unified interface for parsing different file types. It automatically
selects the appropriate ingestor based on the file extension.
"""

from typing import List

from .csv_ingestor import CSVIngestor
from .docx_ingestor import DocxIngestor
from .ingestor_interface import IngestorInterface
from .pdf_ingestor import PDFIngestor
from .quote_model import QuoteModel
from .text_ingestor import TextIngestor


class Ingestor(IngestorInterface):
    """Facade ingestor that selects the appropriate ingestor for a file.
    
    This class implements the Facade pattern to provide a unified interface
    for parsing different file types. It automatically selects the appropriate
    ingestor based on the file extension and handles errors gracefully.

    Supported file types:
        - .txt (plain text)
        - .csv (comma-separated values)
        - .docx (Microsoft Word documents)
        - .pdf (Portable Document Format)

    Note:
        This class inherits from IngestorInterface but doesn't define
        allowed_extensions since it delegates to specific ingestors.
    """

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the file at path and return a list of QuoteModel objects.
        
        This method automatically selects the appropriate ingestor based on
        the file extension and delegates the parsing to that ingestor.

        Args:
            path: Path to the file to parse.
            
        Returns:
            List[QuoteModel]: List of quote objects extracted from the file.
            
        Raises:
            ValueError: If no ingestor can handle the file type or parsing fails.
            FileNotFoundError: If the file doesn't exist.
        """
        import os
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        for ingestor in (TextIngestor, CSVIngestor, DocxIngestor, PDFIngestor):
            if ingestor.can_ingest(path):
                try:
                    return ingestor.parse(path)
                except Exception as e:
                    raise ValueError(f"Failed to parse {path} with {ingestor.__name__}: {e}") from e
        
        raise ValueError(f"No available ingestor for file type: {path}")
