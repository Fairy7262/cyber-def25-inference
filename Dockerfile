# Dockerfile for CYBER-DEF25 inference container
FROM python:3.11-slim

# Create app dir
WORKDIR /app

# Copy requirements first to leverage caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy model and inference code
COPY model.pkl /app/model.pkl
COPY inference.py /app/inference.py

# Create required folders in container
RUN mkdir -p /input/logs /output

# Expose nothing required (it's an offline inference that reads files). Use ENTRYPOINT to run inference.
# If inference.py accepts arguments you can modify CMD accordingly.
ENTRYPOINT ["python", "/app/inference.py"]
