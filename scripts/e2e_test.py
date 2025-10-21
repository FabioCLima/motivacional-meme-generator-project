"""Script de integração: parseia quotes e gera um meme usando recursos locais."""

import os
import random
import sys

# Ensure local src is importable when running this script directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from MemeEngine import MemeEngine
from QuoteEngine.ingestor import Ingestor


def main():
    quote_files = [
        "src/_data/DogQuotes/DogQuotesTXT.txt",
        "src/_data/DogQuotes/DogQuotesDOCX.docx",
        "src/_data/DogQuotes/DogQuotesPDF.pdf",
        "src/_data/DogQuotes/DogQuotesCSV.csv",
    ]

    quotes = []
    for f in quote_files:
        try:
            quotes.extend(Ingestor.parse(f))
        except Exception:
            continue

    images_path = "src/_data/photos/dog/"
    imgs = []
    for root, _dirs, files in os.walk(images_path):
        for n in files:
            if ":" in n:
                continue
            if not n.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                continue
            imgs.append(os.path.join(root, n))

    if not imgs or not quotes:
        print("Resources not available")
        return

    img = random.choice(imgs)
    quote = random.choice(quotes)
    meme = MemeEngine("./tmp")
    out = meme.make_meme(img, quote.body, quote.author)
    print("Generated meme:", out)


if __name__ == "__main__":
    main()
