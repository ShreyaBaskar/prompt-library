from models.prompt import Rating
from models import db

def add_rating(user_id, prompt_id, stars):
    # Update existing or create new
    existing = Rating.query.filter_by(user_id=user_id, prompt_id=prompt_id).first()
    if existing:
        existing.stars = stars
    else:
        r = Rating(user_id=user_id, prompt_id=prompt_id, stars=stars)
        db.session.add(r)
    db.session.commit()

def get_user_rating(user_id, prompt_id):
    r = Rating.query.filter_by(user_id=user_id, prompt_id=prompt_id).first()
    return r.stars if r else 0
