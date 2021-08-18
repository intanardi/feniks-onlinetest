from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app, Flask, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from . import admin
from .. import db, csrf
from ..models import *
import json
import os
from os.path import join, dirname, realpath

apps = Flask(__name__)
apps.config['UPLOAD_PATH'] = 'app/static/uploads/test'

# UPLOADS_TEST_PATH = join(dirname(realpath(__file__)), 'static/upload/')

ROWS_PER_PAGE = 5
ADMIN_PERMISSION_LIST = [1,2]
UPLOAD_FOLDER = '/static/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/open_pdf/<filename>')
def open_pdf(filename):
    print("heree")
    print("----")
    print(filename)
    # directory = "/static/pdf/psikotest/soal_cfit.pdf"
    directory = "/static/uploads/test/" + filename
    print(directory)
    return render_template('admin/master_test/preview.html', directory=directory)

@admin.route('/')
@admin.route('/index')
@csrf.exempt
@login_required
def index():
    return render_template('admin/index.html')
"""
    =================================================
                    USER ADMIN MODULE
    =================================================
"""

@admin.route('/data', methods=['POST', 'GET'])
@csrf.exempt
@login_required
def data():
    _keyword = ""
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    if request.method == "POST":
        _keyword= request.form['keyword']
    _search = "%{}%".format(_keyword)
    page = request.args.get('page', 1, type=int)
    total_rows = User.query.filter(User.role_id.in_(ADMIN_PERMISSION_LIST),User.fullname.like(_search) ,User.status.is_(True)).count()
    boxsize = ROWS_PER_PAGE
    num_pages = -(total_rows // -boxsize)
    users = User.query.filter(User.role_id.in_(ADMIN_PERMISSION_LIST),User.fullname.like(_search) ,User.status.is_(True)).order_by(User.id).paginate(page=page, per_page=ROWS_PER_PAGE)
    next_url = url_for('admin.data', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('admin.data', page=users.prev_num) \
        if users.has_prev else None
    return render_template('admin/admin/index.html', users=users.items, prev_url=prev_url, next_url=next_url, num_pages=int(num_pages))

@admin.route('/add', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def add():
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    if current_user.role_id != 1:
        flash("You have no permision!")
        return redirect(url_for('user.index'))
    roles = Role.query.all()
    divisions = Division.query.all()
    levels = Level.query.all()
    if request.method == 'POST':
        print(request.form)
        user = User()
        user.role_id = int(request.form['roles'])
        user.division_id = int(request.form['division'])
        user.level_id = int(request.form['level'])
        user.username = request.form['username']
        user.email = request.form['email']  
        user.fullname = request.form['fullname']
        user.phone = request.form['phone'] 
        user.address = request.form['address']
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.data'))
        
    return render_template('admin/admin/add.html', roles=roles, divisions=divisions, levels=levels)

@login_required
@admin.route('/edit/<id>', methods=['GET', 'POST'])
@csrf.exempt
def edit(id):
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    if current_user.role_id != 1:
        flash("You have no permision!")
        return redirect(url_for('admin.index'))
    user = User.query.filter_by(id=id).first()
    roles = Role.query.all()
    divisions = Division.query.all()
    levels = Level.query.all()
    if request.method == 'POST':
        print(request.form)
        if  'roles' in request.form:
            user.role_id = int(request.form['roles'])
        if  'division' in request.form:
            user.division_id = int(request.form['division'])
        if  'level' in request.form:
            user.level_id = int(request.form['level'])
        user.username = request.form['username']
        user.email = request.form['email']  
        user.fullname = request.form['fullname']
        user.phone = request.form['phone'] 
        user.address = request.form['address'] 
        # user.role_id = int(request.form['roles'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.data'))
    return render_template('admin/admin/edit.html', user=user, roles=roles, divisions=divisions, levels=levels)

@login_required
@admin.route('/delete/<id>', methods=['GET', 'POST'])
@csrf.exempt
def delete(id):
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    if current_user.role_id != 1:
        flash("You have no permision!")
        return redirect(url_for('user.index'))
    user = User.query.filter_by(id=id).first()
    user.status = False
    db.session.add(user)
    # db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.data'))

"""
    =====================================================
                    END OF USER ADMIN MODULE
    =====================================================
"""

"""
    =====================================================
                    USER CANDIDATE MODULE
    =====================================================
"""


@login_required
@admin.route('/candidate/data', methods=['GET', 'POST'])
@csrf.exempt
def candidate_data():
    _keyword = ""
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.home'))
    if request.method == "POST":
        _keyword= request.form['keyword']
    _search = "%{}%".format(_keyword)
    page = request.args.get('page', 1, type=int)
    total_rows = User.query.filter(User.role_id.in_(["3"]), User.status.is_(True), User.fullname.like(_search)).count()
    boxsize = ROWS_PER_PAGE
    num_pages = -(total_rows // -boxsize)
    candidates = db.session.query(User.id, User.fullname.label('name'), User.email, User.phone, Level.name.label('level'), Division.name.label('division'), Candidate_Schedule_Test.date_test.label('schedule')).join(Level, Division, Candidate_Schedule_Test, isouter=True).filter(User.role_id.in_(["3"]), User.status.is_(True), User.fullname.like(_search)).order_by(User.id).paginate(page=page, per_page=ROWS_PER_PAGE)
    # print(candidates.items)
    # candidates = User.query.filter(User.role_id.in_(["3"]), User.status.is_(True), User.fullname.like(_search)).paginate(page=page, per_page=ROWS_PER_PAGE)
    candidate_schedule = Candidate_Schedule_Test.query.all()
    next_url = url_for('admin.candidate_data', page=candidates.next_num) \
        if candidates.has_next else None
    prev_url = url_for('admin.candidate_data', page=candidates.prev_num) \
        if candidates.has_prev else None
    return render_template('admin/candidate/index.html', candidates=candidates.items, prev_url=prev_url, next_url=next_url, num_pages=int(num_pages), candidate_schedule=candidate_schedule)
    
@login_required
@admin.route('/candidate/add', methods=['GET', 'POST'])
@csrf.exempt
def candidate_add():
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.home'))
    divisions = Division.query.all()
    levels = Level.query.all()
    # print(time)
    # return "njay"
    if request.method == 'POST':
        print("submitted")
        candidate = User()
        if request.form['password'] != request.form['repassword']:
            flash("Confirmation password should be a same")
            return redirect(url_for('candidate.add'))
        timenow = datetime.utcnow()
        time = timenow.strftime("%H%M%S")
        fullname = request.form['fullname'].split(" ")
        firstname = fullname[0]
        generated_username = firstname+time
        # print(firstname+time)
        # return "anjay"
        # candidate.username = request.form['username']
        candidate.username = generated_username
        candidate.email = request.form['email']  
        candidate.fullname = request.form['fullname']
        candidate.phone = request.form['phone'] 
        candidate.address = request.form['address'] 
        candidate.division_id = request.form['division'] 
        candidate.level_id = request.form['level']
        candidate.set_password(request.form['password'] )
        db.session.add(candidate)
        db.session.commit()
        return redirect(url_for('admin.candidate_data'))
        
    return render_template('admin/candidate/add.html', divisions=divisions, levels=levels)

@login_required
@admin.route('/candidate/edit/<id>', methods=['GET', 'POST'])
@csrf.exempt
def candidate_edit(id):
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
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
        return redirect(url_for('admin.candidate_data'))
    return render_template('admin/candidate/edit.html', candidate=candidate, divisions=divisions, levels=levels)

@login_required
@admin.route('/candidate/set_schedule/<id>', methods=['GET', 'POST'])
@csrf.exempt
def candidate_set_schedule(id):
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    schedule_date = ""
    schedule_time = ""
    schedule = Candidate_Schedule_Test()
    divisions = Division.query.all()
    levels = Level.query.all()
    candidate = User.query.filter_by(id=id).first()
    is_time_set = Candidate_Schedule_Test.query.filter_by(candidate_id=candidate.id).first()
    if is_time_set:
        schedule_date = is_time_set.date_test.strftime("%m/%d/%Y")
        schedule_time = is_time_set.date_test.strftime("%H:%M")
        schedule = is_time_set
    # print(schedule)
    if request.method == 'POST':
        timeFormated = request.form['date']+" "+request.form['time']
        datetimeformated = datetime.strptime(timeFormated,'%m/%d/%Y %H:%M')
        schedule.candidate_id = id
        schedule.date_test = datetimeformated
        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for('admin.candidate_data'))
    return render_template('admin/candidate/set_schedule_add.html', candidate=candidate, schedule_date=schedule_date, schedule_time=schedule_time)

@login_required
@admin.route('/candidate/delete/<id>', methods=['GET', 'POST'])
@csrf.exempt
def candidate_delete(id):
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.home'))
    candidate = User.query.filter_by(id=id).first()
    candidate.status = False
    db.session.add(candidate)
    db.session.commit()
    return redirect(url_for('admin.candidate_data'))

"""
    =====================================================
                    END OF CANDIDATE MODULE
    =====================================================
"""

"""
    =====================================================
                    EXAMINATION MODULE
    =====================================================
"""

@login_required
@admin.route('/examination/examination_data', methods=['GET', 'POST'])
@csrf.exempt
def examination_data():
    _keyword = ""
    # _example = Question().data_list(1)
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('question.home'))
    if request.method == "POST":
        _keyword= request.form['keyword']
    _search = "%{}%".format(_keyword)
    page = request.args.get('page', 1, type=int)
    total_rows = Examination.query.filter(Examination.status.is_(True)).count()
    boxsize = ROWS_PER_PAGE
    num_pages = -(total_rows // -boxsize)
    examination = Examination.query.filter(Examination.status.is_(True)).paginate(page=page, per_page=ROWS_PER_PAGE)
    next_url = url_for('admin.examination_data', page=examination.next_num) \
        if examination.has_next else None
    prev_url = url_for('admin.examination_data', page=examination.prev_num) \
        if examination.has_prev else None
    return render_template('admin/examination/index.html', examinations=examination.items, prev_url=prev_url, next_url=next_url, num_pages=int(num_pages))


@login_required
@admin.route('/examination/examination_add', methods=['GET', 'POST'])
@csrf.exempt
def examination_add():
    # Check If user role is superadmin or admin
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    
    # get all data from database
    divisions = Division.query.all()
    levels = Level.query.all()
    if request.method == 'POST':
        check_availibility = Examination.query.filter_by(division_id=request.form['division'], level_id=request.form['level']).first()
        if check_availibility is not None:
            flash("The data with this setting has been already exist")
            return redirect(url_for('admin.examination_add'))
        examination = Examination()
        examination.name = request.form['name']
        examination.division_id = request.form['division']  
        examination.level_id = request.form['level']
        db.session.add(examination)
        db.session.commit()
        return redirect(url_for('admin.examination_data'))
        
    return render_template('admin/examination/add.html', levels=levels, divisions=divisions)

@login_required
@admin.route('/examination/examination_edit/<id>', methods=['GET', 'POST'])
@csrf.exempt
def examination_edit(id):
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    examination = Examination.query.filter_by(id=id).first()
    if request.method == 'POST':
        print(request.form)
        examination.name = request.form['name']
        db.session.add(examination)
        db.session.commit()
        # return to admin route. function
        return redirect(url_for('admin.examination_data'))
    return render_template('admin/examination/edit.html', examination=examination)

@login_required
@admin.route('/examination/examination_delete/<id>', methods=['GET', 'POST'])
@csrf.exempt
def examination_delete(id):
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    examination = Examination.query.filter_by(id=id).first()
    db.session.delete(examination)
    db.session.commit()
    return redirect(url_for('admin.examination_data'))

"""
    =====================================================
                    END OF EXAMINATION MODULE
    =====================================================
"""

"""
    =====================================================
                    QUESTION MODULE
    =====================================================
"""

@login_required
@admin.route('/question/question_data/<id>', methods=['GET', 'POST'])
@csrf.exempt
def question_data(id):
    _keyword = ""
    # _example = Question().data_list(1)
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('question.home'))
    if request.method == "POST":
        _keyword= request.form['keyword']
    _search = "%{}%".format(_keyword)
    get_exam = Examination.query.filter_by(id=id).first()
    division = Division.query.filter_by(id=get_exam.division_id).first()
    level = Level.query.filter_by(id=get_exam.level_id).first()
    page = request.args.get('page', 1, type=int)
    total_rows = Question.query.filter_by(examination_id=id).count()
    boxsize = ROWS_PER_PAGE
    num_pages = -(total_rows // -boxsize)
    question = Question.query.filter_by(examination_id=id).paginate(page=page, per_page=ROWS_PER_PAGE)
    next_url = url_for('admin.question_data', page=question.next_num) \
        if question.has_next else None
    prev_url = url_for('admin.question_data', page=question.prev_num) \
        if question.has_prev else None
    return render_template('admin/question/index.html', quetions=question.items, level=level, division=division, get_exam=get_exam, exam_name=get_exam.name, prev_url=prev_url, next_url=next_url, num_pages=int(num_pages))
    
@login_required
@admin.route('/question/question_add/<id>', methods=['GET', 'POST'])
@csrf.exempt
def question_add(id):
    # Check If user role is superadmin or admin
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    
    # get all data from database
    print(id)
    get_exam = Examination.query.filter_by(id=id).first()
    division = Division.query.filter_by(id=get_exam.division_id).first()
    level = Level.query.filter_by(id=get_exam.level_id).first()
    if request.method == 'POST':
        # set variable to false
        is_multiple = False
        # check if form post got an answer list choice
        check_multiple_choices = request.form.getlist('answer[]')
        if check_multiple_choices:
            # if have a list set variable to true
            is_multiple = True
        question = Question()
        question.name = request.form['name']
        question.question_division_id = request.form['division']  
        question.question_level_id = request.form['level']
        question.question = request.form['question']
        question.is_multiple_choice = is_multiple
        db.session.add(question)
        db.session.commit()
        if is_multiple:
            for i in check_multiple_choices:
                mc = Multiple_Choice()
                mc.name = i
                mc.question_id = question.id
                db.session.add(mc)
                db.session.commit()
        # return "halo"
        return redirect(url_for('admin.question_data'))
        
    return render_template('admin/question/add.html', level=level, division=division, examination_id=id, exam_name=get_exam.name)

@login_required
@admin.route('/question/question_edit/<id>', methods=['GET', 'POST'])
@csrf.exempt
def question_edit(id):
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    question = Question.query.filter_by(id=id).first()
    if request.method == 'POST':
        question.username = request.form['username']
        question.email = request.form['email']  
        question.fullname = request.form['fullname']
        question.phone = request.form['phone'] 
        question.address = request.form['address']
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('admin.question_data'))
    return render_template('admin/question/edit.html', question=question)

@login_required
@admin.route('/question/question_delete/<id>', methods=['GET', 'POST'])
@csrf.exempt
def question_delete(id):
    if current_user.role_id not in [1,2]:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    question = User.query.filter_by(id=id).first()
    question.status = False
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('admin.question_data'))

"""
    =====================================================
                    END OF QUESTION MODULE
    =====================================================
"""

"""
    ====================================
            STATIC ONLINE IN PDF
    ====================================
"""

@login_required
@admin.route('/question/question_pdf_data/<id>', methods=['GET', 'POST'])
@csrf.exempt
def question_pdf_data(id):
    _keyword = ""
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('question.home'))
    if request.method == "POST":
        _keyword= request.form['keyword']
    _search = "%{}%".format(_keyword)
    directory = "/static/uploads/test/"
    get_exam = Examination.query.filter_by(id=id).first()
    division = Division.query.filter_by(id=get_exam.division_id).first()
    level = Level.query.filter_by(id=get_exam.level_id).first()
    page = request.args.get('page', 1, type=int)
    total_rows = Pdf_Test.query.filter_by(examination_id=id).count()
    boxsize = ROWS_PER_PAGE
    num_pages = -(total_rows // -boxsize)
    question_pdf = Pdf_Test.query.filter_by(examination_id=id).paginate(page=page, per_page=ROWS_PER_PAGE)
    next_url = url_for('admin.question_data', page=question_pdf.next_num) \
        if question_pdf.has_next else None
    prev_url = url_for('admin.question_data', page=question_pdf.prev_num) \
        if question_pdf.has_prev else None
    return render_template('admin/master_test/index.html', quetions=question_pdf.items, level=level, division=division, get_exam=get_exam, exam_name=get_exam.name, prev_url=prev_url, next_url=next_url, num_pages=int(num_pages),directory=directory)

@login_required
@admin.route('/question/question_pdf_add/<id>', methods=['GET', 'POST'])
@csrf.exempt
def question_pdf_add(id):
    # Check If user role is superadmin or admin
    if current_user.role_id not in ADMIN_PERMISSION_LIST:
        flash("You have no permision!")
        return redirect(url_for('candidate.index'))
    get_exam = Examination.query.filter_by(id=id).first()
    division = Division.query.filter_by(id=get_exam.division_id).first()
    level = Level.query.filter_by(id=get_exam.level_id).first()
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        timenow = datetime.utcnow()
        time = timenow.strftime("%H%M%S")
        filename_ = file.filename.replace(" ", "_")
        file.save(os.path.join(apps.config['UPLOAD_PATH'],filename_))
        question = Pdf_Test()
        question.filename = filename_
        question.instruction = request.form['instruction']
        question.examination_id = id
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('admin.question_pdf_data', id=id))
        
    return render_template('admin/master_test/add.html', level=level, division=division, examination_id=id, exam_name=get_exam.name)