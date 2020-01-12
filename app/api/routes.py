from flask import Blueprint
from flask_login import login_required
from app.models import Sudoku
from json import dumps

api = Blueprint('api', __name__)

@api.route('/check_answer/<uuid>/<answer>')
@login_required
def check_answer(uuid, answer):
    to_check = Sudoku.query.filter_by(uuid=uuid).first()

    if to_check is None:
        return dumps(False)
    
    return dumps((to_check.solved_str == answer))

