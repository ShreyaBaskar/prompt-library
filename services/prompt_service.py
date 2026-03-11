from utils.prompt_loader import load_prompts, get_prompt_by_id, get_all_categories
from models.prompt import Rating, Review
from models import db
import random

def get_all_prompts():
    return load_prompts()

def get_prompt(prompt_id):
    return get_prompt_by_id(prompt_id)

def get_categories():
    return get_all_categories()

def get_prompts_by_category(category):
    prompts = load_prompts()
    return [p for p in prompts if p.get('category') == category or p.get('subcategory') == category]

def get_avg_rating(prompt_id):
    ratings = Rating.query.filter_by(prompt_id=prompt_id).all()
    if not ratings:
        return round(random.uniform(3.5, 5.0), 1)
    return round(sum(r.stars for r in ratings) / len(ratings), 1)

def get_review_count(prompt_id):
    db_count = Review.query.filter_by(prompt_id=prompt_id).count()
    # Add seeded baseline so prompts don't start at 0
    seed_count = (prompt_id * 7 + 3) % 15 + 2
    return db_count + seed_count

def seed_ratings_if_needed(prompt_id):
    """Ensure every prompt has at least a baseline rating."""
    existing = Rating.query.filter_by(prompt_id=prompt_id, user_id=None).first()
    if not existing:
        stars = random.randint(4, 5)
        r = Rating(user_id=None, prompt_id=prompt_id, stars=stars)
        db.session.add(r)
        db.session.commit()
