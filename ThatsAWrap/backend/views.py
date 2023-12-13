# main views or url endpoints for frontend 

from flask import Blueprint, render_template, Flask, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from spotify.spotifyOAuth import create_spotify_oauth, spotify_redirect, create_playlist, add_tracks_to_playlist, refresh_spotify_token
import requests
import time


bp = Blueprint('views', __name__)

@bp.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user) # render home.html template

@bp.route('/login', methods=['GET', 'POST'])
def spotifyLogin():
    if request.method == 'POST':
        sp_oauth = create_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
        if login_successful:
            # Redirect to another page with a success message
            flash('You were successfully logged in')
            return redirect(url_for('profile'))
        else:
            # Redirect back to the login page with an error message
            flash('Login failed. Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@bp.route('/redirect')
def redirectPage():
    token_info = spotify_redirect()
    session["token_info"] = token_info
    return redirect(url_for("getTracks"))

@bp.route('/profile')
def profile():
    if 'spotify_token' in session:
        headers = {
            'Authorization': f'Bearer {session["spotify_token"]}'
        }
        response = requests.get('https://api.spotify.com/v1/me/top/tracks?limit=10', headers=headers)
        top_tracks = response.json().get('items', [])
        return render_template('profile.html', top_tracks=top_tracks)
    else:
        return redirect(url_for('auth.login'))

# saves the playlist 
@bp.route('/save_playlist', methods=['POST'])
@login_required
def save_playlist():
    if 'token_info' in session:
        token_info = session['token_info']
        # Check if token has expired and refresh if necessary
        if time.time() - token_info['expires_at'] > 0:
            token_info = refresh_spotify_token()
            session['token_info'] = token_info  # Make sure to update the session

        # Now you have an updated token, use it to fetch top tracks
        headers = {
            'Authorization': f"Bearer {token_info['access_token']}"
        }
        response = requests.get('https://api.spotify.com/v1/me/top/tracks?limit=10', headers=headers)
        if response.status_code == 200:
            top_tracks = response.json()['items']
            # Here you can now extract the track URIs and proceed to create a playlist
            # ...

            user_id = session.get('spotify_user_id')
            token = token_info['access_token']
            playlist_id = create_playlist(user_id, token)
            track_uris = [track['uri'] for track in top_tracks]
            add_tracks_to_playlist(playlist_id, track_uris, token)

            # Redirect to some confirmation page or back to profile
            flash('Playlist saved successfully!', category='success')
            return redirect(url_for('.profile'))
        else:
            flash('Failed to fetch top tracks from Spotify.', category='error')
            return redirect(url_for('.profile'))
    else:
        flash('You need to be signed in with Spotify.', category='error')
        return redirect(url_for('.spotifyLogin'))


@bp.route('/getTracks')
@login_required
def getTracks():
    if 'token_info' in session:
        token_info = session['token_info']
        if time.time() - token_info['expires_at'] > 0:
            # Token has expired, refresh it
            token_info = refresh_spotify_token()

        headers = {
            'Authorization': f"Bearer {token_info['access_token']}"
        }
        response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
        if response.status_code == 200:
            top_tracks = response.json()['items']
            return render_template('tracks.html', top_tracks=top_tracks)  # Render your tracks template
        else:
            flash('Failed to fetch top tracks from Spotify.', category='error')
            return redirect(url_for('.home'))
    else:
        flash('Spotify authorization needed.', category='error')
        return redirect(url_for('.spotifyLogin'))