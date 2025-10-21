"""Quote model for representing quotes with body and author.

This module defines the QuoteModel dataclass that represents a quote
with its body text and author information.
"""

from dataclasses import dataclass


@dataclass
class QuoteModel:
    """Model that represents a quote with body and author.

    This dataclass encapsulates a quote with its text content and author
    information. It provides a string representation for easy display.

    Attributes:
        body: The quote text content.
        author: The quote author name.

    Example:
        quote = QuoteModel("To be or not to be", "Shakespeare")
        print(quote)  # "To be or not to be" - Shakespeare
    """

    body: str
    author: str

    def __str__(self) -> str:
        """Return a formatted string representation of the quote.

        Returns:
            str: Formatted quote string in the format '"body" - author'.
        """
        return f'"{self.body}" - {self.author}'
