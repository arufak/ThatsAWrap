# main views or url endpoints for frontend 

from flask import Blueprint, render_template, Flask, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from spotify.spotifyOAuth import create_spotify_oauth, create_playlist, add_tracks_to_playlist
import requests
import time
from . import db
from backend.models import User, db 


views = Blueprint('views', __name__)

@views.route('/spotifyRedirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    user_id = session.get("user_id")
    auth_code = request.args.get("code")
    token_info = sp_oauth.get_access_token(auth_code)
    access_token = token_info['access_token']
    token_expiration = token_info['expires_at']
    refresh_token = token_info['refresh_token']
    update_user = User.query.filter_by(user_id=user_id).first()
    update_user.spotify_access_token = access_token
    update_user.spotify_token_expiration = token_expiration
    update_user.spotify_refresh_token = refresh_token
    db.session.commit()

@views.route('/home')
def spotifyLogin():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)




