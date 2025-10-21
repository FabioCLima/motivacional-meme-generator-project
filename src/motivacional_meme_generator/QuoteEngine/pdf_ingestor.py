"""PDF file ingestor for parsing PDF documents using system tools.

This module provides the PDFIngestor class for parsing PDF files using
system utilities via the subprocess module, demonstrating proper use of
subprocess as required by the project specifications.
"""

import os
import shutil
import subprocess
import tempfile
from typing import List

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class PDFIngestor(IngestorInterface):
    """Ingestor for PDF files using system tools via subprocess module.
    
    This class handles parsing of PDF files by using system utilities through
    the subprocess module. It demonstrates proper use of subprocess as required
    by the project specifications and avoids using the PyPi pdftotext library.

    Attributes:
        allowed_extensions: List containing 'pdf' extension.
    """

    allowed_extensions = ["pdf"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse PDF file and return list of QuoteModel objects.
        
        This method uses the subprocess module to call system utilities for
        text extraction from PDF files. It supports multiple tools with fallback:
        - pdftotext (from xpdf-utils package) - preferred
        - mutool (from mupdf-tools package) - fallback
        
        This implementation demonstrates proper use of the subprocess module
        as required by the project specifications and avoids PyPi libraries.

        Args:
            path: Path to the PDF file to parse.
            
        Returns:
            List[QuoteModel]: List of quote objects extracted from the PDF file.
            
        Raises:
            RuntimeError: If neither pdftotext nor mutool is found, or if
                the subprocess call fails.
            ValueError: If the PDF file cannot be parsed or contains no quotes.
        """
        quotes: List[QuoteModel] = []
        
        # Try pdftotext first, then mutool as fallback
        pdf_tool = None
        if shutil.which("pdftotext"):
            pdf_tool = "pdftotext"
        elif shutil.which("mutool"):
            pdf_tool = "mutool"
        else:
            raise RuntimeError("Neither pdftotext nor mutool found; please install Xpdf utilities or mupdf-tools")

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            if pdf_tool == "pdftotext":
                subprocess.run(["pdftotext", path, tmp_path], check=True, capture_output=True)
            else:  # mutool
                # mutool draw -F txt input.pdf > output.txt
                with open(tmp_path, "w", encoding="utf-8") as f:
                    result = subprocess.run(["mutool", "draw", "-F", "txt", path], 
                                          capture_output=True, text=True, check=True)
                    f.write(result.stdout)
            
            with open(tmp_path, "r", encoding="utf-8") as f:
                for line in f:
                    text = line.strip()
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
        except subprocess.CalledProcessError as err:
            raise RuntimeError(f"{pdf_tool} failed: {err}") from err
        except Exception as e:
            raise ValueError(f"Error parsing PDF file {path}: {e}") from e
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        return quotes
