from flask import Blueprint, render_template, flash, redirect, url_for, session
from app.auth.forms import SignUpForm, LogInForm
from app.models import db, User
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        to_validate = User.query.filter_by(username=form.username.data).first()

        if to_validate is None or to_validate.password != form.password.data:
            flash('Incorrect Username or Password', 'danger')
        else:
            # log in user
            login_user(to_validate)

            flash('Logged In Successfully!', 'success')
            
            if 'next' in session:
                return redirect(session['next'])

            return redirect(url_for('user.home'))
        
    
    return render_template('auth/login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignUpForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is not None:
            flash('This Username is Taken!', 'danger')
        else:
            new_account = User(form.username.data, form.email.data, form.password.data)
            db.session.add(new_account)
            db.session.commit()

            flash('Account Created! Log In Below:', 'success')

            return redirect(url_for('auth.login'))
        
    
    return render_template('auth/signup.html',
                           form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('core.index'))
