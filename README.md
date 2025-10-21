# Motivational Meme Generator

A Flask application that generates motivational memes by combining quotes from various file formats with images. This project demonstrates advanced Python concepts including abstract classes, design patterns, and subprocess module usage.

## 🎯 Features

- **Multi-format Quote Parsing**: Supports CSV, DOCX, PDF, and TXT files
- **Meme Generation**: Combines images with motivational quotes
- **CLI Interface**: Command-line tool for meme generation
- **Web Interface**: Flask-based web application with interactive forms
- **Random Generation**: Automatically selects quotes and images
- **Custom Memes**: Create memes with specific quotes and images

## 🏗️ Architecture

### Design Patterns Implemented

- **Strategy Pattern**: Specific ingestors for each file type
- **Facade Pattern**: Main Ingestor class that automatically selects the appropriate strategy
- **Abstract Factory**: Common interface for all ingestors

### Project Structure

```
motivacional-meme-generator-project/
├── src/
│   ├── motivacional_meme_generator/     # Main package
│   │   ├── __init__.py
│   │   ├── app.py                       # Flask web application
│   │   ├── cli.py                       # Command-line interface
│   │   ├── meme.py                      # Legacy CLI interface
│   │   ├── MemeEngine.py                # Image manipulation engine
│   │   └── QuoteEngine/                 # Quote ingestion module
│   │       ├── __init__.py
│   │       ├── ingestor_interface.py    # Abstract interface
│   │       ├── ingestor.py              # Main facade
│   │       ├── quote_model.py           # Data model
│   │       ├── csv_ingestor.py          # CSV strategy
│   │       ├── docx_ingestor.py         # DOCX strategy
│   │       ├── pdf_ingestor.py          # PDF strategy
│   │       └── text_ingestor.py          # TXT strategy
│   ├── _data/                           # Sample data
│   │   ├── DogQuotes/                   # Dog-themed quotes in multiple formats
│   │   ├── SimpleLines/                 # Simple motivational quotes
│   │   └── photos/                      # Images for memes
│   └── templates/                       # HTML templates
├── static/                              # Generated static files
├── tests/                               # Unit tests
├── scripts/                             # Utility scripts
├── docs/                                # Documentation
├── main.py                              # Main entry point
├── test_implementation.py              # Implementation tests
├── requirements.txt                     # Python dependencies
├── pyproject.toml                       # Project configuration
└── LICENSE                              # MIT License
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- System tools for PDF processing (xpdf-utils or mupdf-tools)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/FabioCLima/motivacional-meme-generator-project.git
cd motivacional-meme-generator-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install PDF tools (Ubuntu/Debian)
sudo apt-get install -y xpdf-utils
```

### Development Installation

For development with additional tools:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Or install specific development tools
pip install pytest black flake8 mypy
```

## 🎮 Usage

### Web Interface (Recommended)

```bash
cd src
python app.py
```

Access the application at: http://127.0.0.1:5000/

The web interface provides:
- **Random Meme Generator**: Automatically creates memes with random quotes and images
- **Custom Meme Creator**: Form to create memes with specific quotes and images
- **Image Upload**: Support for image URLs

### Command Line Interface

#### Random Meme Generation
```bash
python main.py
```

#### Custom Meme Generation
```bash
# Using the legacy CLI
python src/meme.py --path ./src/_data/photos/dog/xander_1.jpg --body "Hello World" --author "Test Author"

# Using the new CLI (if installed)
meme-generator --image ./src/_data/photos/dog/xander_1.jpg --quote "Hello World" --author "Test Author"
```

### Programmatic Usage

```python
from src.QuoteEngine import Ingestor, QuoteModel
from src.MemeEngine import MemeEngine

# Load quotes from files
quotes = Ingestor.parse("./src/_data/DogQuotes/DogQuotesTXT.txt")

# Create meme engine
meme_engine = MemeEngine("./static")

# Generate meme
meme_path = meme_engine.make_meme(
    image_path="./src/_data/photos/dog/xander_1.jpg",
    body="Stay motivated!",
    author="Motivational Speaker"
)
```

## 🧪 Testing

### Run Implementation Tests
```bash
python test_implementation.py
```

### Run Unit Tests
```bash
# Using pytest
pytest tests/

# With coverage
pytest --cov=src tests/
```

### Expected Test Results
```
🚀 Running Implementation Tests
==================================================
🧪 Testing Quote Parsing...
✓ DogQuotesTXT.txt: 2 quotes
✓ DogQuotesCSV.csv: 2 quotes
✓ DogQuotesPDF.pdf: 3 quotes
✓ SimpleLines.txt: 5 quotes
✓ SimpleLines.csv: 5 quotes
✓ SimpleLines.pdf: 5 quotes
📊 Total quotes parsed: 22

🎨 Testing Meme Generation...
✓ Meme generated successfully

🔧 Testing Ingestor Interface...
✓ All interface tests passed

📊 Test Results: 3/3 tests passed
🎉 All tests passed! Implementation is working correctly.
```

## 📊 Quote Format

The project expects quotes in the following format:
```
"Quote text" - Author Name
```

### Supported Formats

- **TXT**: Lines with quotes separated by "-"
- **CSV**: Columns "body" and "author" (or "quote" and "speaker")
- **DOCX**: Paragraphs with quotes in standard format
- **PDF**: Lines extracted as text with standard format

## 🔧 Technologies Used

### Python Libraries
- **Pillow**: Image manipulation and processing
- **python-docx**: Microsoft Word document processing
- **Flask**: Web framework for the web interface
- **requests**: HTTP library for image downloads

### System Tools
- **pdftotext** (xpdf-utils): PDF text extraction
- **mutool** (mupdf-tools): Alternative PDF processing

## 🎯 Python Concepts Demonstrated

- **Abstract Classes**: `IngestorInterface` with abstract methods
- **Inheritance**: All ingestors inherit from the common interface
- **Polymorphism**: Same `parse()` method for different file types
- **Subprocess Module**: System tool integration for PDF processing
- **Type Hints**: Type annotations throughout the codebase
- **Exception Handling**: Robust error handling in all operations
- **Design Patterns**: Strategy, Facade, and Abstract Factory patterns

## 📈 Project Statistics

- **Total Quotes**: 22+ quotes from 8 different files
- **Supported Formats**: 4 file types (CSV, DOCX, PDF, TXT)
- **Image Support**: JPG, PNG, GIF, BMP formats
- **Test Coverage**: Comprehensive test suite
- **Code Quality**: PEP 8 compliant with type hints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Fabio C. Lima**
- Email: lima.fisico@gmail.com
- GitHub: [@FabioCLima](https://github.com/FabioCLima)

## 🙏 Acknowledgments

- Udacity Intermediate Python Course
- Python community for excellent libraries
- Contributors and testers

---

**Ready for submission and evaluation!** 🚀