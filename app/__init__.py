from flask import Flask, render_template
from flask_login import LoginManager
from app.core.routes import core as core_blueprint
from app.auth.routes import auth as auth_blueprint
from app.user.routes import user as user_blueprint
from app.api.routes import api as api_blueprint
from app.models import db, User
from app.config import *


# initialize app, and app configurations
app = Flask(__name__)

app.secret_key = (SECRET_KEY_FAKE if not DEBUG else SECRET_KEY_REAL)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['USE_SESSION_FOR_NEXT'] = USE_SESSION_FOR_NEXT

# initialize database, and create tables
db.init_app(app)

with app.app_context():
    db.create_all()


# initialize login manager, and set it up
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'



# register blueprints
app.register_blueprint(core_blueprint, url_prefix='/')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(api_blueprint, url_prefix='/api')
