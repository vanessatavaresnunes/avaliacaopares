FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy source
COPY . .

# Streamlit settings for containers
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Default command can be overridden by docker-compose
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

EXPOSE 8501 8502

