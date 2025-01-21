class BookSearchError(Exception):
    """Base exception for book search errors"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code

class PlatformNotFoundError(BookSearchError):
    """Raised when platform is not supported"""
    def __init__(self, platform: str):
        super().__init__(f"Platform {platform} is not supported", 400)

class SearchError(BookSearchError):
    """Raised when search operation fails"""
    def __init__(self, message: str, platform: str):
        super().__init__(f"Search failed on {platform}: {message}", 500)

class BookNotFoundError(BookSearchError):
    """Raised when book is not found"""
    def __init__(self, book_id: str, platform: str):
        super().__init__(f"Book {book_id} not found on {platform}", 404) 