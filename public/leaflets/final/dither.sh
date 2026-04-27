#!/bin/bash

# Configuration
INPUT_DIR="."
OUTPUT_DIR="./dithered"
WIDTH=200        # Set your desired width
HEIGHT=150       # Set your desired height
# To resize by one dimension only (preserve aspect ratio), use e.g.:
# RESIZE="${WIDTH}x"   # constrain width only
# RESIZE="x${HEIGHT}"  # constrain height only
RESIZE="${WIDTH}x${HEIGHT}"

mkdir -p "$OUTPUT_DIR"

for f in "$INPUT_DIR"/*.jpg; do
  [ -f "$f" ] || continue
  filename=$(basename "$f")
  echo "Processing: $filename"
convert "$f" \
  -resize "${RESIZE}" \
  -dither FloydSteinberg \
  -quantize transparent \
  -colors 16 \
  -depth 4 \
  "$OUTPUT_DIR/$filename"
done

echo "Done. Output in: $OUTPUT_DIR"
