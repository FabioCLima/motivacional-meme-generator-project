"""Motivacional Meme Generator Package.

A motivational meme generator that combines quotes from various file formats
with images, demonstrating advanced Python concepts like abstract classes,
design patterns, and subprocess module usage.

This package provides:
- QuoteEngine: For parsing quotes from TXT, CSV, DOCX, and PDF files
- MemeEngine: For generating memes by adding text to images
- Web interface: Flask-based web application
- CLI interface: Command-line interface for meme generation
"""

__version__ = "1.0.0"
__author__ = "Fabio C. Lima"
__email__ = "fabio@example.com"

from .QuoteEngine import Ingestor, QuoteModel
from .MemeEngine import MemeEngine

__all__ = [
    "Ingestor",
    "QuoteModel", 
    "MemeEngine",
    "__version__",
    "__author__",
    "__email__",
]
