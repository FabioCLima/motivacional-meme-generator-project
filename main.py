#!/usr/bin/env python3
"""Main entry point for the Motivacional Meme Generator project.

This script provides a command-line interface to generate memes from quotes
and images. It demonstrates the usage of the QuoteEngine and MemeEngine modules.
"""

import os
import random
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine


def load_quotes(data_dir: str = "./src/_data") -> list[QuoteModel]:
    """Load quotes from all supported file types in the data directory.
    
    This function searches for quote files in the specified directory and
    subdirectories, parsing them using the appropriate ingestors.

    Args:
        data_dir: Directory containing quote files.
        
    Returns:
        list[QuoteModel]: List of QuoteModel objects loaded from all files.
    """
    quotes = []
    
    # Define quote file paths
    quote_files = [
        f"{data_dir}/DogQuotes/DogQuotesTXT.txt",
        f"{data_dir}/DogQuotes/DogQuotesDOCX.docx", 
        f"{data_dir}/DogQuotes/DogQuotesPDF.pdf",
        f"{data_dir}/DogQuotes/DogQuotesCSV.csv",
        f"{data_dir}/SimpleLines/SimpleLines.txt",
        f"{data_dir}/SimpleLines/SimpleLines.docx",
        f"{data_dir}/SimpleLines/SimpleLines.pdf",
        f"{data_dir}/SimpleLines/SimpleLines.csv",
    ]
    
    for file_path in quote_files:
        if os.path.exists(file_path):
            try:
                file_quotes = Ingestor.parse(file_path)
                quotes.extend(file_quotes)
                print(f"✓ Loaded {len(file_quotes)} quotes from {os.path.basename(file_path)}")
            except Exception as e:
                print(f"⚠ Failed to load quotes from {os.path.basename(file_path)}: {e}")
        else:
            print(f"⚠ File not found: {os.path.basename(file_path)}")
    
    return quotes


def load_images(data_dir: str = "./src/_data") -> list[str]:
    """Load image file paths from the data directory.
    
    This function recursively searches for image files in the specified
    directory and returns their file paths.

    Args:
        data_dir: Directory containing image files.
        
    Returns:
        list[str]: List of image file paths.
    """
    images = []
    photos_dir = f"{data_dir}/photos"
    
    if os.path.exists(photos_dir):
        for root, _dirs, files in os.walk(photos_dir):
            for name in files:
                # Skip Windows ADS artifacts and non-image files
                if ":" in name:
                    continue
                lower = name.lower()
                if lower.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                    images.append(os.path.join(root, name))
    
    return images


def generate_random_meme(output_dir: str = "./static") -> str:
    """Generate a random meme using random quote and image.
    
    This function selects a random quote and image from the available data,
    then generates a meme using the MemeEngine.

    Args:
        output_dir: Directory to save the generated meme.
        
    Returns:
        str: Path to the generated meme file.
        
    Raises:
        ValueError: If no quotes or images are available.
    """
    quotes = load_quotes()
    images = load_images()
    
    if not quotes:
        raise ValueError("No quotes available")
    if not images:
        raise ValueError("No images available")
    
    quote = random.choice(quotes)
    image = random.choice(images)
    
    print(f"Selected quote: {quote}")
    print(f"Selected image: {os.path.basename(image)}")
    
    meme_engine = MemeEngine(output_dir)
    meme_path = meme_engine.make_meme(image, quote.body, quote.author)
    
    print(f"Generated meme: {meme_path}")
    return meme_path


def main():
    """Main function demonstrating the meme generator functionality.
    
    This function serves as the entry point for the CLI application,
    demonstrating the complete meme generation workflow.
    """
    print("🎭 Motivacional Meme Generator")
    print("=" * 40)
    
    try:
        # Create output directory
        os.makedirs("./static", exist_ok=True)
        
        # Generate random meme
        meme_path = generate_random_meme()
        
        print("\n🎉 Success! Your motivational meme has been generated!")
        print(f"📁 File location: {meme_path}")
        
        # Show some statistics
        quotes = load_quotes()
        images = load_images()
        print(f"\n📊 Statistics:")
        print(f"   • Total quotes loaded: {len(quotes)}")
        print(f"   • Total images available: {len(images)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
