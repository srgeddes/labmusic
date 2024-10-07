from flask import request
from ...auth.services.spotipy_service import get_spotify_client


def search_action(search_request, sp):

    search_results = []
    if search_request:
        spotify_results = sp.search(q=search_request, type="track")

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
    return search_results


def get_queue(sp):

    queue_info = sp.queue()
    current_queue = []

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

            current_queue.append(
                {
                    "name": song["name"],
                    "artists": ", ".join(artist["name"] for artist in song["artists"]),
                    "album": song["album"]["name"],
                    "cover_url": (
                        song["album"]["images"][0]["url"]
                        if song["album"]["images"]
                        else None
                    ),
                    "uri": song["uri"],
                }
            )
    return current_queue


def get_now_playing(sp):

    playback_info = sp.current_playback()

    if not playback_info or not playback_info.get("item"):
        return None

    playing_song = playback_info["item"]
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

    return current_song


def add_to_queue(track_uri, sp):
    sp.add_to_queue(track_uri)


def get_sp():
    try:
        sp = get_spotify_client()
    except Exception as e:
        print(e)
        return None
    return sp
