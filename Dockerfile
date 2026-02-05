# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Render uses dynamic PORT)
EXPOSE 10000

# Command to run the application using host/port variables
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
