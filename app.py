import os
from flask import Flask, render_template
from flask_login import LoginManager
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.prompt_routes import prompt_bp
    from routes.search_routes import search_bp
    from routes.favourite_routes import favourite_bp
    from routes.review_routes import review_bp
    from routes.profile_routes import profile_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(favourite_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)

    # Main index route
    @app.route('/')
    def index():
        from services.prompt_service import get_all_prompts, get_avg_rating, get_review_count
        from services.favourite_service import get_user_favourites
        from flask_login import current_user
        prompts = get_all_prompts()
        fav_ids = get_user_favourites(current_user.id) if current_user.is_authenticated else []
        featured = []
        for p in prompts[:6]:
            featured.append({
                **p,
                'avg_rating': get_avg_rating(p['id']),
                'review_count': get_review_count(p['id']),
                'is_fav': p['id'] in fav_ids
            })
        return render_template('index.html', featured_prompts=featured, total_prompts=len(prompts))

    @app.route('/categories')
    def categories():
        from services.prompt_service import get_categories, get_all_prompts
        categories = get_categories()
        prompts = get_all_prompts()
        return render_template('categories.html', categories=categories, prompts=prompts)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', code=403, message='Access Forbidden'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html', code=404, message='Page Not Found'), 404

    # Init DB tables
    with app.app_context():
        db.create_all()
        _seed_default_owner(app)

    return app

def _seed_default_owner(app):
    from models.user import User
    with app.app_context():
        if not User.query.filter_by(email='admin@promptlibrary.com').first():
            owner = User(name='Admin', email='admin@promptlibrary.com', role='owner')
            owner.set_password('admin123')
            db.session.add(owner)
            db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
