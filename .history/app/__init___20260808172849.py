from flask import Flask

from config import Config

from .ai import ai_bp
from .extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .documents import documents_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(documents_bp)

    with app.app_context():
        db.create_all()

    return app




