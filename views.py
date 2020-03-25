"""
views imports app, auth, and models, but none of these import views
"""
from app import app,db
from models import *
from forms import *
from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from auth import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

@app.route('/index')
@login_required
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
@login_required

def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/add')
@login_required

def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
@login_required
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletepost/<int:post_id>')
@login_required
def deletepost(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))


#user authentication

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html",name=current_user.username)

@app.route("/signup",methods=["POST","GET"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,method="sha256")
        new_user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return "<h1>New user has been created</h1>"
       
    return render_template("signup.html",form=form)

@app.route("/login",methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user :
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
            else:
                return '<h1>invalid username/password</h1>'
        
    return render_template("login.html",form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))