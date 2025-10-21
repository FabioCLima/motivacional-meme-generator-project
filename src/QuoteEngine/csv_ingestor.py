"""CSV file ingestor for parsing comma-separated value files.

This module provides the CSVIngestor class for parsing CSV files containing
quotes in various formats and column arrangements.
"""

import csv
from typing import List

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class CSVIngestor(IngestorInterface):
    """Ingestor for CSV files containing quotes.

    This class handles parsing of CSV files with various column name formats
    and provides fallback mechanisms for different CSV structures.

    Attributes:
        allowed_extensions: List containing 'csv' extension.
    """

    allowed_extensions = ["csv"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse CSV file and return list of QuoteModel objects.
        
        This method attempts to parse CSV files with various column name formats:
        - body/author columns
        - quote/speaker columns  
        - Case variations (Body/Author, Quote/Speaker)
        - Fallback to positional columns if named columns not found

        Args:
            path: Path to the CSV file to parse.
            
        Returns:
            List[QuoteModel]: List of quote objects extracted from the CSV file.
            
        Raises:
            ValueError: If the CSV file cannot be parsed with any method.
        """
        quotes: List[QuoteModel] = []
        try:
            with open(path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Try different column name variations
                    body = (row.get("body") or 
                           row.get("quote") or 
                           row.get("Body") or 
                           row.get("Quote"))
                    
                    author = (row.get("author") or 
                            row.get("speaker") or 
                            row.get("Author") or 
                            row.get("Speaker"))
                    
                    # If no named columns found, use positional
                    if not body or not author:
                        values = list(row.values())
                        if len(values) >= 2:
                            body = values[0]
                            author = values[1]
                    
                    if body and author:
                        quotes.append(QuoteModel(body.strip(), author.strip()))
        except Exception as e:
            # Fallback to simple CSV parsing
            try:
                with open(path, "r", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) >= 2 and row[0].strip() and row[1].strip():
                            quotes.append(QuoteModel(row[0].strip(), row[1].strip()))
            except Exception as fallback_error:
                raise ValueError(f"Error parsing CSV file {path}: {e}, fallback also failed: {fallback_error}") from e

        return quotes
