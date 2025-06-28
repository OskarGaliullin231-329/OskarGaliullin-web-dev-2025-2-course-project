# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Create directory for file storage
RUN mkdir -p users_file_storage

# Create directory for Flask sessions
RUN mkdir -p flask_session

# Expose port for gunicorn
EXPOSE 8000

# Run the startup script
CMD ["./start.sh"] 
