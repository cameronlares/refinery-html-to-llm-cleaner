FROM python:3.12-slim

# Install system dependencies including Rust
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    curl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Rust source and build
COPY Cargo.toml Cargo.lock ./
COPY src ./src/

# Build and install Rust core
RUN pip install maturin && \
    maturin build --release && \
    pip install target/wheels/refinery_core-0.1.0-cp312-cp312-linux_x86_64.whl

# Copy FastAPI application
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run the actor
CMD ["python", "-m", "refinery"]
