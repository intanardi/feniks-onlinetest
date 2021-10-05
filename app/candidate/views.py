from flask import render_template, session, redirect, url_for, flash, request, current_app
from flask_login import login_required, login_user, logout_user, current_user
from . import candidate
from .forms import CandidateForm, LoginForm
from .. import db, csrf
from ..utils import convert_in_hours, convert_in_minutes, format_duration
from ..models import *
import json
from datetime import datetime, date, time, timedelta
# current_time = now.strftime("%H:%M:%S")

title = "Feniks CBT"
directory = "/static/uploads/test/"

def check_login_allowed():
    if current_user.is_authenticated:
        schedule = Candidate_Schedule_Test.query.filter_by(candidate_id=current_user.id).first()
        if schedule is None:
            return False
        else :
            today = datetime.now()
            today_datetime = today.strftime("%Y-%m-%d %H:%M:%S")
            today_datetime_fix = datetime.strptime(today_datetime, '%Y-%m-%d %H:%M:%S')
            date_from_db = schedule.date_test.strftime("%Y-%m-%d %H:%M:%S")
            date_from_db_fix = datetime.strptime(date_from_db, '%Y-%m-%d %H:%M:%S')
            gs = Global_Setting.query.filter_by(setting_code=1).first()
            login_expired = date_from_db_fix + timedelta(hours=int(gs.variable))
            if today.date() == date_from_db_fix.date():
                if today_datetime_fix >= login_expired:
                    return False
            else:
                return False
        return True
    else :
        return redirect(url_for('auth.login'))

