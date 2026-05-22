# Refinery Cloud API - Documentation

## Overview
Ultra-fast HTML text extraction API - 281x faster than BeautifulSoup

## Base URL
```
https://refinery-api.larelabs.com
```

## Endpoints

### POST /v1/refinery
Extract clean text and metadata from HTML

**Request:**
```bash
curl -X POST "https://refinery-api.larelabs.com/v1/refinery" \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Test</h1></body></html>"}'
```

**Request Body:**
```json
{
  "html": "<html>...</html>"
}
```

**Response:**
```json
{
  "html": "Clean extracted text",
  "language": "en",
  "word_count": 5,
  "mentions": ["@username"],
  "hashtags": ["#tag"],
  "content_type": "web",
  "performance": {
    "processing_time_ms": 16.2,
    "throughput_factor": "281x faster than BeautifulSoup"
  }
}
```

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "engine": "refinery-rust",
  "performance": "281x"
}
```

### GET /
API information

**Response:**
```json
{
  "name": "Refinery Cloud API",
  "description": "Ultra-fast HTML text extraction for AI agents",
  "performance": "281x faster than BeautifulSoup",
  "endpoints": {
    "extract": "/v1/refinery (POST)",
    "health": "/health (GET)"
  }
}
```

## Features

### Text Extraction
- Removes all HTML tags, scripts, styles
- Returns clean, readable text
- Preserves whitespace and structure

### Language Detection
- Supports 176 languages
- 85% confidence with heuristic optimization
- FastText model integration

### Social Feature Extraction
- **Mentions:** @username patterns
- **Hashtags:** #tag patterns
- **Content Type:** forum, news, social, web

### Performance
- **Processing Time:** ~1.02ms average
- **Throughput:** 281x faster than BeautifulSoup
- **Payload Limit:** 2MB maximum

## Error Handling

### 413 Payload Too Large
```json
{
  "detail": "Payload too large"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message"
}
```

## Usage Examples

### Basic Extraction
```python
import requests

response = requests.post("https://refinery-api.larelabs.com/v1/refinery", 
    json={"html": "<html><body><h1>Hello World</h1></body></html>"})
result = response.json()
print(result["html"])  # "Hello World"
```

### Batch Processing
```python
import requests

html_pages = ["<html>...</html>", "<html>...</html>"]
results = []

for html in html_pages:
    response = requests.post("https://refinery-api.larelabs.com/v1/refinery", 
        json={"html": html})
    results.append(response.json())
```

## Integration with AI Agents

### MCP Schema
```json
{
  "name": "refinery_extract",
  "description": "Extract clean text from HTML",
  "inputSchema": {
    "type": "object",
    "properties": {
      "html": {"type": "string", "description": "HTML content to process"}
    },
    "required": ["html"]
  }
}
```

### Cursor/Claude Integration
Add to MCP configuration:
```json
{
  "mcpServers": {
    "refinery": {
      "command": "python",
      "args": ["mcp_server_with_payments.py"]
    }
  }
}
```

## Performance Benchmarks

| Input Size | Processing Time | Throughput |
|------------|----------------|------------|
| 1KB HTML   | 0.8ms          | 1,250 req/s |
| 10KB HTML  | 16.2ms         | 62 req/s    |
| 100KB HTML | 45ms           | 22 req/s    |

*Based on actual server testing results*

## Security

- **Payload Validation:** 2MB size limit
- **UTF-8 Validation:** Ensures proper encoding
- **Input Sanitization:** Basic HTML tag removal
- **Rate Limiting:** Not implemented (configure per deployment)

## Deployment

### Docker
```bash
docker build -f Dockerfile.universal -t refinery-api .
docker run -p 8002:8002 refinery-api
```

### VPS Deployment
```bash
# Install dependencies
pip install -r requirements.production.txt

# Run server
python app/api.py
```

## Support

- **GitHub Issues:** https://github.com/LareLabs/refinery-html-to-llm-cleaner/issues
- **Documentation:** https://github.com/LareLabs/refinery-html-to-llm-cleaner
- **Performance:** Benchmarks available on request
