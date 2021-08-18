from flask_login.utils import _secret_key
from sqlalchemy.orm import backref
from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from flask_login import login_required
from datetime import datetime

_secret_key_mine = "dnsia129eGH1092dnsua81ainfia18ecdsn382r76dsnkudsay"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.route('/secret')
# @login_required
# def secret():
#     return 'Only authenticated users are allowed!'

class Role(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
    
    def insert_static_data(self):
        values = ['superadmin', 'admin', 'candidate']
        for v in values:
            role = Role()
            role.name = v
            db.session.add(role)
            db.session.commit()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(128))
    phone = db.Column(db.String(15))
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=3)
    is_deleted = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)
    # canidate_schedules = db.relationship('Candidate_Schedule_Test', backref='user', lazy='dynamic')
    # candidate_tests = db.relationship('Candidate_Test', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def insert_static_data(self):
        values = [
            { "email" : "example2@gmail.com", "username" :"ardipramanova", "password": "ardiziermedia123", "role_id": 1 },
            { "email" : "example1@gmail.com", "username" :"dhinifeniks", "password": "dhinimedia123", "role_id": 2 },
            { "email" : "example3@gmail.com", "username" :"ayufeniks", "password": "ayumedia123", "role_id": 2 }
            ]
        for v in values:
            user = User()
            user.username = v['username']
            user.password_hash = generate_password_hash(v['password'])
            user.email = v['email']
            user.role_id = v['role_id']
            db.session.add(user)
            db.session.commit()
    
    def insert_data(self, data):
        user = User()
        user.email = data['email']
        user.username = data['username']
        password_hashed = generate_password_hash(str(data['password'])+_secret_key_mine)
        # check = check_password_hash(nyanya, str(data['password'])+_secret_key_mine)
        user.email = data['email']
        user.password = password_hashed
        user.role_id = data['role']
        db.session.add(user)
        db.session.commit()
        return "00"
    
    def data_list():
        _dict = []
        user = User.query.filter_by(role_id=3).all()
        for u in user:
            schedule = "Not Set"
            schedule_status = 0
            get_schedule = Candidate_Schedule_Test.query.filter_by(candidate_id=u.id).first()
            if get_schedule is not None :
                schedule = get_schedule.date_test
                schedule_status = 1
            _dict.append({"name" : u.fullname, "email" : u.email,"phone" : u.phone, "address" : u.address, "status": schedule_status, "schedule": schedule, "division" : u.division.name, "level" : u.level.name})
        
        return _dict


class Candidate(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(128))
    phone = db.Column(db.String(15))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=3)
    status = db.Column(db.Boolean, default=True)
    

    def insert(self, data):
        candidate = Candidate()

        return True

class Level(db.Model):
    __tablename__ = "level"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=True)
    examinations = db.relationship('Examination', backref='level', lazy='dynamic')
    users = db.relationship('User', backref='level', lazy='dynamic')

    def __repr__(self):
        return '<Question_Level %r>' % self.name
    
    def insert_static_data(self):
        values = ['SPV', 'Staff', 'All']
        for v in values:
            level = Level()
            level.name = v
            db.session.add(level)
            db.session.commit()

class Division(db.Model):
    __tablename__ = "division"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=True)
    examinations = db.relationship('Examination', backref='division', lazy='dynamic')
    users = db.relationship('User', backref='division', lazy='dynamic')

    def __repr__(self):
        return '<Division %r>' % self.name
    
    def insert_static_data(self):
        values = ['Accounting', 'Audit' , 'Legal', 'HR', 'IT', 'All']
        for v in values:
            division = Division()
            division.name = v
            db.session.add(division)
            db.session.commit()

class Examination(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    is_multiple_choice = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)
    questions = db.relationship('Question', backref='examination', lazy='dynamic')
    choices = db.relationship('Multiple_Choice', backref='examination', lazy='dynamic')
    pdfs = db.relationship('Pdf_Test', backref='examination', lazy='dynamic')
    
    def __repr__(self):
        return '<Examination %r>' % self.name

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.Text())
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'))
    status = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return '<Question %r>' % self.name

class Multiple_Choice(db.Model):
    __tablename__ = "multiple_choice"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, index=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'))
    is_correct = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return '<Multiple_Choice %r>' % self.name

# ======================= STATIC MODELS =============================

class Psikotest_Type(db.Model):
    __tablename__ = "psikotest_type"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=True)
    psikotests = db.relationship('Psikotest', backref='psikotest_type', lazy='dynamic')

    def __repr__(self):
        return '<Psikotest_Type %r>' % self.name
    
    def insert_static_data(self):
        values = ['CFIT', 'WPT']
        for v in values:
            pt = Psikotest_Type()
            pt.name = v
            db.session.add(pt)
            db.session.commit()

class Psikotest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(128))
    instruction = db.Column(db.Text())
    psikotest_type_id = db.Column(db.Integer, db.ForeignKey('psikotest_type.id'))
    status = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return '<Psikotest %r>' % self.name
    
    def insert_static_data(self):
        values = [
            { "filename" : "soal_cfit.pdf", "instruction" : "SIlahkan Baca Instruksi Lembar soal !", "psikotest_type_id": 1 },
            { "filename" : "soal_wpt.pdf", "instruction" : "SIlahkan Baca Instruksi Lembar soal !", "psikotest_type_id": 2 }
            ]
        for v in values:
            p= Psikotest()
            p.filename = v['filename']
            p.instruction = v['instruction']
            p.psikotest_type_id = v['psikotest_type_id']
            db.session.add(p)
            db.session.commit()

class Pdf_Test(db.Model):
    __tablename__ = "pdf_test"
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(128))
    instruction = db.Column(db.Text())
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'))
    status = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return '<Pdf_Test %r>' % self.name

class Candidate_Schedule_Test(db.Model):
    __tablename__ = "candidate_schedule_test"
    id = db.Column(db.Integer, primary_key = True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_test = db.Column(db.DateTime())
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Candidate_Schedule_Test %r>' % self.date_test

class Candidate_Test(db.Model):
    __tablename__ = "candidate_test"
    id = db.Column(db.Integer, primary_key = True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pdf_test_id = db.Column(db.Integer, db.ForeignKey('pdf_test.id'))
    time_test = db.Column(db.Time())
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Candidate_Test %r>' % self.name
    
    def insert_static_data(self):
        values = ['psikotest', 'specific']
            

# ======================= END STATIC MODELS ==========================

# Insert Static data using python shell
def reinit():
    db.drop_all()
    db.create_all()

def initialize_data():
    Role().insert_static_data()
    User().insert_static_data()
    Level().insert_static_data()
    Division().insert_static_data()
    Psikotest_Type().insert_static_data()
