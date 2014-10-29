from app import app, db, uploaded_docs
from models import User, Upload
from flask import render_template, request, flash, redirect, url_for, session
from forms import SignupForm, SigninForm, UploadForm
from flask.ext.uploads import UploadNotAllowed


@app.route('/')
def home():
    if 'email' in session:
        return redirect(url_for('upload'))
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #FIXME Make password checking
    if 'email' in session:
        return redirect(url_for('profile'))
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            session['email'] = newuser.email
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'email' in session:
        return redirect(url_for('profile'))
    form = SigninForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('signin.html', form=form)


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('home'))
    user = User.query.filter_by(email=session['email']).first()

    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST' and 'doc' in request.files:
        doc = request.files.get('doc')
        if not doc:
            flash("You must choose file!")
        else:
            try:
                filename = uploaded_docs.save(request.files['doc'])
            except UploadNotAllowed:
                flash("The upload was not allowed!")
            else:
                newupload = Upload(file_name=filename, timestamp=form.published.data)
                db.session.add(newupload)
                db.session.commit()
    return render_template('uploads.html', form=form)


@app.route('/history')
def history():
    if 'email' not in session:
        return redirect(url_for('home'))
    return render_template('history.html')


@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('home'))
    session.pop('email', None)
    return redirect(url_for('signup'))  #TODO change to home