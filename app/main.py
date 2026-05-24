"""
Refinery Cloud API - FastAPI Server
281x faster HTML extraction for AI agents
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import hashlib
import time
import json
from typing import Optional, Dict, Any
import logging

# Add refinery core to path
sys.path.append('/root/ACTIVE_PROJECTS/refinery/refinery-rust/refinery_core_src')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Refinery Cloud API",
    description="281x faster HTML extraction for AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pricing tiers
TIER_LIMITS = {
    "free": 500,
    "starter": 10000,
    "pro": 100000,
    "scale": 1000000,
    "enterprise": float('inf')
}

# Mock database (replace with real DB)
API_KEYS = {
    "test_key_free": {"tier": "free", "usage": 0, "limit": 500},
    "test_key_starter": {"tier": "starter", "usage": 0, "limit": 10000},
    "test_key_pro": {"tier": "pro", "usage": 0, "limit": 100000},
}

# Request models
class ExtractRequest(BaseModel):
    html: str
    selector: Optional[str] = None

class ExtractResponse(BaseModel):
    text: str
    language: str
    word_count: int
    mentions: list
    hashtags: list
    content_type: str
    processing_time: float
    success: bool

class UsageResponse(BaseModel):
    tier: str
    usage: int
    limit: int
    remaining: int
    reset_date: str

class ConfigSnippetResponse(BaseModel):
    mcp_config: str
    instructions: str

# Utility functions
def hash_api_key(api_key: str) -> str:
    """Hash API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def validate_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate API key and return user info"""
    api_key = credentials.credentials
    
    # Mock validation (replace with real DB lookup)
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    user_info = API_KEYS[api_key]
    
    # Check usage limits
    if user_info["usage"] >= user_info["limit"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Usage limit exceeded"
        )
    
    return user_info

def track_usage(api_key: str, user_info: Dict[str, Any]):
    """Track API usage"""
    user_info["usage"] += 1
    logger.info(f"API key {api_key[:8]}... usage: {user_info['usage']}/{user_info['limit']}")

# Import Refinery core
try:
    import refinery_core
    REFINERY_AVAILABLE = True
    logger.info("Refinery Rust core loaded successfully")
except ImportError as e:
    REFINERY_AVAILABLE = False
    logger.warning(f"Refinery core not available: {e}")

def refinery_extract_text(html: str, selector: Optional[str] = None) -> Dict[str, Any]:
    """
    Real Refinery extraction using Rust core
    """
    start_time = time.time()
    
    if REFINERY_AVAILABLE:
        try:
            # Call actual Refinery Rust function
            result = refinery_core.refinery_json(html)
            
            # Parse the JSON result
            if isinstance(result, str):
                import json
                result = json.loads(result)
            
            processing_time = time.time() - start_time
            
            return {
                "text": result.get("text", ""),
                "language": result.get("language", "unknown"),
                "word_count": result.get("word_count", 0),
                "mentions": result.get("mentions", []),
                "hashtags": result.get("hashtags", []),
                "content_type": result.get("content_type", "web"),
                "processing_time": processing_time * 1000,  # Convert to ms
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Refinery extraction failed: {e}")
            # Fallback to basic extraction
            return _fallback_extraction(html, start_time)
    else:
        # Fallback extraction when Refinery not available
        return _fallback_extraction(html, start_time)

def _fallback_extraction(html: str, start_time: float) -> Dict[str, Any]:
    """Fallback extraction when Refinery core unavailable"""
    import re
    
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract text
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    
    processing_time = time.time() - start_time
    
    return {
        "text": text[:1000],  # Limit for demo
        "language": "en",  # Mock detection
        "word_count": len(text.split()),
        "mentions": [],  # Mock extraction
        "hashtags": [],  # Mock extraction
        "content_type": "web",  # Mock detection
        "processing_time": processing_time * 1000,  # Convert to ms
        "success": True
    }

# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Refinery Cloud API",
        "description": "281x faster HTML extraction for AI agents",
        "version": "1.0.0",
        "status": "operational"
    }

@app.post("/extract", response_model=ExtractResponse)
async def extract_text(
    request: ExtractRequest,
    user_info: Dict[str, Any] = Depends(validate_api_key)
):
    """
    Extract clean text from HTML
    
    - **html**: HTML content to process
    - **selector**: Optional CSS selector (not implemented yet)
    """
    try:
        # Track usage
        api_key = "mock_key"  # Get from request context
        track_usage(api_key, user_info)
        
        # Extract text using Refinery
        result = refinery_extract_text(request.html, request.selector)
        
        return ExtractResponse(**result)
        
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}"
        )

@app.get("/usage", response_model=UsageResponse)
async def get_usage(user_info: Dict[str, Any] = Depends(validate_api_key)):
    """Get current usage statistics"""
    from datetime import datetime, timedelta
    
    reset_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    return UsageResponse(
        tier=user_info["tier"],
        usage=user_info["usage"],
        limit=user_info["limit"],
        remaining=user_info["limit"] - user_info["usage"],
        reset_date=reset_date
    )

@app.get("/config", response_model=ConfigSnippetResponse)
async def get_mcp_config():
    """Get MCP configuration snippet"""
    config = {
        "mcpServers": {
            "refinery": {
                "command": "python",
                "args": ["-m", "refinery_mcp"],
                "env": {
                    "REFINERY_API_KEY": "your_api_key_here"
                }
            }
        }
    }
    
    return ConfigSnippetResponse(
        mcp_config=json.dumps(config, indent=2),
        instructions="Add this to your Claude Desktop config to use Refinery Cloud"
    )

@app.get("/pricing")
async def get_pricing():
    """Get pricing information"""
    return {
        "tiers": [
            {"name": "Free", "price": 0, "pages": 500, "features": ["Basic extraction", "Rate limited"]},
            {"name": "Starter", "price": 15, "pages": 10000, "features": ["All features", "Priority support"]},
            {"name": "Pro", "price": 50, "pages": 100000, "features": ["All features", "Analytics", "Priority support"]},
            {"name": "Scale", "price": 200, "pages": 1000000, "features": ["All features", "Custom integrations", "Dedicated support"]},
            {"name": "Enterprise", "price": "Custom", "pages": "Unlimited", "features": ["Self-hosted", "Custom features", "24/7 support"]}
        ],
        "per_request": 0.001,  # $0.001 per request overage
        "speed_advantage": "281x faster than competitors"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# Development server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
