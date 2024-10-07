from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.spotipy_service import (
    get_spotify_client,
    search_action,
    get_queue,
    get_now_playing,
    add_to_queue,
)

index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET", "POST"])
def index():
    sp = get_spotify_client()

    search_results = []
    current_song = None
    current_queue = []

    if request.method == "POST":
        search_results = search_action(request.form.get("song_name"), sp)

    try:
        current_song = get_now_playing(sp)
        current_queue = get_queue(sp)
    except Exception as e:
        print(f"Error fetching now playing or queue: {e}")

    return render_template(
        "index.html",
        search_results=search_results,
        current_song=current_song,
        current_queue=current_queue,
    )


@index_bp.route("/queue", methods=["POST"])
def queue_action():
    sp = get_spotify_client()

    track_uri = request.form.get("track_uri")
    if not track_uri:
        return redirect(url_for("index.index"))

    try:
        add_to_queue(track_uri, sp)
        flash("Song Queued", "success")
    except Exception as e:
        flash("Error while trying to queue", "danger")

    return redirect(url_for("index.index"))
