
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TransactionForm, ResetPasswordRequestForm, StartingBalanceForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Transaction
from werkzeug.urls import url_parse
from app.email import send_password_reset_email


#Displays index according to the conditions in index.html. View differs when user is logged in and not logged in.
@app.route('/')
@app.route('/index')
def index():
    # user = {"username" : "Rishabh Sarup"}
    return render_template('index.html', title = "Index")

#Registers a new user and sets their starting balances
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(home))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, cashBalance = 0, bankBalance=0, payappBalance=0, currency = "")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are now a registered user')
        return redirect(url_for('login'))
    return render_template('registration.html', title = "Register", form = form)

#route in order to allow the users to set their starting balances
@app.route('/startingbalance', methods = ['GET', 'POST'])
def startingbalance(): 
    if current_user.is_anonymous: 
        return redirect(url_for(login))
    form = StartingBalanceForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = current_user.username).first()
        user.cashBalance = form.cash.data
        user.bankBalance = form.bank.data
        user.payappBalance = form.payapp.data
        user.currency = form.currency.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('startingbalance.html', title = "Record Starting Balances", form = form)


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
@app.route('/logtransaction', methods = ['GET', 'POST'])
@login_required
def logcash():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(user_id = current_user.id, date = form.date.data, amount = form.amount.data, description= form.description.data, category = form.category.data, type = form.type.data, transtype = form.transtype.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction Registered')
        if transaction.type == "Cash":
            if transaction.transtype == 'debit':
                current_user.cashBalance = current_user.cashBalance - transaction.amount
                user = User.query.filter_by(username = current_user.username).first()
                user.cashBalance = current_user.cashBalance
                db.session.commit()
            elif transaction.transtype == 'receipt':
                current_user.cashBalance = current_user.cashBalance + transaction.amount
                user = User.query.filter_by(username = current_user.username).first()
                user.cashBalance = current_user.cashBalance
                db.session.commit()
        elif transaction.type == "Bank":
            if transaction.transtype == "debit":
                current_user.bankBalance = current_user.bankBalance - transaction.amount
                user = User.query.filter_by(username = current_user.username).first()
                user.bankBalance = current_user.bankBalance
                db.session.commit()
            elif transaction.transtype == "receipt":
                current_user.bankBalance = current_user.bankBalance + transaction.amount
                user = User.query.filter_by(username = current_user.username).first()
                user.bankBalance = current_user.bankBalance
                db.session.commit()
            elif transaction.transtype == 'banktopayapp': 
                current_user.bankBalance = current_user.bankBalance - transaction.amount
                current_user.payappBalance = current_user.payappBalance + transaction.amount 
                user = User.query.filter_by(username = current_user.username).first()
                user.bankBalance = current_user.bankBalance
                user.payappBalance = current_user.payappBalance
                db.session.commit()
            elif transaction.transtype == 'payapptobank': 
                current_user.bankBalance = current_user.bankBalance + transaction.amount
                current_user.payappBalance = current_user.payappBalance - transaction.amount
                user = User.query.filter_by(username = current_user.username).first()
                user.bankBalance = current_user.bankBalance
                user.payappBalance = current_user.payappBalance
                db.session.commit()
        elif transaction.type == "PayApp":
            if transaction.transtype == "debit":
                current_user.payappBalance = current_user.payappBalance - transaction.amount
                user = User.query.filter_by(username = current_user.username).first()
                user.payappBalance = current_user.payappBalance
                db.session.commit()
            elif transaction.transtype == "credit":
                current_user.pay = current_user.payappBalance + transaction.amount
                user = User.query.filter_by(username = current_user.username).first()
                user.payappBalance = current_user.payappBalance
                db.session.commit()
            elif transaction.transtype == 'payapptobank': 
                current_user.bankBalance = current_user.bankBalance + transaction.amount
                current_user.payappBalance = current_user.payappBalance - transaction.amount 
                user = User.query.filter_by(username = current_user.username).first()
                user.bankBalance = current_user.bankBalance
                user.payappBalance = current_user.payappBalance
                db.session.commit()
            elif transaction.transtype == 'banktopayapp': 
                current_user.bankBalance = current_user.bankBalance - transaction.amount
                current_user.payappBalance = current_user.payappBalance + transaction.amount 
                user = User.query.filter_by(username = current_user.username).first()
                user.bankBalance = current_user.bankBalance
                user.payappBalance = current_user.payappBalance
                db.session.commit()
        return redirect(url_for('login'))

    return render_template('logtransaction.html', title = "Log Transaction", form = form)


#displays all cash transactions
@app.route('/allcashtransaction')
@login_required
def allcashtransaction():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    user = current_user
    transactions = current_user.allTransactions
    cashlist = []
    for transaction in transactions: 
        if transaction.type == 'Cash':
            cashlist.append(transaction)
    return render_template('cashtransactions.html', user = user, transactions = transactions)


#displays all bank transactions
@app.route('/allbanktransaction')
@login_required
def allbanktransaction():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    user = current_user
    transactions = current_user.allTransactions
    banklist = []
    for transaction in transactions: 
        if transaction.type == 'Bank':
            banklist.append(transaction)
    return render_template('banktransactions.html', user = user, transactions = banklist)


#displays all payapp transactions
@app.route('/allpayapptransaction')
@login_required
def allpayapptransaction():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    user = current_user
    transactions = current_user.allTransactions
    payapplist = []
    for transaction in transactions: 
        if transaction.type == 'PayApp':
            payapplist.append(transaction)
    return render_template('payapptransactions.html', user = user, transactions = payapplist)

#displays all user transactions (trial) 
@app.route('/alltransactions')
@login_required
def alltransactions():
    if current_user.is_anonymous:
        return redirect(url_for(login))
    user = current_user
    transactions = current_user.allTransactions
    return render_template('alltransactions.html', user = user, transactions = transactions)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

from app.forms import ResetPasswordForm


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
