from models.prompt import Favourite
from models import db

def add_favourite(user_id, prompt_id):
    existing = Favourite.query.filter_by(user_id=user_id, prompt_id=prompt_id).first()
    if not existing:
        fav = Favourite(user_id=user_id, prompt_id=int(prompt_id))
        db.session.add(fav)
        db.session.commit()
        return True
    return False

def remove_favourite(user_id, prompt_id):
    fav = Favourite.query.filter_by(user_id=user_id, prompt_id=prompt_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return True
    return False

def is_favourite(user_id, prompt_id):
    return Favourite.query.filter_by(user_id=user_id, prompt_id=int(prompt_id)).first() is not None

def get_user_favourites(user_id):
    return [f.prompt_id for f in Favourite.query.filter_by(user_id=user_id).all()]
