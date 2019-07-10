from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, CashTransaction, BankTransaction, PayAppTransaction


#Form that takes in login factors
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#form that takes in info for a new registrant
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])
    cash = IntegerField('Starting Cash Balance')
    bank = IntegerField('Starting Bank Balance')
    payapp = IntegerField('Starting PayApp Balance')
    submit = SubmitField('Register')

class TransactionForm(FlaskForm):
    date = StringField('Date - Enter dd/mm/yy', validators = [DataRequired()])
    debit = BooleanField('Was this a debit?')
    amount = IntegerField("Amount", validators = [DataRequired()])
    description = StringField('Describe your transaction', validators = [DataRequired()])



# If the username already exists in db, they will need to use a different name
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('There is already an account with this Username. Please use a different username.')

#If the email already exists in db, they will have to use a different email.
    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email is not None:
            raise ValidationError('This email has already been registered on this website. Please use a different email')
