FROM python:3.10-slim AS builder

WORKDIR /root

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to local user directory
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Stage 2: Runtime ---
FROM python:3.10-slim

# Install runtime dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a non-root user
RUN groupadd -r placement && useradd -r -g placement placement

# Copy installed dependencies from the builder stage
COPY --from=builder /root/.local /home/placement/.local
ENV PATH=/home/placement/.local/bin:$PATH

# Copy application files
COPY . .

# Adjust permissions and switch to non-root user
RUN chown -R placement:placement /app \
    && mkdir -p /app/logs /app/uploads \
    && chown -R placement:placement /app/logs /app/uploads

USER placement

EXPOSE 8000

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
