
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TransactionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, CashTransaction, BankTransaction, PayAppTransaction
from werkzeug.urls import url_parse


#Displays index according to the conditions in index.html. View differs when user is logged in and not logged in.
@app.route('/')
@app.route('/index')
def index():
    # user = {"username" : "Rishabh Sarup"}
    return render_template('index.html', title = "Index")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(home))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, cashBalance = form.cash.data, bankBalance=form.bank.data, payappBalance=form.payapp.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are now a registered user')
        return redirect(url_for('login'))
    return render_template('registration.html', title = "Register", form = form)

#route to login a user
@app.route('/login', methods=['GET', 'POST'])
def login():

    #If the user is already logged in, and they try to click login again, they will just redirect to homepage.
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        #parses the next page name in the case of the @login_required redirect.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

#Logs the user out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Displays user information
@app.route('/home')
@login_required
def home():
    user = {"username": "Rishabh Sarup"}
    return render_template('home.html', title = "Home", user=user)

#Logging of a cash transaction
@app.route('/logcash', methods = ['GET', 'POST'])
@login_required
def logcash():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = CashTransaction(user_id = current_user.id, date = form.date.data, debit = form.debit.data, amount = form.amount.data, description= form.description.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Cash Transaction Registered')
        if transaction.debit == True:
            current_user.cashBalance = current_user.cashBalance - transaction.amount
            user = User.query.filter_by(username = current_user.username).first()
            user.cashBalance = current_user.cashBalance
            db.session.commit()
        if transaction.debit == False:
            current_user.cashBalance = current_user.cashBalance + transaction.amount
            user = User.query.filter_by(username = current_user.username).first()
            user.cashBalance = current_user.cashBalance
            db.session.commit()
        return redirect(url_for('login'))

    return render_template('logcash.html', title = "Log Cash Transaction", form = form)

#Records a bank transaction
@app.route('/logbank', methods = ['GET', 'POST'])
@login_required
def logbank():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = BankTransaction(user_id = current_user.id, date = form.date.data, debit = form.debit.data, amount = form.amount.data, description= form.description.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Bank Transaction Registered')
        if transaction.debit == True:
            current_user.bankBalance = current_user.bankBalance - transaction.amount
            user = User.query.filter_by(username = current_user.username).first()
            user.bankBalance = current_user.bankBalance
            db.session.commit()
        if transaction.debit == False:
            current_user.bankBalance = current_user.bankBalance + transaction.amount
            user = User.query.filter_by(username = current_user.username).first()
            user.bankBalance = current_user.bankBalance
            db.session.commit()
        return redirect(url_for('login'))

    return render_template('logbank.html', title = "Log Bank Transaction", form = form)

#Records a payapp transaction
@app.route('/logpayapp', methods = ['GET', 'POST'])
@login_required
def logpayapp():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = PayAppTransaction(user_id = current_user.id, date = form.date.data, debit = form.debit.data, amount = form.amount.data, description= form.description.data)
        db.session.add(transaction)
        db.session.commit()
        flash('PayApp Transaction Registered')
        if transaction.debit == True:
            current_user.payappBalance = current_user.payappBalance - transaction.amount
            user = User.query.filter_by(username = current_user.username).first()
            user.payappBalance = current_user.payappBalance
            db.session.commit()
        if transaction.debit == False:
            current_user.payappBalance = current_user.payappBalance + transaction.amount
            user = User.query.filter_by(username = current_user.username).first()
            user.payappBalance = current_user.payappBalance
            db.session.commit()
        return redirect(url_for('login'))

    return render_template('logpayapp.html', title = "Log PayApp Transaction", form = form)

@app.route('/allcashtransaction')
@login_required
def allcashtransaction():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    user = current_user
    transactions = current_user.allCashTransactions
    return render_template('cashtransactions.html', user = user, transactions = transactions)
