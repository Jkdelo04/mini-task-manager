import os
from flask import Flask
from .extensions import db, bcrypt, migrate, login_manager
from .models import User
from .routes.auth_routes import auth_bp
from .routes.task_routes import task_bp

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from config.py
    app.config.from_object(config_class)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # points to auth blueprint's login route

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints WITHOUT url_prefix
    # This means login is at /login, register at /register, etc.
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
