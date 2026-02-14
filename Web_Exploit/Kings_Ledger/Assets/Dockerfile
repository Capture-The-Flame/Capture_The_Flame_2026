# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Flask port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Run Flask
CMD ["flask", "run"]
