from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app
from flask_login import login_required, login_user, logout_user, current_user
from . import candidate
from .forms import CandidateForm, LoginForm
from .. import db, csrf
from ..models import *
import json

ROWS_PER_PAGE = 3
@login_required
@candidate.route('/', methods=['GET', 'POST'])
@candidate.route('/index', methods=['GET', 'POST'])
@candidate.route('/home', methods=['GET', 'POST'])
@csrf.exempt
def index():
    return render_template('candidate/index.html')
    
@login_required
@candidate.route('/add', methods=['GET', 'POST'])
@csrf.exempt
def add():
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.home'))
    divisions = Division.query.all()
    levels = Level.query.all()
    if request.method == 'POST':
        print("submitted")
        candidate = User()
        if request.form['password'] != request.form['repassword']:
            flash("Confirmation password sshould be a same")
            return redirect(url_for('candidate.add'))
        candidate.username = request.form['username']
        candidate.email = request.form['email']  
        candidate.fullname = request.form['fullname']
        candidate.phone = request.form['phone'] 
        candidate.address = request.form['address'] 
        candidate.division_id = request.form['division'] 
        candidate.level_id = request.form['level']
        candidate.set_password(request.form['password'] )
        db.session.add(candidate)
        db.session.commit()
        return redirect(url_for('candidate.index'))
        
    return render_template('admin/candidate/add.html', divisions=divisions, levels=levels)

@login_required
@candidate.route('/edit/<id>', methods=['GET', 'POST'])
@csrf.exempt
def edit(id):
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.home'))
    divisions = Division.query.all()
    levels = Level.query.all()
    candidate = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        candidate.username = request.form['username']
        candidate.email = request.form['email']  
        candidate.fullname = request.form['fullname']
        candidate.phone = request.form['phone'] 
        candidate.address = request.form['address']
        candidate.division_id = request.form['division'] 
        candidate.level_id = request.form['level']
        db.session.add(candidate)
        db.session.commit()
        return redirect(url_for('candidate.index'))
    return render_template('admin/candidate/edit.html', candidate=candidate, divisions=divisions, levels=levels)

@login_required
@candidate.route('/delete/<id>', methods=['GET', 'POST'])
@csrf.exempt
def delete(id):
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.home'))
    candidate = User.query.filter_by(id=id).first()
    candidate.status = False
    db.session.add(candidate)
    db.session.commit()
    return redirect(url_for('user.index'))