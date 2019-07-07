#models.py file

from app import db

#Class for users of the app - includes an overview of all their balances
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    bankBalance = db.Column(db.Integer)
    bankBalance = db.Column(db.Integer)
    payappBalance = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

#Class for all cash transactions that the user makes.
class CashTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique = True) #The user that the transaction is associated with.
    debit = db.Column(db.Boolean) # True if the amount is to be subtracted, false if it is actually a credit
    amount = db.Column(db.Integer)

    def __repr(self):
        return '<User {}>'.format(self.username) + str(id)

class BankTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique = True) #The user that the transaction is associated with.
    debit = db.Column(db.Boolean) # True if the amount is to be subtracted, false if it is actually a credit
    amount = db.Column(db.Integer)

    def __repr(self):
        return '<User {}>'.format(self.username) + str(id)

class PayAppTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique = True) #The user that the transaction is associated with.
    debit = db.Column(db.Boolean) # True if the amount is to be subtracted, false if it is actually a credit
    amount = db.Column(db.Integer)

    def __repr(self):
        return '<User {}>'.format(self.username) + str(id)

        