@candidate.route('/', methods=['GET', 'POST'])
@candidate.route('/index', methods=['GET', 'POST'])
@candidate.route('/home', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def index():
    return render_template('candidate/index.html', title=title)

@candidate.route('/quiz', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def quiz():
    status = check_login_allowed()
    print(status)
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    message = None
    status = None
    time = datetime.now()
    _date = time.strftime("%Y-%m-%d %H:%M:%S")
    _time = time.strftime("%H:%M:%S")
    date = datetime.strptime(_date, '%Y-%m-%d %H:%M:%S')
    schedule = Candidate_Schedule_Test.query.filter_by(candidate_id=current_user.id).first()
    cand_date = ""
    if schedule is not None:
        _date_db = schedule.date_test.strftime("%Y-%m-%d %H:%M:%S")
        # _time_db = schedule.date_test.strftime("%H:%M:%S")
        date_db = datetime.strptime(_date_db, '%Y-%m-%d %H:%M:%S')
        cand_date = schedule.date_test.strftime("%Y %m %d %H:%M:%S")
        if date_db.date() == date.date():
            if date.time() >= date_db.time():
                message = "Anda sudah masuk waktu pengerjaan. Silahkan klik mulai Test untuk masuk ke tes"
                status = 00
            elif date.time() < date_db.time():
                message = "Jadwal tes anda adalah hari ini. dimulai pukul : "+ str(date_db.time())
                status = 10
        elif date_db.date() > date.date():
            message = "Tanggal pengerjaan anda adalah "+ str(date_db.date().strftime('%D %M %Y')) +" pukul : "+ str(date_db.time())
            status = 20
        else:
            message = "Maaf schedule anda sudah lewat waktu. anda tidak bisa untuk mengikuti tes"
            status = 50
    else:
        message = "Anda belum memiliki schedule test"
        status = 30
    return render_template('candidate/quiz.html', title=title, schedule=schedule, cand_date=cand_date, current_time=time, message=message, status=status)

@candidate.route('/test', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def test():
    status = check_login_allowed()
    print(status)
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    message = None
    status = None
    time = datetime.now()
    _date = time.strftime("%Y-%m-%d %H:%M:%S")
    _time = time.strftime("%H:%M:%S")
    date = datetime.strptime(_date, '%Y-%m-%d %H:%M:%S')
    schedule = Candidate_Schedule_Test.query.filter_by(candidate_id=current_user.id).first()
    cand_date = ""
    check_Candidate_Psikotest_Schedule = Candidate_Psikotest_Schedule.query.filter_by(candidate_id=current_user.id).first()
    today = datetime.now()
    if check_Candidate_Psikotest_Schedule is not None :
        return redirect(url_for('candidate.candidate_psikotest'))
    else :
        if schedule is not None:
            _date_db = schedule.date_test.strftime("%Y-%m-%d %H:%M:%S")
            # _time_db = schedule.date_test.strftime("%H:%M:%S")
            date_db = datetime.strptime(_date_db, '%Y-%m-%d %H:%M:%S')
            cand_date = schedule.date_test.strftime("%Y %m %d %H:%M:%S")
            print("track")
            print(date_db)
            print(cand_date)
            if date_db.date() == date.date():
                if date.time() >= date_db.time():
                    message = "Anda sudah masuk waktu pengerjaan. Silahkan klik mulai Test untuk masuk ke tes"
                    status = 00
                elif date.time() < date_db.time():
                    message = "Jadwal tes anda adalah hari ini. dimulai pukul : "+ str(date_db.time())
                    status = 10
            elif date_db.date() > date.date():
                message = "Tanggal pengerjaan anda adalah "+ str(date_db.date().strftime('%D %M %Y')) +" pukul : "+ str(date_db.time())
                status = 20
            else:
                message = "Maaf schedule anda sudah lewat waktu. anda tidak bisa untuk mengikuti tes"
                status = 50
        else:
            message = "Anda belum memiliki schedule test"
            status = 30
            # return redirect('auth.logout')
        return render_template('candidate/test.html', title=title, schedule=schedule, cand_date=cand_date, current_time=time, message=message, status=status)

@candidate.route('/psikotest/quiz', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def candidate_psikotest():
    # check login expired
    status = check_login_allowed()
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    today = datetime.now()
    today_datetime = today.strftime("%Y-%m-%d %H:%M:%S")
    today_datetime_fix = datetime.strptime(today_datetime, '%Y-%m-%d %H:%M:%S')
    # check if flag is false then psikotest not done yet
    check_psikotest = Candidate_Psikotest_Schedule.query.filter_by(candidate_id=current_user.id, flag=False).first()
    # print(check_psikotest)
    if check_psikotest is not None:
        status = check_psikotest.status
        flag = check_psikotest.flag
        psikotest = Psikotest.query.filter_by(id=check_psikotest.psikotest_id).first()
        psikotest_type = Psikotest_Type.query.filter_by(id=psikotest.psikotest_type_id).first()
        psikotest_name = psikotest_type.name
        datetime_duration = 0
        # Convert datetime object to string in specific format 
        if status :
            print("duration : ")
            print(psikotest.timedelta_duration)
            given_time = check_psikotest.started_time
            datetime_duration = given_time + timedelta(minutes=psikotest.timedelta_duration)
            print(datetime_duration)
            pdf = psikotest.test_filename
        else :
            pdf = psikotest.instruction_filename
        alert = psikotest.alert
        source_file = directory + pdf
        # if sattus is False instruction will appear, if True psikotest exam will apppear
        # once intrcution pressed "understand update the flag to True"
        return render_template('candidate/psikotest_exam.html', title=title, status=status, source_file=source_file, flag=flag, alert=alert, target_candidate_id=check_psikotest.id, psikotest=psikotest, check_psikotest=check_psikotest, datetime_duration=datetime_duration)
    else :
        flash("Psikotest Telah Berahir")
        return redirect(url_for("candidate.main_test_preview"))
    

@candidate.route('/psikotest/save_test_detail', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def save_test_detail():
    status = check_login_allowed()
    print(status)
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    psikotest_type_list = []
    psikotest_list = []
    psikotest_type = Psikotest_Type.query.all()
    check_Candidate_Psikotest_Schedule = Candidate_Psikotest_Schedule.query.filter_by(candidate_id=current_user.id, is_deleted=False).first()
    if check_Candidate_Psikotest_Schedule is None :
        for a in psikotest_type :
            print(a.id)
            psikotest = Psikotest.query.filter_by(psikotest_type_id=a.id, is_deleted=False).all()
            for b in psikotest :
                ct = Candidate_Psikotest_Schedule()
                ct.candidate_id = current_user.id
                ct.psikotest_id = b.id
                db.session.add(ct)
                db.session.commit()
                # psikotest_list.append(b.id)
        cur_candidate = User.query.filter_by(id=current_user.id).first()
        print(cur_candidate)
        examination = Examination.query.filter_by(division_id=cur_candidate.division_id, level_id=cur_candidate.level_id).first()
        exam_detail = Examination_Detail.query.filter_by(examination_id=examination.id).all()
        for c in exam_detail:
            print(c.id)
        print(psikotest_list)
    return redirect(url_for('candidate.candidate_psikotest'))

@candidate.route('/psikotest/update_status_psikotest/<id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def update_status_psikotest(id):
    status = check_login_allowed()
    print(status)
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    response = {}
    psikotest = Candidate_Psikotest_Schedule.query.filter_by(id=id).first()
    psikotest.status = True
    psikotest.started_time = datetime.now()
    db.session.add(psikotest)
    db.session.commit()
    response = "quiz"
    return response

@candidate.route('/psikotest/update_flag_psikotest/<id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def update_flag_psikotest(id):
    status = check_login_allowed()
    print(status)
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    response = {}
    psikotest = Candidate_Psikotest_Schedule.query.filter_by(id=id).first()
    psikotest.flag = True
    db.session.add(psikotest)
    db.session.commit()
    response = "quiz"
    return redirect(url_for('candidate.candidate_psikotest'))

@candidate.route('/main/test/preview', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def main_test_preview():
    status = check_login_allowed()
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    user = User.query.filter_by(id=current_user.id).first()
    examination = Examination.query.filter_by(level_id=user.level_id, division_id=user.division_id).first()
    get_all_test = Examination_Detail.query.filter_by(examination_id=examination.id).all()
    check_main_test = Candidate_Main_Schedule.query.filter_by(candidate_id=current_user.id).first()
    msg_status = False
    if check_main_test is not None:
        return redirect(url_for('candidate.main_test'))
    if request.method == 'POST':
        for i in get_all_test :
            main_test = Candidate_Main_Schedule()
            main_test.candidate_id = current_user.id
            main_test.division_test_id = i.id
            db.session.add(main_test)
            db.session.commit()
        return redirect(url_for('candidate.main_test'))
    return render_template('candidate/main_test.html', title=title, user=user, msg_status=msg_status, check_main_test=check_main_test)

@candidate.route('/main/test', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def main_test():
    status = check_login_allowed()
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    msg_status = True
    user = User.query.filter_by(id=current_user.id).first()
    check_main_test = Candidate_Main_Schedule.query.filter_by(candidate_id=current_user.id, flag=False).first()
    datetime_duration = 0
    check_psikotest = Candidate_Psikotest_Schedule.query.filter_by(candidate_id=current_user.id, flag=False).first()
    # print(check_psikotest)
    if check_psikotest is not None:
        return redirect(url_for('candidate.candidate_psikotest'))
    if check_main_test is None:
        return redirect(url_for('candidate.candidate_test_done'))
    print(check_main_test.division_test_id)
    print('0000')
    examination_test = Examination_Detail.query.filter_by(id=check_main_test.division_test_id).first()
    if examination_test is None:
        flash("Soal tidak ditemukan! silahkan informasikan kepada pihak Phoenix")
        return render_template('500.html')
    given_time = check_main_test.started_time
    source_file = directory + examination_test.filename
    flag= check_main_test.flag
    status = check_main_test.status
    if status :
        print(examination_test)
        print(given_time)
        datetime_duration = given_time + timedelta(minutes=examination_test.timedelta_duration)
    return render_template('candidate/main_test.html', title=title, user=user, source_file=source_file, flag=flag, status=status, msg_status=msg_status,datetime_duration=datetime_duration, check_main_test=check_main_test, examination_test=examination_test)

@candidate.route('/main/test/save_main_test_detail', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def save_main_test_detail():
    status = check_login_allowed()
    print(status)
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    examination = Examination.query.filter_by(division_id=current_user.division_id, level_id=current_user.level_id).all()
    
    check_main_Schedule = Candidate_Main_Schedule.query.filter_by(candidate_id=current_user.id, is_deleted=False).first()
    if check_main_Schedule is None :
        for a in examination :
            examination_test = Examination_Detail.query.filter_by(examination_id=a.id, is_deleted=False).all()
            for b in examination_test :
                cm = Candidate_Main_Schedule()
                cm.candidate_id = current_user.id
                cm.division_test_id = b.id
                db.session.add(cm)
                db.session.commit()
    return redirect(url_for('candidate.main_test'))

@candidate.route('/main/update_status_main_test/<id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def update_status_main_test(id):
    status = check_login_allowed()
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    main_test = Candidate_Main_Schedule.query.filter_by(id=id).first()
    main_test.status = True
    main_test.started_time = datetime.now()
    db.session.add(main_test)
    db.session.commit()
    return redirect(url_for('candidate.main_test'))

@candidate.route('/main/update_flag_main_test/<id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def update_flag_main_test(id):
    status = check_login_allowed()
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    main_test = Candidate_Main_Schedule.query.filter_by(id=id).first()
    main_test.flag = True
    db.session.add(main_test)
    db.session.commit()
    return redirect(url_for('candidate.main_test'))

@candidate.route('/main/test/done', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def candidate_test_done():
    status = check_login_allowed()
    print(status)
    if status == False:
        flash("Waktu izin login habis")
        return redirect(url_for('auth.logout'))
    return render_template('candidate/test_done.html')