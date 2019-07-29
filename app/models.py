#models.py file

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, app
from time import time
import jwt


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



#Class for users of the app - includes an overview of all their balances
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    cashBalance = db.Column(db.Float, index = True)
    bankBalance = db.Column(db.Float, index = True)
    payappBalance = db.Column(db.Float, index = True)
    password_hash = db.Column(db.String(128))

    #creating relations between user and transactions
    allTransactions = db.relationship('Transaction', backref = 'spender',lazy = 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

#Class for all transactions that the user makes. Replacing all transaction types into one big model. 
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #The user that the transaction is associated with.
    date = db.Column(db.String, index = True)
    debit = db.Column(db.Boolean, index = True) # True if the amount is to be subtracted, false if it is actually a credit
    amount = db.Column(db.Float, index = True)
    description = db.Column(db.String(255), index = True)
    category = db.Column(db.String(255), index = True)
    type = db.Column(db.String(255), index = True)

# class BankTransaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #The user that the transaction is associated with.
#     date = db.Column(db.String, index = True)
#     debit = db.Column(db.Boolean, index = True) # True if the amount is to be subtracted, false if it is actually a credit
#     amount = db.Column(db.Float, index = True)
#     description = db.Column(db.String(255), index = True)
#     category = db.Column(db.String(255), index = True)

# class PayAppTransaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #The user that the transaction is associated with.
#     date = db.Column(db.String, index = True)
#     debit = db.Column(db.Boolean, index = True) # True if the amount is to be subtracted, false if it is actually a credit
#     amount = db.Column(db.Float, index = True)
#     description = db.Column(db.String(255), index = True)
#     category = db.Column (db.String(255), index = True)
