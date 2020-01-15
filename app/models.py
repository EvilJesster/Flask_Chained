from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import time

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    boards = db.relationship('SudokuSaveState', back_populates='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Sudoku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unsolved_str = db.Column(db.String(81), nullable=True)
    solved_str = db.Column(db.String(81), nullable=True)
    uuid = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(180), nullable=True)

    save_states = db.relationship('SudokuSaveState', back_populates='board')

    def __init__(self, uuid, solve, unsolve, diff):
        self.uuid = uuid
        self.solved_str = solve
        self.unsolved_str = unsolve
        self.difficulty = diff

# save state
# actually an association table



class SudokuSaveState(db.Model):
    # columns
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    sudoku_id = db.Column(db.Integer, db.ForeignKey('sudoku.id'), primary_key=True)
    number_str = db.Column(db.String(81), nullable=False, default='_'*81)
    pencilmark_str = db.Column(db.String(729), nullable=False, default='_'*791)
    time_start = db.Column(db.Integer, nullable=False, default=lambda: int(time.time()))
    time_end = db.Column(db.Integer, nullable=True, default=None)

    user = db.relationship(User, back_populates='boards')
    board = db.relationship(Sudoku, back_populates='save_states')


    def __init__(self, user, sudoku):
        self.user_id = user.id
        self.sudoku_id = sudoku.id
    

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable = False)
    game = db.Column(db.String(100), nullable = False)
    time = db.Column(db.Float, nullable = False)
    difficulty = db.Column(db.String(20), nullable = False)

    def __init__(self, username, game, time, difficulty):
        self.username = username
        self.game = game
        self.time = time
        self.difficulty = difficulty
