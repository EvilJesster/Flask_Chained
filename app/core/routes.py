from flask import Blueprint, render_template

# the core blueprint
# contains core routes
core = Blueprint('core', __name__)

@core.route('/')
@core.route('/index')
def index():
    return render_template('core/index.html')
