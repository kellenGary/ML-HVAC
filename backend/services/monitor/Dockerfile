# Use python 3.11 slim image for smaller size (supports ARM64/Pi 5)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Bluetooth (required by Bleak)
RUN apt-get update && apt-get install -y \
    bluez \
    dbus \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the build context (backend root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared code
COPY shared/ ./shared/

# Copy the monitor service code
COPY services/monitor/ ./services/monitor/

# Add /app to PYTHONPATH so imports like 'from shared.constants' work
ENV PYTHONPATH=/app

# Run the monitor script
CMD ["python", "services/monitor/main.py"]
