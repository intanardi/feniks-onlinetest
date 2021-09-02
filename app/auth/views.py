from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db, csrf
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    if request.method == 'POST':
        print(request.form['username'])
        user = User.query.filter_by(username = request.form['username']).first()
        if user is None or not user.check_password(request.form['password']):
            flash("Invalid username or pasword")
            return redirect(url_for('auth.login'))
        login_user(user)
        if user.role.name.lower() == 'candidate':
            # return redirect(url_for('exam.index'))
            return redirect(url_for('candidate.index'))
        return redirect(url_for('admin.index'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
