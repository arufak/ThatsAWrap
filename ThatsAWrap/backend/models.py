# store database models

from . import db 
from sqlalchemy.sql import func

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    spotifyToken = db.Column(db.String(150), unique=True)
    spotifyTokenExpiration = db.Column(db.String(150), unique=False)
    spotifyRefreshToken = db.Column(db.String(150), unique=False)
    playlistInfo = db.Column(db.String(150), unique=False)
