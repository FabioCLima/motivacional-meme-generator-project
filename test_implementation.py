#!/usr/bin/env python3
"""Test script to verify the implementation works correctly.

This script tests all components of the meme generator to ensure
they work according to the requirements.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine


def test_quote_parsing():
    """Test parsing of different file types.
    
    Returns:
        bool: True if quote parsing tests pass, False otherwise.
    """
    print("🧪 Testing Quote Parsing...")
    
    # Test data paths
    test_files = [
        "./src/_data/DogQuotes/DogQuotesTXT.txt",
        "./src/_data/DogQuotes/DogQuotesCSV.csv",
        "./src/_data/DogQuotes/DogQuotesPDF.pdf",
        "./src/_data/SimpleLines/SimpleLines.txt",
        "./src/_data/SimpleLines/SimpleLines.csv",
        "./src/_data/SimpleLines/SimpleLines.pdf",
    ]
    
    total_quotes = 0
    
    for file_path in test_files:
        if os.path.exists(file_path):
            try:
                quotes = Ingestor.parse(file_path)
                print(f"✓ {os.path.basename(file_path)}: {len(quotes)} quotes")
                total_quotes += len(quotes)
                
                # Show first quote as example
                if quotes:
                    print(f"  Example: {quotes[0]}")
            except Exception as e:
                print(f"❌ {os.path.basename(file_path)}: {e}")
        else:
            print(f"⚠ {os.path.basename(file_path)}: File not found")
    
    print(f"📊 Total quotes parsed: {total_quotes}")
    return total_quotes > 0


def test_meme_generation():
    """Test meme generation functionality.
    
    Returns:
        bool: True if meme generation tests pass, False otherwise.
    """
    print("\n🎨 Testing Meme Generation...")
    
    # Find a test image
    images_dir = "./src/_data/photos"
    test_image = None
    
    if os.path.exists(images_dir):
        for root, _dirs, files in os.walk(images_dir):
            for name in files:
                if name.lower().endswith((".jpg", ".jpeg", ".png")):
                    test_image = os.path.join(root, name)
                    break
            if test_image:
                break
    
    if not test_image:
        print("⚠ No test images found")
        return False
    
    try:
        # Create test meme
        meme_engine = MemeEngine("./tmp_test")
        test_quote = QuoteModel("Test quote", "Test Author")
        
        meme_path = meme_engine.make_meme(test_image, test_quote.body, test_quote.author)
        
        if os.path.exists(meme_path):
            print(f"✓ Meme generated successfully: {os.path.basename(meme_path)}")
            return True
        else:
            print("❌ Meme file not created")
            return False
            
    except Exception as e:
        print(f"❌ Meme generation failed: {e}")
        return False


def test_ingestor_interface():
    """Test the ingestor interface and strategy pattern.
    
    Returns:
        bool: True if ingestor interface tests pass, False otherwise.
    """
    print("\n🔧 Testing Ingestor Interface...")
    
    from QuoteEngine.text_ingestor import TextIngestor
    from QuoteEngine.csv_ingestor import CSVIngestor
    from QuoteEngine.docx_ingestor import DocxIngestor
    from QuoteEngine.pdf_ingestor import PDFIngestor
    
    # Test can_ingest method
    test_cases = [
        ("test.txt", TextIngestor, True),
        ("test.csv", CSVIngestor, True),
        ("test.docx", DocxIngestor, True),
        ("test.pdf", PDFIngestor, True),
        ("test.txt", CSVIngestor, False),
        ("test.jpg", TextIngestor, False),
    ]
    
    all_passed = True
    
    for filename, ingestor_class, expected in test_cases:
        result = ingestor_class.can_ingest(filename)
        status = "✓" if result == expected else "❌"
        print(f"{status} {ingestor_class.__name__}.can_ingest('{filename}') = {result} (expected {expected})")
        if result != expected:
            all_passed = False
    
    return all_passed


def main():
    """Run all tests and return exit code.
    
    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    print("🚀 Running Implementation Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Quote parsing
    if test_quote_parsing():
        tests_passed += 1
    
    # Test 2: Meme generation
    if test_meme_generation():
        tests_passed += 1
    
    # Test 3: Ingestor interface
    if test_ingestor_interface():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Implementation is working correctly.")
        return 0
    else:
        print("⚠ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
