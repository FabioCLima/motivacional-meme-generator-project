"""CLI interface for the Motivacional Meme Generator.

This module provides a command-line interface for generating memes using the
QuoteEngine and MemeEngine components. It can generate random memes or create
custom memes with specific images and quotes.
"""

import os
import random
from typing import Optional

from MemeEngine import MemeEngine
from QuoteEngine.ingestor import Ingestor
from QuoteEngine.quote_model import QuoteModel


def generate_meme(
    path: Optional[str] = None, body: Optional[str] = None, author: Optional[str] = None
) -> str:
    """Generate a meme given an optional path and quote.

    Args:
        path: Path to an image file. If None, a random image is chosen.
        body: Quote text. If None, a random quote is chosen from built-in data.
        author: Quote author. Required if body is provided.

    Returns:
        str: File path to the generated meme image.
        
    Raises:
        ValueError: If author is required but not provided.
    """
    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, _dirs, files in os.walk(images):
            for name in files:
                if ":" in name:
                    continue
                if not name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    continue
                imgs.append(os.path.join(root, name))
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            "./_data/DogQuotes/DogQuotesTXT.txt",
            "./_data/DogQuotes/DogQuotesDOCX.docx",
            "./_data/DogQuotes/DogQuotesPDF.pdf",
            "./_data/DogQuotes/DogQuotesCSV.csv",
        ]
        quotes = []
        for f in quote_files:
            try:
                quotes.extend(Ingestor.parse(f))
            except Exception:
                # Ignore problematic files but continue
                continue
        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError("Author Required if Body is Used")
        quote = QuoteModel(body, author)

    meme = MemeEngine("./tmp")
    out_path = meme.make_meme(img, quote.body, quote.author)
    return out_path


if __name__ == "__main__":
    # Minimal CLI for quick testing
    import argparse

    parser = argparse.ArgumentParser(description="Generate a meme")
    parser.add_argument("--path", type=str, help="path to an image file")
    parser.add_argument("--body", type=str, help="quote body to add to the image")
    parser.add_argument("--author", type=str, help="quote author to add to the image")
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
