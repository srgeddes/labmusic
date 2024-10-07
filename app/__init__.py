from flask import Flask
from .config import Config
from .auth.routes.admin_routes import admin_bp
from .index.routes.index import index_bp
from .index.routes.spotipy import spotipy_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(spotipy_bp)
    app.register_blueprint(index_bp)

    return app
