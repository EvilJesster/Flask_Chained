from flask import Blueprint
from flask_login import login_required, current_user
from app.models import db, Sudoku, SudokuSaveState
from json import dumps

api = Blueprint('api', __name__)

@api.route('/check_answer/<uuid>/<answer>')
@login_required
def check_answer(uuid, answer):
    to_check = Sudoku.query.filter_by(uuid=uuid).first()

    if to_check is None:
        return dumps(False)
    
    return dumps((to_check.solved_str == answer))

@api.route('/save_state/<uuid>/<numbers>/<pencilmarks>')
@login_required
def save_state(uuid, numbers, pencilmarks):
    sss = SudokuSaveState.query.filter_by(user_id = current_user.id).all();

    ss = None

    for i in sss:
        if i.board.uuid == uuid:
            ss = i
            break

    ss.number_str = numbers
    ss.pencilmark_str = pencilmarks

    db.session.commit()

    return ''
