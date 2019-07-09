#models.py file

from app import db

#Class for users of the app - includes an overview of all their balances
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    cashBalance = db.Column(db.Integer, index = True)
    bankBalance = db.Column(db.Integer, index = True)
    payappBalance = db.Column(db.Integer, index = True)
    password_hash = db.Column(db.String(128))

    #creating relations between user and transactions
    allCashTransactions = db.relationship('CashTransaction', backref = 'cashspender', lazy = 'dynamic')
    allBankTransactions = db.relationship('BankTransaction', backref= 'bankspender', lazy = 'dynamic')
    allPayAppTransactions = db.relationship('PayAppTransaction', backref = 'payappspender', lazy = 'dynamic' )

    def __repr__(self):
        return '<User {}>'.format(self.username)

#Class for all cash transactions that the user makes.
class CashTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #The user that the transaction is associated with.
    debit = db.Column(db.Boolean, index = True) # True if the amount is to be subtracted, false if it is actually a credit
    amount = db.Column(db.Integer, index = True)
    description = db.Column(db.String(255), index = True)

class BankTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #The user that the transaction is associated with.
    debit = db.Column(db.Boolean, index = True) # True if the amount is to be subtracted, false if it is actually a credit
    amount = db.Column(db.Integer, index = True)
    description = db.Column(db.String(255), index = True)

class PayAppTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #The user that the transaction is associated with.
    debit = db.Column(db.Boolean, index = True) # True if the amount is to be subtracted, false if it is actually a credit
    amount = db.Column(db.Integer, index = True)
    description = db.Column(db.String(255), index = True)
