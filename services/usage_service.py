from models.prompt import Usage
from models import db

GUEST_LIMIT = 5

def track_usage(user_id, session_id, prompt_id, action='copy'):
    u = Usage(user_id=user_id, session_id=session_id, prompt_id=int(prompt_id), action=action)
    db.session.add(u)
    db.session.commit()

def get_guest_usage_count(session_id):
    return Usage.query.filter_by(session_id=session_id, user_id=None).count()

def can_guest_use(session_id):
    return get_guest_usage_count(session_id) < GUEST_LIMIT

def get_total_usage():
    return Usage.query.count()

def get_usage_by_prompt(prompt_id):
    return Usage.query.filter_by(prompt_id=prompt_id).count()
