from flask import Flask, request, url_for, session, redirect 
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import os
from dotenv import load_dotenv
import requests
import time
from backend.models import User, db 

# load environment variables
load_dotenv() 
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read,user-library-modify,playlist-modify-private,ugc-image-upload'
    )

def create_playlist(token, name):
    sp_oauth = create_spotify_oauth()
    code = token
    playlist_name = name
    token_info = sp_oauth.get_access_token(code)
    spotify_object = spotipy.Spotify(auth=token_info['access_token'])
    user_id = spotify_object.current_user()['id'] 
    create_playlist = spotify_object.user_playlist_create(user_id,playlist_name,False,False,'Your Top 10 Wrapped')
    return create_playlist['id'] 

def add_tracks_to_playlist(token, playlist_id, track_list):
    sp_oauth = create_spotify_oauth()
    code = token
    token_info = sp_oauth.get_access_token(code)
    spotify_object = spotipy.Spotify(auth=token_info['access_token'])
    add_to_playlist = spotify_object.playlist_add_items(playlist_id,track_list)
    return add_to_playlist 











