"""
Refinery HTML to Text Cleaner - Apify Actor (Pure Python)
Ultra-fast HTML text extraction for RAG and AI agents
"""

import asyncio
import json
import time
import re
import httpx
from apify import Actor

def extract_text_simple(html: str, remove_scripts: bool = True, remove_styles: bool = True) -> dict:
    """Simple HTML text extraction using regex"""
    start_time = time.time()
    
    text = html
    
    # Remove script tags
    if remove_scripts:
        script_regex = re.compile(r'<script[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
        text = script_regex.sub('', text)
        scripts_removed = True
    else:
        scripts_removed = False
    
    # Remove style tags
    if remove_styles:
        style_regex = re.compile(r'<style[^>]*>.*?</style>', re.DOTALL | re.IGNORECASE)
        text = style_regex.sub('', text)
        styles_removed = True
    else:
        styles_removed = False
    
    # Remove all HTML tags
    html_regex = re.compile(r'<[^>]*>')
    text = html_regex.sub(' ', text)
    
    # Clean up whitespace
    whitespace_regex = re.compile(r'\s+')
    text = whitespace_regex.sub(' ', text.strip())
    
    # Calculate processing time
    processing_time = (time.time() - start_time) * 1000
    
    return {
        'extracted_text': text,
        'processing_time_ms': round(processing_time, 2),
        'scripts_removed': scripts_removed,
        'styles_removed': styles_removed,
        'original_size': len(html),
        'cleaned_size': len(text)
    }

async def fetch_url(url: str) -> str:
    """Fetch HTML content from a URL"""
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

async def main():
    async with Actor:
        # Get input from Apify
        input_data = await Actor.get_input() or {}
        
        # Get options
        include_metadata = input_data.get('includeMetadata', True)
        remove_scripts = input_data.get('removeScripts', True)
        remove_styles = input_data.get('removeStyles', True)
        extract_mentions = input_data.get('extractMentions', False)
        extract_hashtags = input_data.get('extractHashtags', False)
        
        # Get HTML content (either raw_payload or URLs)
        raw_payload = input_data.get('raw_payload', '')
        urls = input_data.get('urls', [])
        
        # If URLs provided, fetch HTML
        if urls and not raw_payload:
            Actor.log.info(f'Fetching {len(urls)} URLs')
            html_contents = []
            for url in urls:
                try:
                    html = await fetch_url(url)
                    html_contents.append(html)
                    Actor.log.info(f'Fetched {url} ({len(html)} bytes)')
                except Exception as e:
                    Actor.log.error(f'Failed to fetch {url}: {str(e)}')
            # Combine all HTML if multiple URLs
            html = '\n\n'.join(html_contents) if html_contents else ''
        else:
            html = raw_payload
        
        if not html:
            Actor.log.error('No HTML provided in input')
            raise ValueError('No HTML provided in input')
        
        # Validate payload size (10MB limit)
        if len(html) > 10 * 1024 * 1024:
            Actor.log.error('Payload too large (max 10MB)')
            raise ValueError('Payload too large (max 10MB)')
        
        Actor.log.info(f'Processing HTML payload ({len(html)} bytes)')
        
        try:
            # Process HTML with simple Python implementation
            result = extract_text_simple(html, remove_scripts, remove_styles)
            result['success'] = True
            
            # Apply options
            if not include_metadata:
                # Keep only essential fields
                result = {
                    'extracted_text': result.get('extracted_text', ''),
                    'success': result.get('success', True)
                }
            
            if not extract_mentions:
                result.pop('mentions', None)
            
            if not extract_hashtags:
                result.pop('hashtags', None)
            
            Actor.log.info(f'Extraction complete in {result["processing_time_ms"]:.2f}ms')
            
            # Push output to Apify
            await Actor.push_data(result)
            
            Actor.log.info('Output pushed successfully')
            
        except Exception as e:
            Actor.log.error(f'Extraction failed: {str(e)}')
            Actor.log.error(f'Exception type: {type(e).__name__}')
            raise

if __name__ == '__main__':
    asyncio.run(main())
