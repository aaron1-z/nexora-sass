FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root (assuming context is project root, but docker-compose context is ./api usually)
# We need to adjust docker-compose context or copy requirements here.
# For simplicity, let's assume we copy requirements.txt to api/ or install directly.
# Better: Copy requirements.txt to the service dir first or use a shared context.
# Given the structure, let's create a requirements.txt inside api/ or just install the main one if context allows.
# Standard pattern: Copy local requirements.

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
