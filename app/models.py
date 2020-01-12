from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Sudoku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unsolved_str = db.Column(db.String(81), nullable=True)
    solved_str = db.Column(db.String(81), nullable=True)
    uuid = db.Column(db.String(100), nullable=False)

    def __init__(self, uuid, solve, unsolve):
        self.uuid = uuid
        self.solved_str = solve
        self.unsolved_str = unsolve
    
    @property
    def is_active():
        return (unsolved_str is not None and solve_str is not None)
