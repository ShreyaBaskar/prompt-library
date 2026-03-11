from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.prompt import Review, Rating
from models import db
from services.rating_service import add_rating

review_bp = Blueprint('reviews', __name__)

@review_bp.route('/api/add-review', methods=['POST'])
@login_required
def add_review():
    data = request.get_json()
    prompt_id = data.get('prompt_id')
    content = data.get('content', '').strip()
    stars = data.get('stars', 0)
    if not content:
        return jsonify({'success': False, 'error': 'Review cannot be empty'})
    review = Review(user_id=current_user.id, prompt_id=prompt_id,
                    reviewer_name=current_user.name, content=content)
    db.session.add(review)
    if stars:
        add_rating(current_user.id, prompt_id, int(stars))
    db.session.commit()
    return jsonify({'success': True, 'name': current_user.name, 'content': content})

@review_bp.route('/api/rate', methods=['POST'])
@login_required
def rate_prompt():
    data = request.get_json()
    prompt_id = data.get('prompt_id')
    stars = data.get('stars', 0)
    add_rating(current_user.id, prompt_id, int(stars))
    return jsonify({'success': True})
