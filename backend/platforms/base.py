from abc import ABC, abstractmethod
from typing import Dict, Any
from config import Config
from utils.errors import SearchError, BookNotFoundError
from utils.decorators import retry_on_failure, cache_response

class BookPlatform(ABC):
    """Base class for book search platforms"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.config = Config.PLATFORMS.get(platform_name, {})
        self.headers = Config.DEFAULT_HEADERS
        self.base_url = self.config.get('base_url', '')
        self.timeout = self.config.get('timeout', 10)
        self.max_retries = self.config.get('max_retries', 3)
    
    @abstractmethod
    @retry_on_failure()
    @cache_response()
    def search(self, keyword: str) -> Dict[str, Any]:
        """
        Search books with the given keyword
        Args:
            keyword: Search keyword
        Returns:
            Response data from the platform
        Raises:
            SearchError: If search operation fails
        """
        pass
    
    @abstractmethod
    @retry_on_failure()
    @cache_response()
    def get_book_detail(self, book_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific book
        Args:
            book_id: Book identifier
        Returns:
            Book details
        Raises:
            BookNotFoundError: If book is not found
            SearchError: If operation fails
        """
        pass
    
    def _handle_response(self, response: Any, error_msg: str) -> Dict[str, Any]:
        """
        Handle response and check for errors
        Args:
            response: Response object
            error_msg: Error message if request fails
        Returns:
            Processed response data
        Raises:
            SearchError: If request fails
        """
        if not hasattr(response, 'status_code') or response.status_code != 200:
            raise SearchError(error_msg, self.platform_name)
            
        return {
            'content': response.content,
            'status': response.status_code,
            'headers': dict(response.headers)
        } 