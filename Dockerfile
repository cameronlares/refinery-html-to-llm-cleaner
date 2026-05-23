FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pre-compiled Python module
COPY refinery_core_src/refinery_core.cpython-312-x86_64-linux-gnu.so /usr/local/lib/python3.12/site-packages/

# Copy FastAPI application
COPY app/ ./app/
COPY src/main.py ./src/

# Install the actor
RUN pip install -e .

# Expose port
EXPOSE 8000

# Run the actor
CMD ["python", "-m", "refinery"]
