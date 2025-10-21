"""Abstract interface for file ingestors.

This module defines the abstract base class for all file ingestor implementations,
ensuring a consistent interface for parsing different file types.
"""

from abc import ABC, abstractmethod
from typing import List

from .quote_model import QuoteModel


class IngestorInterface(ABC):
    """Abstract interface for file ingestors.

    This abstract base class defines the contract that all file ingestor
    implementations must follow. It ensures consistent behavior across
    different file type parsers.

    Attributes:
        allowed_extensions: List of file extensions this ingestor can handle.

    Note:
        Implementations must provide can_ingest and parse class methods.
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if this ingestor can parse the given file based on extension.

        Args:
            path: File path to check.

        Returns:
            bool: True if this ingestor can handle the file type, False otherwise.
        """
        ext = path.split(".")[-1].lower()
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the file and return list of QuoteModel objects.

        Args:
            path: Path to the file to parse.

        Returns:
            List[QuoteModel]: List of quote objects extracted from the file.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError
