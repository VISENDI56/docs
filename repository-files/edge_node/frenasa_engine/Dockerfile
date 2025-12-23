# iLuminara-Core FRENASA Engine Dockerfile
# Voice-to-JSON transformation with offline SQLite buffer (IP-05: Golden Thread)
# Compliance: NIST RMF supply chain requirements

FROM python:3.11.7-slim@sha256:2cba8e6b7c59a0e2f9b5e3d8f8c8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8 AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    OFFLINE_MODE=true \
    GOLDEN_THREAD_BUFFER=/app/data/golden_thread.db

WORKDIR /app

# Install system dependencies including SQLite
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libsqlite3-dev \
        sqlite3 \
        libsndfile1 \
        ffmpeg \
        curl \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-frenasa.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-frenasa.txt

# Copy FRENASA engine code
COPY edge_node/frenasa_engine/ ./frenasa_engine/
COPY edge_node/sync_protocol/ ./sync_protocol/
COPY governance_kernel/ ./governance_kernel/

# Create data directory for offline buffer
RUN mkdir -p /app/data && \
    sqlite3 /app/data/golden_thread.db "CREATE TABLE IF NOT EXISTS offline_buffer (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, data_type TEXT, payload TEXT, synced INTEGER DEFAULT 0);"

# Create non-root user
RUN useradd -m -u 1001 -s /bin/bash iluminara && \
    chown -R iluminara:iluminara /app

# Switch to non-root user
USER iluminara

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import sqlite3; conn = sqlite3.connect('/app/data/golden_thread.db'); conn.execute('SELECT 1'); conn.close()" || exit 1

# Expose port
EXPOSE 8082

# Labels for compliance
LABEL org.opencontainers.image.title="iLuminara FRENASA Engine" \
      org.opencontainers.image.description="Voice-to-JSON with Offline Buffer" \
      org.opencontainers.image.vendor="iLuminara Health" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.licenses="Proprietary" \
      compliance.offline="true" \
      nuclear_ip.golden_thread="active" \
      nuclear_ip.offline_buffer="sqlite"

# Start FRENASA engine
CMD ["python", "-m", "frenasa_engine.voice_processor"]
