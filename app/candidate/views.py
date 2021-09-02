from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app
from flask_login import login_required, login_user, logout_user, current_user
from . import candidate
from .forms import CandidateForm, LoginForm
from .. import db, csrf
from ..models import *
import json
from datetime import datetime

# current_time = now.strftime("%H:%M:%S")

title = "Feniks CBT"

@login_required
@candidate.route('/', methods=['GET', 'POST'])
@candidate.route('/index', methods=['GET', 'POST'])
@candidate.route('/home', methods=['GET', 'POST'])
@csrf.exempt
def index():
    return render_template('candidate/index.html', title=title)

@login_required
@candidate.route('/test', methods=['GET', 'POST'])
@csrf.exempt
def test():
    message = None
    status = None
    time = datetime.now()
    print("current time :")
    print()
    _date = time.strftime("%Y-%m-%d %H:%M:%S")
    _time = time.strftime("%H:%M:%S")
    date = datetime.strptime(_date, '%Y-%m-%d %H:%M:%S')
    print(_date)
    print(type(_date))
    print("***")
    print(date)
    print(type(date))
    print("--------------")
    print()
    print("schedule time :")
    print()
    schedule = Candidate_Schedule_Test.query.filter_by(candidate_id=current_user.id).first()
    print(schedule)
    print("schedule ada di atas")
    cand_date = ""
    if schedule is not None:
        _date_db = schedule.date_test.strftime("%Y-%m-%d %H:%M:%S")
        # _time_db = schedule.date_test.strftime("%H:%M:%S")
        date_db = datetime.strptime(_date_db, '%Y-%m-%d %H:%M:%S')
        cand_date = schedule.date_test.strftime("%Y %m %d %H:%M:%S")
        print()
        print()
        print("perbandingan :")
        print("dari DB tanggal :")
        print(date_db.date())
        print("dari DB jam :")
        print(date_db.time())
        print("hari dibuka tanggal")
        print(date.date())
        print("hari dibuka jam")
        print(date.time())
        if date_db.date() == date.date():
            if date.time() >= date_db.time():
                message = "Anda sudah masuk waktu pengerjaan"
                status = 00
            elif date.time() < date_db.time():
                message = "Waktu pengerjaan belum dimulai. dimulai pukul : "+ str(date_db.time())
                status = 10
        elif date_db.date() > date.date():
            message = "Anda belum bisa mengikuti tes. Tanggal pengerjaan anda adalah "+ str(date_db.date().strftime('%D %M %Y')) +" pukul : "+ str(date_db.time())
            status = 20
        else:
            message = "Maaf schedule anda sudah lewat waktu. anda tidak bisa untuk mengikuti tes"
            status = 50
    else:
        message = "Anda belum memiliki schedule test"
        status = 30
    return render_template('candidate/test.html', title=title, schedule=schedule, cand_date=cand_date, current_time=time, message=message, status=status)