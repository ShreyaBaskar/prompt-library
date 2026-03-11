from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.prompt import Review, Rating, Usage
from services.prompt_service import get_all_prompts
from services.usage_service import get_total_usage

admin_bp = Blueprint('admin', __name__)

def require_owner(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_owner():
            abort(403)
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/admin')
@login_required
@require_owner
def dashboard():
    total_users = User.query.count()
    total_prompts = len(get_all_prompts())
    total_reviews = Review.query.count()
    total_usages = get_total_usage()
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_prompts=total_prompts,
                           total_reviews=total_reviews,
                           total_usages=total_usages,
                           recent_reviews=recent_reviews)

@admin_bp.route('/admin/delete-review/<int:review_id>', methods=['POST'])
@login_required
@require_owner
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'success': True})
