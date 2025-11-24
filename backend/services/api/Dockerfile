FROM python:3.11-slim

WORKDIR /app

# Copy requirements from the build context
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared code
COPY shared/ ./shared/

# Copy the api service code
COPY services/api/ ./services/api/

# Add /app to PYTHONPATH
ENV PYTHONPATH=/app

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the API script
CMD ["python", "services/api/main.py"]
