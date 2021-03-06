from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from sudoku.generator import gen_sudoku, EASY, MEDIUM, HARD, INSANE, DEMO
from app.models import Sudoku, SudokuSaveState, db
import threading
import time
from uuid import uuid4
from urllib.request import urlopen
import json
import time
from datetime import datetime

user = Blueprint('user', __name__)

# user home
@user.route('/home')
@login_required
def home():

    in_progress = []
    completed = []

    for i in current_user.boards:
        if i.time_end is None:
            in_progress.append((datetime.fromtimestamp(i.time_start), i.board.difficulty, i.board.uuid))
        else:
            completed.append((i.board.difficulty, i.time_end - i.time_start, i.board.uuid))

    return render_template('user/home.html', in_progress=in_progress, completed=completed)

# leaderbaord
@user.route('/leaderboard')
@login_required
def leaderboard():

    return render_template('user/leaderboard.html')

@user.route('/leaderboard/<diff>')
@login_required
def leaderboardDisplay(diff):

    #grab all the games
    games = SudokuSaveState.query.all()
    #need completed games information
    completed = []


    for i in games:
        #if completed and matching the requested difficulty, add to list
        if i.time_end != None and i.board.difficulty == diff.upper():
            completed.append((i.user.username, i.time_end - i.time_start, i.board.uuid))

    #sort list by time taken
    completed.sort(key=lambda game: game[1])

    return render_template('user/leaderboard.html', diff = diff.capitalize(), completed = completed)

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

        n = Sudoku(uuid, solved_str, unsolved_str, diff.upper())
        db.session.add(n)
        db.session.commit()


# route for creating a new puzzle
@user.route('/new-sudoku/<diff>')
@login_required
def new_puzzle(diff):

    # ensure that difficulty is right
    if not diff.capitalize() in [EASY, MEDIUM, HARD, INSANE, DEMO]:
        return 'no'

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
        # generate a random fact so they don't get bored
        u = urlopen("https://uselessfacts.jsph.pl/random.json?language=en")
        get = u.read()
        info = json.loads(get)
        random_fact=info['text']

        return render_template('user/puzzle_loading.html', random_fact=random_fact)


    # create a new state if needed
    save_state = SudokuSaveState.query.filter_by(user_id=current_user.id, sudoku_id=to_show.id).first()
    if save_state is None:
            new_state = SudokuSaveState(current_user, to_show)
            db.session.add(new_state)
            db.session.commit()
            save_state = new_state


    return render_template('user/view_puzzle.html', sudoku=to_show, state=save_state, time=int(time.time()))
