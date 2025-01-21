import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import urllib.parse

async def search_zlibrary(session, keyword):
    """Search Z-Library for books"""
    try:
        # URL encode the keyword
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://z-library.sk/s/{encoded_keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        async with session.get(url, headers=headers, timeout=30) as response:
            if response.status != 200:
                print(f"Error: Received status code {response.status} from Z-Library")
                return []
                
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            results = []
            books = soup.find_all('div', class_='resItemBox')
            
            if not books:
                print("Warning: No books found in the response HTML")
                return []
            
            for book in books:
                try:
                    title_elem = book.find('h3', class_='title')
                    author_elem = book.find('div', class_='authors')
                    year_elem = book.find('div', class_='property_year')
                    download_elem = book.find('a', class_='dlButton')
                    
                    if title_elem and download_elem:
                        result = {
                            'title': title_elem.get_text(strip=True),
                            'author': author_elem.get_text(strip=True) if author_elem else 'Unknown',
                            'year': year_elem.get_text(strip=True) if year_elem else 'Unknown',
                            'download_url': download_elem.get('href', ''),
                            'source': 'Z-Library'
                        }
                        results.append(result)
                except Exception as e:
                    print(f"Error parsing book element: {str(e)}")
                    continue
            
            return results
    except asyncio.TimeoutError:
        print(f"Timeout while searching Z-Library for: {keyword}")
        return []
    except Exception as e:
        print(f"Error searching Z-Library: {str(e)}")
        return []

def is_isbn(keyword):
    """Check if the keyword is an ISBN (10 or 13 digits)"""
    isbn_pattern = re.compile(r'^(?:\d{10}|\d{13})$')
    return bool(isbn_pattern.match(keyword.replace('-', '')))

async def search_all_sources(keyword):
    """Search all configured sources for a single book"""
    async with aiohttp.ClientSession() as session:
        try:
            results = await search_zlibrary(session, keyword)
            return results
        except Exception as e:
            print(f"Error in search_all_sources: {str(e)}")
            return []

def search_books(keywords, page=1, per_page=10):
    """Main search function that coordinates the search across all sources"""
    if not keywords:
        return {'error': 'No keywords provided'}
    
    # Clean up the input - we only take the first keyword now
    keyword = keywords.split(',')[0].strip()
    if not keyword:
        return {'error': 'Invalid keyword'}
    
    # Run async search
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        all_results = loop.run_until_complete(search_all_sources(keyword))
    except Exception as e:
        print(f"Error in search_books: {str(e)}")
        all_results = []
    finally:
        loop.close()
    
    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_results = all_results[start_idx:end_idx]
    
    return {
        'results': paginated_results,
        'total': len(all_results),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(all_results) + per_page - 1) // per_page
    } 