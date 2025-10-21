from QuoteEngine.quote_model import QuoteModel
from QuoteEngine.text_ingestor import TextIngestor


def test_quote_model_str():
    q = QuoteModel("Hello world", "Author")
    assert "Hello world" in str(q)


def test_text_ingestor(tmp_path):
    content = "This is a test - Tester\nAnother quote - Someone"
    file = tmp_path / "quotes.txt"
    file.write_text(content, encoding="utf-8")
    quotes = TextIngestor.parse(str(file))
    assert len(quotes) == 2
    assert quotes[0].author == "Tester"
