# Start from a base image that has Python already installed
FROM python:3.11-slim

# Install Tesseract OCR
# This is the system that reads text from images
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
# All our files will go in /app
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY app/ ./app/
COPY fonts/ ./fonts/
COPY app/ parchment.png .
COPY scripts/ ./scripts/

# Make the script executable
RUN chmod +x scripts/make_image.sh

# Expose port 5000
EXPOSE 5000

# Run the application when the container starts
CMD ["python", "app/server.py"]
