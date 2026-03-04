#!/usr/bin/env bash

set -euo pipefail

TEXT="${1:-}"
OUT="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Look for font and parchment in current directory first, then script directory
if [ -f "./EzraSil-Po0B.ttf" ]; then
    FONT="./EzraSil-Po0B.ttf"
elif [ -f "${SCRIPT_DIR}/../fonts/EzraSil-Po0B.ttf" ]; then
    FONT="${SCRIPT_DIR}/../fonts/EzraSil-Po0B.ttf"
else
    echo "Error: EzraSil-Po0B.ttf not found!"
    echo "Please download it: curl -O http://localhost:5000/download/EzraSil-Po0B.ttf"
    exit 1
fi

if [ -f "./parchment.png" ]; then
    PARCHMENT="./parchment.png"
elif [ -f "${SCRIPT_DIR}/../parchment.png" ]; then
    PARCHMENT="${SCRIPT_DIR}/../parchment.png"
else
    echo "Error: parchment.png not found!"
    echo "Please download it: curl -O http://localhost:5000/download/parchment.png"
    exit 1
fi

mkdir -p "$(dirname "$OUT")"

# Use Python with Pillow
python3 - "$TEXT" "$OUT" "$FONT" "$PARCHMENT" << 'PYTHON'
import sys
from PIL import Image, ImageDraw, ImageFont

text = sys.argv[1]
output = sys.argv[2]
font_path = sys.argv[3]
parchment_path = sys.argv[4]

# Load and resize parchment
img = Image.open(parchment_path)
img = img.resize((400, 200), Image.Resampling.LANCZOS)

# Load font
font = ImageFont.truetype(font_path, 36)

# Create drawing context
draw = ImageDraw.Draw(img)

# Get text bounding box for centering
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Center text
x = (400 - text_width) // 2
y = (200 - text_height) // 2

# Draw text
draw.text((x, y), text, font=font, fill="#2b1e0b")

# Save
img.save(output)
PYTHON

echo "Created image: $OUT"