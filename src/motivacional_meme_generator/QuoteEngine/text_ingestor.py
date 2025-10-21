"""Plain text file ingestor for parsing text files.

This module provides the TextIngestor class for parsing plain text files
containing quotes in the format "quote text - author".
"""

from typing import List

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class TextIngestor(IngestorInterface):
    """Ingestor for plain text files containing quotes.

    This class handles parsing of plain text files where each line contains
    a quote in the format "quote text - author".

    Attributes:
        allowed_extensions: List containing 'txt' extension.
    """

    allowed_extensions = ["txt"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse text file and return list of QuoteModel objects.
        
        This method parses plain text files where each line contains a quote
        in the format "quote text - author". It handles various delimiters
        and cleans up the text content.

        Expected format: "Quote text" - Author

        Args:
            path: Path to the text file to parse.
            
        Returns:
            List[QuoteModel]: List of quote objects extracted from the text file.
            
        Raises:
            ValueError: If the text file cannot be parsed.
        """
        quotes: List[QuoteModel] = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if "-" not in line:
                        continue
                    
                    # Split by last occurrence of " - " or just "-"
                    if " - " in line:
                        body, author = line.rsplit(" - ", 1)
                    else:
                        body, author = line.rsplit("-", 1)
                    
                    # Clean up body (remove quotes and extra spaces)
                    body = body.strip(' "').strip()
                    author = author.strip()
                    
                    if body and author:  # Only add if both parts exist
                        quotes.append(QuoteModel(body, author))
        except Exception as e:
            raise ValueError(f"Error parsing text file {path}: {e}") from e
        return quotes
