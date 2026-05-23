FROM apify/actor-python:3.12

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/main.py ./src/main.py

# Run the actor
CMD ["python", "src/main.py"]
