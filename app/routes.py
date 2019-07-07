
from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    # user = {"username" : "Rishabh Sarup"}
    return render_template('index.html', title = "Index")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/home')
def home():
    user = {"username": "Rishabh Sarup"}
    return render_template('home.html', title = "Home", user=user)
