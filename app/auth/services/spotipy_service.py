from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from flask import session, redirect, url_for, request
from app.config import Config

sp_oauth = SpotifyOAuth(
    client_id=Config.SPOTIPY_CLIENT_ID,
    client_secret=Config.SPOTIPY_CLIENT_SECRET,
    redirect_uri=Config.SPOTIPY_REDIRECT_URI,
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing",
)


def get_spotify_client():
    token_info = session.get("token_info")

    # Check if the token is expired
    if not token_info or sp_oauth.is_token_expired(token_info):
        try:

            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            session["token_info"] = token_info
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return redirect(
                url_for("routes.login_route")
            )  # Redirect to login if refresh fails

    sp = Spotify(auth=token_info["access_token"])
    return sp


def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("index.index"))  # Redirect to your main index page
