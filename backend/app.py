# -*- coding: utf-8 -*-
from flask import Flask, Response, jsonify
from platforms import PlatformFactory
from utils.errors import BookSearchError
from config import Config
import logging
import os
from logging.handlers import RotatingFileHandler
from flask_cors import CORS

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create file handler
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=1024 * 1024,  # 1MB
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# Get logger
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

app = Flask(__name__)
CORS(app)  # 启用CORS支持

@app.errorhandler(BookSearchError)
def handle_book_search_error(error):
    """Global error handler for book search errors"""
    logger.error(f"Book search error: {str(error)}")
    return jsonify({'error': str(error)}), error.status_code

@app.route('/<platform>/s/<keyword>')
def search(platform: str, keyword: str):
    """
    Search books on specified platform
    Args:
        platform: Platform name (e.g., 'zlibrary')
        keyword: Search keyword
    """
    logger.info(f"Received search request - Platform: {platform}, Keyword: {keyword}")
    
    try:
        platform_instance = PlatformFactory.get_platform(platform)
        result = platform_instance.search(keyword)
        
        # Log search results
        if isinstance(result['content'], dict):
            total_books = result['content'].get('total', 0)
            logger.info(f"Search completed - Found {total_books} books")
        
        return jsonify(result['content']), result['status']
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise

@app.route('/<platform>/book/<book_id>')
def get_book(platform: str, book_id: str):
    """
    Get book details from specified platform
    Args:
        platform: Platform name (e.g., 'zlibrary')
        book_id: Book identifier
    """
    logger.info(f"Received book detail request - Platform: {platform}, Book ID: {book_id}")
    
    try:
        platform_instance = PlatformFactory.get_platform(platform)
        result = platform_instance.get_book_detail(book_id)
        return jsonify(result['content']), result['status']
    except Exception as e:
        logger.error(f"Get book detail failed: {str(e)}")
        raise

if __name__ == '__main__':
    logger.info(f"Starting server - Debug: {Config.DEBUG}, Host: {Config.HOST}, Port: {Config.PORT}")
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )