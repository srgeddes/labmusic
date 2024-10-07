from flask import Flask, render_template, request, redirect, url_for, session, flash
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time
from functools import wraps

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config["SESSION_COOKIE_NAME"] = "spotify-login-session"
app.config["QUEUE_ENABLED"] = True


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-playback-state user-modify-playback-state",
        cache_handler=None,
        show_dialog=True,
    )


def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        raise Exception("Token not found in session")

    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60

    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    return token_info


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "token_info" not in session:
            return redirect("/login")
        else:
            try:
                get_token()
            except Exception as e:
                print(e)
                return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/login")
def login():
    sp_auth = create_spotify_oauth()
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    sp_auth = create_spotify_oauth()
    code = request.args.get("code")
    token_info = sp_auth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("search"))


@app.route("/", methods=["GET", "POST"])
@login_required
def search():
    try:
        token_info = get_token()
    except Exception as e:
        print(e)
        return redirect("/login")

    sp = spotipy.Spotify(auth=token_info["access_token"])

    search_results = []
    if request.method == "POST":
        song_name = request.form.get("song_name")

        if song_name:
            spotify_results = sp.search(q=song_name, type="track")

            if spotify_results["tracks"]["items"]:
                seen_uris = set()
                for track in spotify_results["tracks"]["items"]:
                    if track["uri"] not in seen_uris:
                        seen_uris.add(track["uri"])
                        search_results.append(
                            {
                                "name": track["name"],
                                "artists": ", ".join(
                                    artist["name"] for artist in track["artists"]
                                ),
                                "album": track["album"]["name"],
                                "cover_url": (
                                    track["album"]["images"][0]["url"]
                                    if track["album"]["images"]
                                    else None
                                ),
                                "uri": track["uri"],
                            }
                        )
                    if len(search_results) == 10:
                        break

    queue_info = sp.queue()
    current_queue = []
    current_song = {}

    if queue_info["currently_playing"]:
        playing_song = queue_info["currently_playing"]
        current_song = {
            "name": playing_song["name"],
            "artists": ", ".join(artist["name"] for artist in playing_song["artists"]),
            "album": playing_song["album"]["name"],
            "cover_url": (
                playing_song["album"]["images"][0]["url"]
                if playing_song["album"]["images"]
                else None
            ),
            "uri": playing_song["uri"],
        }

    if queue_info["queue"]:
        for song in queue_info["queue"]:
            if len(current_queue) < 5:
                current_queue.append(
                    {
                        "name": song["name"],
                        "artists": ", ".join(
                            artist["name"] for artist in song["artists"]
                        ),
                        "album": song["album"]["name"],
                        "cover_url": (
                            song["album"]["images"][0]["url"]
                            if song["album"]["images"]
                            else None
                        ),
                        "uri": song["uri"],
                    }
                )

    return render_template(
        "index.html",
        search_results=search_results,
        current_queue=current_queue,
        current_song=current_song,
    )


@app.route("/queue", methods=["POST"])
@login_required
def queue():
    if app.config.get("QUEUE_ENABLED") == True:
        try:
            token_info = get_token()
        except Exception as e:
            print(e)
            return redirect("/login")

        sp = spotipy.Spotify(auth=token_info["access_token"])
        devices = sp.devices()
        active_device = any(
            device.get("is_active") for device in devices.get("devices", [])
        )
        if active_device:
            track_uri = request.form.get("track_uri")
            if track_uri:
                try:
                    sp.add_to_queue(track_uri)
                    flash("Song added to queue!", "success")
                    return redirect(url_for("search"))
                except spotipy.SpotifyException as e:
                    print(f"An error occurred: {e}")
                    flash(
                        "Song was not able to be added to the queue",
                        "danger",
                    )
            return redirect(url_for("search"))
        else:
            flash("No Device is availible to queue", "danger")
            return redirect(url_for("search"))
    else:
        flash("Queue is not enabled", "danger")
        return redirect(url_for("search"))


@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("search"))


@app.route("/admin_dashboard", methods=["GET", "POST"])
@admin_required
def admin_dashboard():
    if request.method == "POST":
        queue_enabled = request.form.get("toggle_queue") == "on"
        app.config["QUEUE_ENABLED"] = queue_enabled
        return redirect(url_for("admin_dashboard"))

    queue_enabled = app.config.get("QUEUE_ENABLED", False)
    return render_template("admin_dashboard.html", queue_enabled=queue_enabled)


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv(
            "ADMIN_PASSWORD"
        ):
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")


@app.route("/logout")
@admin_required
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("search"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
