#!/usr/bin/env python3
"""
Convert each image in a directory to a PDF with the image
centered on a letter-size page (8.5" x 11").
"""

import sys
import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp"}

LETTER_W, LETTER_H = letter  # 612 x 792 pts
MARGIN = 36  # 0.5" margin on each side


def image_to_pdf(img_path: Path, out_path: Path):
    with Image.open(img_path) as im:
        img_w, img_h = im.size

    # Rotate canvas (not image) 90° if image is wider than tall,
    # so the long edge of the image always runs along the long edge of the page.
    rotate = img_w > img_h
    if rotate:
        page_w, page_h = LETTER_H, LETTER_W  # landscape canvas
    else:
        page_w, page_h = LETTER_W, LETTER_H  # portrait canvas

    # Available area inside margins
    avail_w = page_w - 2 * MARGIN
    avail_h = page_h - 2 * MARGIN

    # Scale to fit, then halve
    scale = min(avail_w / img_w, avail_h / img_h) / 2
    draw_w = img_w * scale
    draw_h = img_h * scale

    # Center on page
    x = (page_w - draw_w) / 2
    y = (page_h - draw_h) / 2

    c = canvas.Canvas(str(out_path), pagesize=(page_w, page_h))
    c.drawImage(str(img_path), x, y, width=draw_w, height=draw_h,
                preserveAspectRatio=True, mask="auto")
    c.save()


def main():
    if len(sys.argv) < 2:
        print("Usage: python images_to_pdf.py <image_dir> [output_dir]")
        sys.exit(1)

    img_dir = Path(sys.argv[1])
    if not img_dir.is_dir():
        print(f"Error: '{img_dir}' is not a directory.")
        sys.exit(1)

    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else img_dir / "pdfs"
    out_dir.mkdir(parents=True, exist_ok=True)

    images = sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS)

    if not images:
        print("No images found.")
        sys.exit(0)

    print(f"Found {len(images)} image(s). Writing PDFs to: {out_dir}")

    for img_path in images:
        out_path = out_dir / (img_path.stem + ".pdf")
        try:
            image_to_pdf(img_path, out_path)
            print(f"  ✓ {img_path.name} → {out_path.name}")
        except Exception as e:
            print(f"  ✗ {img_path.name}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()