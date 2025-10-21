"""CSV file ingestor for parsing comma-separated value files using pandas.

This module provides the CSVIngestor class for parsing CSV files containing
quotes in various formats and column arrangements using the pandas library.
"""

import pandas as pd
from typing import List

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class CSVIngestor(IngestorInterface):
    """Ingestor for CSV files containing quotes using pandas.

    This class handles parsing of CSV files with various column name formats
    using pandas DataFrame operations and structural pattern matching for
    cleaner conditional logic.

    Attributes:
        allowed_extensions: List containing 'csv' extension.
    """

    allowed_extensions = ["csv"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse CSV file and return list of QuoteModel objects using pandas.
        
        This method uses pandas to read CSV files and employs structural pattern
        matching to handle various column name formats:
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
            # Read CSV file using pandas
            df = pd.read_csv(path)
            
            # Use structural pattern matching to determine column mapping
            body_col, author_col = cls._find_quote_columns(df.columns.tolist())
            
            if body_col and author_col:
                # Extract quotes using identified columns
                for _, row in df.iterrows():
                    body = str(row[body_col]).strip()
                    author = str(row[author_col]).strip()
                    
                    if body and author and body != 'nan' and author != 'nan':
                        quotes.append(QuoteModel(body, author))
            else:
                # Fallback: use first two columns if no named columns found
                if len(df.columns) >= 2:
                    for _, row in df.iterrows():
                        body = str(row.iloc[0]).strip()
                        author = str(row.iloc[1]).strip()
                        
                        if body and author and body != 'nan' and author != 'nan':
                            quotes.append(QuoteModel(body, author))
                            
        except Exception as e:
            raise ValueError(f"Error parsing CSV file {path} with pandas: {e}") from e

        return quotes
    
    @classmethod
    def _find_quote_columns(cls, columns: List[str]) -> tuple[str | None, str | None]:  # type: ignore
        """Find quote and author columns using structural pattern matching.
        
        Uses Python's structural pattern matching to identify the correct
        column names for body/quote and author/speaker fields.
        
        Args:
            columns: List of column names from the CSV file.
            
        Returns:
            tuple: (body_column, author_column) or (None, None) if not found.
        """
        # Convert to lowercase for case-insensitive matching
        lower_columns = [col.lower() for col in columns]
        
        # Use structural pattern matching to find columns
        match lower_columns:
            case cols if "body" in cols and "author" in cols:
                body_idx = lower_columns.index("body")
                author_idx = lower_columns.index("author")
                return columns[body_idx], columns[author_idx]
                
            case cols if "quote" in cols and "speaker" in cols:
                quote_idx = lower_columns.index("quote")
                speaker_idx = lower_columns.index("speaker")
                return columns[quote_idx], columns[speaker_idx]
                
            case cols if "body" in cols and "speaker" in cols:
                body_idx = lower_columns.index("body")
                speaker_idx = lower_columns.index("speaker")
                return columns[body_idx], columns[speaker_idx]
                
            case cols if "quote" in cols and "author" in cols:
                quote_idx = lower_columns.index("quote")
                author_idx = lower_columns.index("author")
                return columns[quote_idx], columns[author_idx]
                
            case _:
                # No matching pattern found
                return None, None
