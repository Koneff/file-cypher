from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)  #salted password

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)  #return True if match


class Upload(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    #dbx_in = db.Column(db.Boolean)  #dropbox integration
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, file_name, timestamp):
        self.file_name = file_name.title()
        self.timestamp = timestamp.title()