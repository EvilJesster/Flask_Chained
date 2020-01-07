from flask import Blueprint, render_template
from flask_login import login_required

user = Blueprint('user', __name__)

@user.route('/home')
@login_required
def home():

    return render_template('user/home.html')
