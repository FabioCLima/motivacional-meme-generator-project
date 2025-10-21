"""Flask web application for the Motivacional Meme Generator.

This module provides a web interface for generating memes using the QuoteEngine
and MemeEngine components. Users can generate random memes or create custom
memes with their own images and quotes.
"""

import os
import random

import requests
from flask import Flask, abort, flash, redirect, render_template, request, url_for

from MemeEngine import MemeEngine
from QuoteEngine.ingestor import Ingestor

# Configure Flask to serve static files from the parent directory
app = Flask(__name__, static_folder='../static', static_url_path='/static')
app.secret_key = "replace-this-with-env-var"

# Create static directory in the project root
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
meme = MemeEngine(static_dir)


def setup():
    """Load quotes and images from provided data folders.
    
    Returns:
        tuple: A tuple containing (quotes, images) where quotes is a list of
            QuoteModel objects and images is a list of image file paths.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    quote_files = [
        os.path.join(script_dir, "_data/DogQuotes/DogQuotesTXT.txt"),
        os.path.join(script_dir, "_data/DogQuotes/DogQuotesDOCX.docx"),
        os.path.join(script_dir, "_data/DogQuotes/DogQuotesPDF.pdf"),
        os.path.join(script_dir, "_data/DogQuotes/DogQuotesCSV.csv"),
    ]

    quotes = []
    for f in quote_files:
        if os.path.exists(f):
            try:
                quotes.extend(Ingestor.parse(f))
                print(f"✓ Loaded quotes from {os.path.basename(f)}")
            except Exception as e:
                print(f"⚠ Failed to load {os.path.basename(f)}: {e}")
                continue
        else:
            print(f"⚠ File not found: {f}")

    images_path = os.path.join(script_dir, "_data/photos/dog/")
    imgs = []
    if os.path.exists(images_path):
        for root, _dirs, files in os.walk(images_path):
            for name in files:
                # skip Windows ADS artifacts and non-image files
                if ":" in name:
                    continue
                lower = name.lower()
                if not lower.endswith((".jpg", ".jpeg", ".png", ".gif")):
                    continue
                imgs.append(os.path.join(root, name))
        print(f"✓ Found {len(imgs)} images")
    else:
        print(f"⚠ Images directory not found: {images_path}")

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Generate a random meme and render it.
    
    Returns:
        str: Rendered HTML template with the generated meme.
        
    Raises:
        HTTPException: 500 error if resources are not available.
    """
    if not imgs or not quotes:
        abort(500, "Resources not available")

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    
    # Convert absolute path to relative path for Flask static files
    filename = os.path.basename(path)
    static_path = f"/static/{filename}"
    
    return render_template("meme.html", path=static_path)


@app.route("/create", methods=["GET"])
def meme_form():
    """Display user input form for creating custom memes.
    
    Returns:
        str: Rendered HTML template with the meme creation form.
    """
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme from form data.
    
    Returns:
        str: Rendered HTML template with the generated meme, or redirect to
            form if there's an error.
    """
    image_url = request.form.get("image_url")
    body = request.form.get("body")
    author = request.form.get("author")
    # Basic validation
    if not image_url:
        flash("Image URL is required", "danger")
        return redirect(url_for("meme_form"))
    if not body or not author:
        flash("Both quote body and author are required", "danger")
        return redirect(url_for("meme_form"))

    # 1. Download the image to a temp file
    try:
        res = requests.get(image_url, timeout=5)
        res.raise_for_status()
    except Exception:
        flash("Unable to fetch image from provided URL", "danger")
        return redirect(url_for("meme_form"))

    tmp_path = os.path.join("/tmp", f"tmp_{random.randint(0, 1000000)}")
    with open(tmp_path, "wb") as f:
        f.write(res.content)

    # 2. Generate the meme
    try:
        path = meme.make_meme(tmp_path, body, author)
        # Convert absolute path to relative path for Flask static files
        filename = os.path.basename(path)
        static_path = f"/static/{filename}"
    except Exception as e:
        flash(f"Error generating meme: {e}", "danger")
        static_path = None
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    if not static_path:
        return redirect(url_for("meme_form"))

    return render_template("meme.html", path=static_path)


if __name__ == "__main__":
    app.run()
