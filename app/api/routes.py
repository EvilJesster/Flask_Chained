from flask import Blueprint, request, flash
from flask_login import login_required, current_user
from app.models import db, Sudoku, SudokuSaveState
from json import dumps
import time

api = Blueprint('api', __name__)

@api.route('/check_answer/<uuid>/<answer>')
@login_required
def check_answer(uuid, answer):
    to_check = Sudoku.query.filter_by(uuid=uuid).first()

    if to_check is None:
        return dumps(False)


    is_correct = (to_check.solved_str == answer)

    if is_correct:
        # find the association
        assoc = SudokuSaveState.query.filter_by(user_id=current_user.id, sudoku_id=to_check.id).first()

        if assoc.time_end is None:
            assoc.time_end = int(time.time())
            flash('Congrats! You completed this %s difficulty puzzle in %d seconds!' % (to_check.difficulty, assoc.time_end - assoc.time_start), 'success')
            db.session.commit()

#        assoc.time_end = time.time()
    
    
    return dumps(is_correct)

@api.route('/save_state/<uuid>', methods=['POST'])
@login_required
def save_state(uuid):
    sss = SudokuSaveState.query.filter_by(user_id = current_user.id).all();

    ss = None

    for i in sss:
        if i.board.uuid == uuid:
            ss = i
            break

    numbers = request.form.get('numbers')
    pencilmarks = request.form.get('pencilmarks')

    ss.number_str = numbers
    ss.pencilmark_str = pencilmarks

    db.session.commit()

    return ''
