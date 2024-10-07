from flask import Blueprint
from ...auth.services.spotipy_service import login, callback

spotipy_bp = Blueprint("sptipy", __name__)


@spotipy_bp.route("/login")
def login_route():
    return login()


@spotipy_bp.route("/callback")
def callback_route():
    return callback()
