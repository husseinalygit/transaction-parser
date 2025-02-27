from flask import Flask
from app.core.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)

    return app 