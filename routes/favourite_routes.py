from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from services.favourite_service import add_favourite, remove_favourite, get_user_favourites
from services.prompt_service import get_prompt, get_avg_rating, get_review_count

favourite_bp = Blueprint('favourites', __name__)

@favourite_bp.route('/favourites')
@login_required
def list_favourites():
    fav_ids = get_user_favourites(current_user.id)
    prompts = []
    for pid in fav_ids:
        p = get_prompt(pid)
        if p:
            prompts.append({
                **p,
                'avg_rating': get_avg_rating(p['id']),
                'review_count': get_review_count(p['id']),
                'is_fav': True
            })
    return render_template('favourites.html', prompts=prompts)

@favourite_bp.route('/api/toggle-favourite', methods=['POST'])
@login_required
def toggle_favourite():
    data = request.get_json()
    prompt_id = data.get('prompt_id')
    fav_ids = get_user_favourites(current_user.id)
    if int(prompt_id) in fav_ids:
        remove_favourite(current_user.id, prompt_id)
        return jsonify({'success': True, 'action': 'removed'})
    else:
        add_favourite(current_user.id, prompt_id)
        return jsonify({'success': True, 'action': 'added'})
