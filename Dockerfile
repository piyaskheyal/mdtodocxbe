# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy pandoc .deb file
COPY deb_files/pandoc-3.8.2.1-1-amd64.deb /tmp/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    /tmp/pandoc-3.8.2.1-1-amd64.deb \
    && rm -rf /var/lib/apt/lists/* /tmp/pandoc-3.8.2.1-1-amd64.deb

# Copy requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY backend/ .

# Create uploads directory
RUN mkdir -p uploads/md uploads/docx

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
