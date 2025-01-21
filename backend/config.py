from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management"""
    
    # Platform configurations
    PLATFORMS: Dict[str, Dict[str, Any]] = {
        'zlibrary': {
            'base_url': os.getenv('ZLIBRARY_BASE_URL', 'https://z-library.sk'),
            'timeout': int(os.getenv('ZLIBRARY_TIMEOUT', '10')),
            'max_retries': int(os.getenv('ZLIBRARY_MAX_RETRIES', '3'))
        }
    }
    
    # Global settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    
    # Request settings
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    # Cache settings
    ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'False').lower() == 'true'
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '3600'))  # 1 hour 