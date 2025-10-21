"""Command-line interface for the Motivacional Meme Generator.

This module provides a CLI interface for generating memes from the command line.
"""

import argparse
import os
import random
import sys
from pathlib import Path
from typing import Optional

from .QuoteEngine import Ingestor, QuoteModel
from .MemeEngine import MemeEngine


def load_quotes(data_dir: str = None) -> list[QuoteModel]:
    """Load quotes from all supported file types in the data directory.
    
    Args:
        data_dir: Directory containing quote files. If None, uses package data.
        
    Returns:
        list[QuoteModel]: List of QuoteModel objects loaded from all files.
    """
    if data_dir is None:
        # Use package data directory
        package_dir = Path(__file__).parent
        data_dir = str(package_dir / "_data")
    
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


def load_images(data_dir: str = None) -> list[str]:
    """Load image file paths from the data directory.
    
    Args:
        data_dir: Directory containing image files. If None, uses package data.
        
    Returns:
        list[str]: List of image file paths.
    """
    if data_dir is None:
        # Use package data directory
        package_dir = Path(__file__).parent
        data_dir = str(package_dir / "_data")
    
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
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate motivational memes from quotes and images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Generate random meme
  %(prog)s --output ./memes          # Save to custom directory
  %(prog)s --quote "Hello World" --author "Test" --image ./photo.jpg
        """
    )
    
    parser.add_argument(
        "--output", "-o",
        default="./static",
        help="Output directory for generated memes (default: ./static)"
    )
    
    parser.add_argument(
        "--quote", "-q",
        help="Quote text to use (if not provided, random quote will be selected)"
    )
    
    parser.add_argument(
        "--author", "-a",
        help="Quote author (required if --quote is provided)"
    )
    
    parser.add_argument(
        "--image", "-i",
        help="Image file path (if not provided, random image will be selected)"
    )
    
    parser.add_argument(
        "--data-dir", "-d",
        help="Directory containing quotes and images data"
    )
    
    args = parser.parse_args()
    
    try:
        # Create output directory
        os.makedirs(args.output, exist_ok=True)
        
        if args.quote and args.author:
            # Custom quote provided
            if not args.image:
                raise ValueError("Image file required when using custom quote")
            
            if not os.path.exists(args.image):
                raise FileNotFoundError(f"Image file not found: {args.image}")
            
            quote = QuoteModel(args.quote, args.author)
            meme_engine = MemeEngine(args.output)
            meme_path = meme_engine.make_meme(args.image, quote.body, quote.author)
            
            print(f"🎉 Custom meme generated: {meme_path}")
            
        else:
            # Generate random meme
            meme_path = generate_random_meme(args.output)
            print(f"\n🎉 Success! Your motivational meme has been generated!")
            print(f"📁 File location: {meme_path}")
            
            # Show some statistics
            quotes = load_quotes(args.data_dir)
            images = load_images(args.data_dir)
            print(f"\n📊 Statistics:")
            print(f"   • Total quotes loaded: {len(quotes)}")
            print(f"   • Total images available: {len(images)}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
