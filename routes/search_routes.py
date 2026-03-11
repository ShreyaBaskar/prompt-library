from flask import Blueprint, render_template, request
from services.search_service import keyword_search, filter_by_category
from services.semantic_search_service import semantic_search
from services.prompt_service import get_avg_rating, get_review_count, get_categories
from services.favourite_service import get_user_favourites
from flask_login import current_user

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    mode = request.args.get('mode', 'keyword')
    categories = get_categories()
    results = []
    if query:
        if mode == 'smart':
            results = semantic_search(query)
        else:
            results = keyword_search(query, category or None)
    elif category:
        results = filter_by_category(category)
    fav_ids = get_user_favourites(current_user.id) if current_user.is_authenticated else []
    prompt_data = [{
        **p,
        'avg_rating': get_avg_rating(p['id']),
        'review_count': get_review_count(p['id']),
        'is_fav': p['id'] in fav_ids
    } for p in results]
    return render_template('search.html', prompts=prompt_data, query=query,
                           category=category, mode=mode, categories=categories)
