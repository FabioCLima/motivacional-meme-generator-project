"""Web interface for the Motivacional Meme Generator.

This module provides a Flask-based web interface for generating memes.
"""

import os
import random
import sys
from pathlib import Path

import requests
from flask import Flask, abort, flash, redirect, render_template, request, url_for

from .MemeEngine import MemeEngine
from .QuoteEngine import Ingestor


def create_app(data_dir: str = None, static_dir: str = None):
    """Create and configure the Flask application.
    
    Args:
        data_dir: Directory containing quotes and images data.
        static_dir: Directory for static files (generated memes).
        
    Returns:
        Flask: Configured Flask application.
    """
    app = Flask(__name__, static_folder=static_dir, static_url_path='/static')
    app.secret_key = os.environ.get('SECRET_KEY', "replace-this-with-env-var")
    
    if data_dir is None:
        # Use package data directory
        package_dir = Path(__file__).parent
        data_dir = str(package_dir / "_data")
    
    if static_dir is None:
        # Use default static directory
        static_dir = str(Path.cwd() / "static")
    
    # Create static directory
    os.makedirs(static_dir, exist_ok=True)
    meme_engine = MemeEngine(static_dir)
    
    def load_quotes():
        """Load quotes from data directory."""
        quote_files = [
            os.path.join(data_dir, "DogQuotes", "DogQuotesTXT.txt"),
            os.path.join(data_dir, "DogQuotes", "DogQuotesDOCX.docx"),
            os.path.join(data_dir, "DogQuotes", "DogQuotesPDF.pdf"),
            os.path.join(data_dir, "DogQuotes", "DogQuotesCSV.csv"),
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
        
        return quotes
    
    def load_images():
        """Load images from data directory."""
        images_path = os.path.join(data_dir, "photos", "dog")
        imgs = []
        
        if os.path.exists(images_path):
            for root, _dirs, files in os.walk(images_path):
                for name in files:
                    # Skip Windows ADS artifacts and non-image files
                    if ":" in name:
                        continue
                    lower = name.lower()
                    if not lower.endswith((".jpg", ".jpeg", ".png", ".gif")):
                        continue
                    imgs.append(os.path.join(root, name))
            print(f"✓ Found {len(imgs)} images")
        else:
            print(f"⚠ Images directory not found: {images_path}")
        
        return imgs
    
    # Load quotes and images
    quotes = load_quotes()
    imgs = load_images()
    
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
        path = meme_engine.make_meme(img, quote.body, quote.author)
        
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
        
        # Download the image to a temp file
        try:
            res = requests.get(image_url, timeout=5)
            res.raise_for_status()
        except Exception:
            flash("Unable to fetch image from provided URL", "danger")
            return redirect(url_for("meme_form"))
        
        tmp_path = os.path.join("/tmp", f"tmp_{random.randint(0, 1000000)}")
        with open(tmp_path, "wb") as f:
            f.write(res.content)
        
        # Generate the meme
        try:
            path = meme_engine.make_meme(tmp_path, body, author)
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
    
    return app


def main():
    """Main entry point for the web application."""
    app = create_app()
    
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🌐 Starting Motivacional Meme Generator Web Interface")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
