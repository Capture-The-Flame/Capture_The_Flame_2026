from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES

OUT_PLAIN = "plain_image.bmp"
OUT_ENC   = "encrypted_image.bmp"
KEY = b"THIS_IS_16_BYTES"

# CRITICAL: Use dimensions where each PIXEL row aligns with blocks
# Each pixel row = width * 3 bytes (RGB)
# We want this divisible by 16
IMG_W, IMG_H = 320, 240    # 320*3 = 960 bytes = 60 blocks per row

FLAG_TEXT = "FLAME { ECB }"  # Shorter, clearer flag

# Create image with LARGE blocks of solid color
img = Image.new("RGB", (IMG_W, IMG_H), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# Create a simple pattern with LARGE repeating tiles (32x32 or larger)
TILE = 32  # Much larger tiles
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]

for ty in range(0, IMG_H, TILE):
    for tx in range(0, IMG_W, TILE):
        idx = ((tx // TILE) + (ty // TILE)) % len(colors)
        draw.rectangle([tx, ty, tx+TILE-1, ty+TILE-1], fill=colors[idx])

# Draw VERY LARGE text
try:
    font = ImageFont.truetype("SonikaBlack.ttf", 40)  
except:
    font = ImageFont.load_default()

# Center the text
draw.text((10, IMG_H//2 - 30), FLAG_TEXT, font=font, fill=(0, 0, 0))

img.save(OUT_PLAIN, format="BMP")
print(f"Plain BMP saved to {OUT_PLAIN}")


# 2) Encrypt the pixel data region of the BMP while preserving header
with open(OUT_PLAIN, "rb") as f:
    bmp = bytearray(f.read())

# BMP header: bytes 10-13 (little-endian) contain the offset to the start of pixel data
data_offset = int.from_bytes(bmp[10:14], "little")
print("BMP pixel data offset:", data_offset)

pixel_data = bytes(bmp[data_offset:])

# Ensure length multiple of 16 (we picked IMG_W/IMG_H such that RGB bytes divisible by 16)
if len(pixel_data) % 16 != 0:
    # As a safe fallback, pad with zeros (rare if IMG dims chosen well); viewers will still show it.
    pad_len = 16 - (len(pixel_data) % 16)
    pixel_data += b'\x00' * pad_len
    print("Padded pixel data by", pad_len)

cipher = AES.new(KEY, AES.MODE_ECB)
enc_pixels = cipher.encrypt(pixel_data)

# Write encrypted BMP: header untouched, pixel bytes replaced with ciphertext
with open(OUT_ENC, "wb") as f:
    f.write(bmp[:data_offset])
    f.write(enc_pixels)
print(f"Encrypted BMP written to {OUT_ENC}")
print("Keep KEY secret (not provided to players).")
