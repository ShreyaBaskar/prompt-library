from flask import Blueprint, render_template, request, jsonify, session
from flask_login import current_user, login_required
from services.prompt_service import get_all_prompts, get_prompt, get_categories, get_avg_rating, get_review_count
from services.favourite_service import is_favourite, get_user_favourites
from services.usage_service import track_usage, can_guest_use, get_guest_usage_count
from services.personalization_service import personalize_prompt
from models.prompt import Review
import uuid

prompt_bp = Blueprint('prompts', __name__)

def _get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@prompt_bp.route('/prompts')
def list_prompts():
    prompts = get_all_prompts()
    categories = get_categories()
    fav_ids = get_user_favourites(current_user.id) if current_user.is_authenticated else []
    prompt_data = []
    for p in prompts:
        prompt_data.append({
            **p,
            'avg_rating': get_avg_rating(p['id']),
            'review_count': get_review_count(p['id']),
            'is_fav': p['id'] in fav_ids
        })
    return render_template('prompts.html', prompts=prompt_data, categories=categories)

@prompt_bp.route('/prompts/<int:prompt_id>')
def view_prompt(prompt_id):
    prompt = get_prompt(prompt_id)
    if not prompt:
        return "Prompt not found", 404
    reviews = Review.query.filter_by(prompt_id=prompt_id).order_by(Review.created_at.desc()).limit(5).all()
    fav = is_favourite(current_user.id, prompt_id) if current_user.is_authenticated else False
    avg_rating = get_avg_rating(prompt_id)
    personalized = None
    if current_user.is_authenticated:
        personalized = personalize_prompt(prompt['template'], current_user)
    return render_template('prompt_detail.html', prompt=prompt, reviews=reviews,
                           is_fav=fav, avg_rating=avg_rating, personalized=personalized)

@prompt_bp.route('/api/copy-prompt', methods=['POST'])
def copy_prompt():
    data = request.get_json()
    prompt_id = data.get('prompt_id')
    sid = _get_session_id()
    uid = current_user.id if current_user.is_authenticated else None
    if uid is None and not can_guest_use(sid):
        return jsonify({'success': False, 'error': 'Guest limit reached. Please log in.', 'limit_reached': True})
    track_usage(uid, sid, prompt_id, 'copy')
    prompt = get_prompt(prompt_id)
    if not prompt:
        return jsonify({'success': False, 'error': 'Prompt not found'})
    template = prompt['template']
    if current_user.is_authenticated:
        template = personalize_prompt(template, current_user)
    remaining = None
    if uid is None:
        used = get_guest_usage_count(sid)
        remaining = max(0, 5 - used)
    return jsonify({'success': True, 'template': template, 'remaining': remaining})
