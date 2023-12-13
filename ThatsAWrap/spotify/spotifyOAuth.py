from flask import Flask, request, url_for, session, redirect 
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import os
from dotenv import load_dotenv
import requests
import time

# load environment variables
load_dotenv() 
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


SPOTIFY_SCOPE = "user-top-read playlist-modify-public playlist-modify-private"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
        cache_path=session.get('cache_path')
    )

def spotify_redirect():
    sp_oauth = create_spotify_oauth()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    header = {"Authorization": f"Bearer {token_info['access_token']}"}
    user_profile = requests.get("https://api.spotify.com/v1/me", headers=header).json()
    session['spotify_user_id'] = user_profile.get['id']
    session['token_info'] = token_info
    return token_info

def refresh_spotify_token():
    token_info = session.get('token_info')
    if token_info:
        now = int(time.time())
        is_token_expired = token_info['expires_at'] - now < 60
        if is_token_expired:
            sp_oauth = create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
    else:
        raise 'Missing token info'
    return token_info

def create_playlist(user_id, token):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'name': 'My Top Tracks',
        'description': 'My top tracks of the month',
        'public': False  # Set to True if you want the playlist to be public
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json().get('id')

def add_tracks_to_playlist(playlist_id, tracks, token):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    track_uris = [track['uri'] for track in tracks]
    payload = {
        'uris': track_uris
    }
    requests.post(url, headers=headers, json=payload)




