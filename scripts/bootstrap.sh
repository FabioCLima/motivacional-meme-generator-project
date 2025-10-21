#!/usr/bin/env bash
# Bootstrap script: create venv (optional) and install dependencies using uv or pip
set -euo pipefail

echo "Bootstrap script for Motivational Meme Generator"

if command -v uv >/dev/null 2>&1; then
  echo "Using uv to add dependencies..."
  uv add Pillow python-docx Flask requests pytest
else
  echo "uv not found, falling back to pip"
  python3 -m pip install -r requirements.txt
fi

echo "Done. Run 'uv run python src/app.py' or 'python3 src/app.py' to start the server."
