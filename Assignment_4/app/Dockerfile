FROM python:3.12-slim

WORKDIR /app

# Install system dependencies first
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel

# Try wheels only, fallback to normal if needed
RUN pip install --only-binary=:all: --no-cache-dir -r requirements.txt || pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
