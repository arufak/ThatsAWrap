from backend import views
from flask import Flask 
from flask_login import LoginManager, UserMixin 
from backend.auth import get_user_by_id

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "secretkeyyyy"
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

app.register_blueprint(views.bp)

if __name__ == '__main__': 
    app.run(debug=True)

