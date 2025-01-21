from flask import Blueprint, request, jsonify
from .search import search_books

main = Blueprint('main', __name__)

@main.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data or 'keywords' not in data:
        return jsonify({'error': 'No keywords provided'}), 400
    
    keywords = data['keywords']
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    
    try:
        results = search_books(keywords, page, per_page)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}) 