"""MemeEngine module: generate memes by adding text to images.

Simple, well-typed implementation using Pillow.
"""

from __future__ import annotations

import os
import random

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:  # Pillow is optional at import time
    Image = ImageDraw = ImageFont = None


class MemeEngine:
    """Engine to create memes: write text onto images and save them.

    This class handles image manipulation and text overlay for meme generation.
    It uses Pillow (PIL) for image processing and provides methods to resize
    images and add formatted text with proper wrapping and positioning.

    Attributes:
        output_dir: Directory where generated memes are saved.

    Example:
        meme = MemeEngine('./tmp')
        path = meme.make_meme(img_path, 'hello', 'author')
    """

    def __init__(self, output_dir: str) -> None:
        """Initialize the MemeEngine with an output directory.

        Args:
            output_dir: Directory where generated memes will be saved.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _load_font(self, size: int = 20) -> ImageFont.FreeTypeFont:
        """Load a font with the specified size.

        Args:
            size: Font size in points.

        Returns:
            ImageFont.FreeTypeFont: Loaded font object.

        Raises:
            RuntimeError: If Pillow is not available.
        """
        # Try to use a common system font; fallback to default
        if ImageFont is None:
            raise RuntimeError("Pillow is required for MemeEngine")

        try:
            return ImageFont.truetype("arial.ttf", size=size)
        except Exception:
            return ImageFont.load_default()

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """Create meme with given text and author, return path to saved image.

        Args:
            img_path: Path to the source image file.
            text: Quote body text to display on the meme.
            author: Quote author to display on the meme.
            width: Maximum width for the output image in pixels.

        Returns:
            str: Path to the generated meme image file.

        Raises:
            RuntimeError: If Pillow is not available.
            FileNotFoundError: If the source image file is not found.
        """
        if Image is None:
            raise RuntimeError("Pillow is required for MemeEngine")

        try:
            img = Image.open(img_path)
        except Exception as e:
            raise FileNotFoundError(f"Image not found: {img_path}") from e

        # Resize maintaining aspect ratio
        ratio = min(1, width / img.width)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

        draw = ImageDraw.Draw(img)

        # Prepare text: body + author on next line
        body = f'"{text}"'
        author_line = f"- {author}"

        # compute max text width (image width minus padding)
        padding = 20
        max_width = img.width - 2 * padding

        # dynamic font sizing: start large and shrink until text fits
        font_size = min(40, int(img.height / 10))
        font = None

        def wrap_text(s: str, font_obj, max_w: int) -> list[str]:
            words = s.split()
            lines: list[str] = []
            current = []
            for w in words:
                candidate = " ".join(current + [w]) if current else w
                w_box = draw.textbbox((0, 0), candidate, font=font_obj)
                w_width = w_box[2] - w_box[0]
                if w_width <= max_w:
                    current.append(w)
                else:
                    if current:
                        lines.append(" ".join(current))
                    current = [w]
            if current:
                lines.append(" ".join(current))
            return lines

        # Pick font size so that wrapped body + author fits vertically
        while font_size > 10:
            try:
                font = self._load_font(size=font_size)
            except RuntimeError:
                raise
            body_lines = wrap_text(body, font, max_width)
            author_lines = wrap_text(author_line, font, max_width)
            # compute total height
            line_height = draw.textbbox((0, 0), "Ay", font=font)[3]
            total_h = (len(body_lines) + len(author_lines)) * (line_height + 4)
            if total_h < img.height * 0.5:  # don't take more than half image height
                break
            font_size -= 2

        # Compose final lines
        lines = body_lines + [""] + author_lines

        # start vertical position centered in the lower half
        total_h = len(lines) * (line_height + 4)
        y_start = int(img.height * 0.6 - total_h // 2)

        # Draw each line centered horizontally with an outline for readability
        for i, line in enumerate(lines):
            if not line:
                continue
            w_box = draw.textbbox((0, 0), line, font=font)
            text_w = w_box[2] - w_box[0]
            x = (img.width - text_w) // 2
            y = y_start + i * (line_height + 4)
            # outline
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    draw.text((x + dx, y + dy), line, font=font, fill="black")
            draw.text((x, y), line, font=font, fill="white")

        out_path = os.path.join(
            self.output_dir, f"meme_{random.randint(0, 1000000)}.jpg"
        )
        img.save(out_path)
        return out_path
