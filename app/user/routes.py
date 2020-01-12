from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required
from sudoku.generator import gen_sudoku, EASY, MEDIUM, HARD, INSANE
from app.models import Sudoku, db
import threading
import time
from uuid import uuid4

user = Blueprint('user', __name__)

# user home
@user.route('/home')
@login_required
def home():

    return render_template('user/home.html')

# test route for sudoku board demo
@user.route('/sudoku_test')
@login_required
def sudoku_test():

    return render_template('user/sudoku_test.html')


# callback for making new puzzle since taking puzzles takes time yknow
def new_puzzle_callback(diff, uuid):
    unsolved, solved = gen_sudoku(diff.capitalize())

    unsolved_str = ''.join(map(str, unsolved))
    solved_str = ''.join(map(str, solved))


    # very legit code right here
    from app import app

    with app.app_context():

        n = Sudoku(uuid, solved_str, unsolved_str)
        db.session.add(n)
        db.session.commit()


# route for creating a new puzzle
@user.route('/new-sudoku/<diff>')
@login_required
def new_puzzle(diff):

    # ensure that difficulty is right
    if not diff.capitalize() in [EASY, MEDIUM, HARD, INSANE]:
        return ''

    # generate a unique ID so we can refer to this puzzle
    uuid = str(uuid4())
    
    # spawn a task to make a new puzzle
    # this way, it can take a long ish time for the task to generate
    thr = threading.Thread(target=new_puzzle_callback, args=(diff.capitalize(), uuid))
    thr.start()
    

    
    return redirect(url_for('user.view_puzzle', uuid=uuid))

# solve a puzzle
@user.route('/puzzle/<uuid>')
@login_required
def view_puzzle(uuid):
    # we want to see if our puzzle exists
    to_show = Sudoku.query.filter_by(uuid=uuid).first()

    if to_show is None:
        # no puzzle yet, let's give the user the loading page
        # generate a random fact so the don't get bored
        # HONGWEI this is ur job!

        random_fact='(Rnadom Fcat)'
        
        return render_template('user/puzzle_loading.html', random_fact=random_fact)

    # puzzle exists
    # in the future, create a save state
    # for now, just display the puzzle
    
    return render_template('user/view_puzzle.html', sudoku=to_show)
