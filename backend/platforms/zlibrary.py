import requests
import urllib3.exceptions
from typing import Dict, Any
import logging
from bs4 import BeautifulSoup
from .base import BookPlatform
from utils.errors import BookNotFoundError, SearchError

logger = logging.getLogger(__name__)

class ZLibrary(BookPlatform):
    """Z-Library platform implementation"""
    
    def __init__(self):
        super().__init__('zlibrary')
        self.platform_name = 'Z-Library'
        self.platform_id = 'zlibrary'  # 用于前端标识
        logger.info(f"Initialized ZLibrary platform with base_url: {self.base_url}")
    
    def search(self, keyword: str) -> Dict[str, Any]:
        """
        Search books on Z-Library
        Args:
            keyword: Search keyword
        Returns:
            Z-Library response with parsed book data
        Raises:
            SearchError: If search fails
        """
        url = f"{self.base_url}/s/{keyword}"
        logger.info(f"Searching Z-Library with URL: {url}")
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                verify=False
            )
            logger.info(f"Got response with status code: {response.status_code}")
            logger.debug(f"Response content preview: {response.text[:500]}")
            
            if response.status_code != 200:
                logger.error(f"Search failed with status {response.status_code}")
                raise SearchError(f"Search failed with status {response.status_code}", self.platform_name)
            
            # Parse the response content
            soup = BeautifulSoup(response.content, 'html.parser')
            books = []
            
            # Find all book cards
            book_cards = soup.find_all('z-bookcard')
            logger.info(f"Found {len(book_cards)} book cards")
            
            for book in book_cards:
                try:
                    # 记录原始HTML以便调试
                    logger.debug(f"Processing book card: {book}")
                    
                    # 从z-bookcard的属性中获取信息
                    book_info = {
                        # 基本信息
                        'title': book.find('div', attrs={'slot': 'title'}).get_text(strip=True) if book.find('div', attrs={'slot': 'title'}) else None,
                        'author': book.find('div', attrs={'slot': 'author'}).get_text(strip=True) if book.find('div', attrs={'slot': 'author'}) else 'Unknown',
                        'year': book.get('year'),
                        'isbn': book.get('isbn'),
                        'publisher': book.get('publisher', 'Unknown'),
                        
                        # 文件信息
                        'extension': book.get('extension'),
                        'filesize': book.get('filesize'),
                        'language': book.get('language', 'Unknown'),
                        
                        # 来源信息
                        'source': self.platform_name,
                        'platform_id': self.platform_id,
                        'book_url': f"{self.base_url}{book.get('href')}" if book.get('href') else None,
                        
                        # 额外信息
                        'pages': book.get('pages', 'Unknown'),
                        'quality': book.get('quality', '0.0'),
                        'rating': book.get('rating', '0.0'),
                    }
                    
                    # 只添加有标题和链接的书籍
                    if book_info['title'] and book_info['book_url']:
                        books.append(book_info)
                        logger.debug(f"Parsed book: {book_info}")
                    
                except Exception as e:
                    logger.error(f"Error parsing book card: {str(e)}")
                    continue
            
            logger.info(f"Successfully parsed {len(books)} books")
            
            return {
                'content': {
                    'books': books,
                    'total': len(books),
                    'platform_status': {
                        'id': self.platform_id,
                        'name': self.platform_name,
                        'available': len(books) > 0,
                        'total': len(books)
                    }
                },
                'status': 200,
                'headers': {'content-type': 'application/json'}
            }
            
        except requests.Timeout:
            logger.error("Request timed out")
            raise SearchError("Request timed out", self.platform_name)
        except urllib3.exceptions.SSLError as e:
            logger.error(f"SSL error: {str(e)}")
            raise SearchError(f"SSL error: {str(e)}", self.platform_name)
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise SearchError(f"Request failed: {str(e)}", self.platform_name)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise SearchError(f"Unexpected error: {str(e)}", self.platform_name)
    
    def get_book_detail(self, book_id: str) -> Dict[str, Any]:
        """
        Get book details from Z-Library
        Args:
            book_id: Book identifier
        Returns:
            Book details
        Raises:
            BookNotFoundError: If book is not found
            SearchError: If request fails
        """
        url = f"{self.base_url}/book/{book_id}"
        logger.info(f"Getting book details from URL: {url}")
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            logger.info(f"Got response with status code: {response.status_code}")
            
            if response.status_code == 404:
                logger.error(f"Book {book_id} not found")
                raise BookNotFoundError(book_id, self.platform_name)
                
            return self._handle_response(
                response,
                f"Failed to get details for book '{book_id}'"
            )
        except Exception as e:
            logger.error(f"Error getting book details: {str(e)}")
            raise 