# Multi-stage build to reduce image size
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy only necessary application code
COPY bot.py config.py rag_system.py knowledge_loader.py ./
COPY knowledge_base ./knowledge_base

# Clean up
RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    find /root/.local -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true && \
    find /root/.local -type f -name "*.pyc" -delete

# Run the bot
CMD ["python", "bot.py"]

