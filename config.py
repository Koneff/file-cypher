CSRF_ENABLED = True
SECRET_KEY = 'djdksji12djc97op'
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')