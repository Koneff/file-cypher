from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uploads import UploadSet, configure_uploads, TEXT

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOADED_DOCS_DEST'] = 'C:/Users/Anton/Desktop/docs'
uploaded_docs = UploadSet('docs', TEXT)
configure_uploads(app, uploaded_docs)
db = SQLAlchemy(app)


from app import views, models
