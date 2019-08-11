from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, InputRequired
from app.models import User, Transaction


#Form that takes in login factors
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

#form that takes in info for a new registrant
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password', message = "Passwords must match")])
    submit = SubmitField('Register')

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

class StartingBalanceForm(FlaskForm): 
    currency = SelectField('Select your Currency', choices = [('USD', 'USD'), ('SGD', 'SGD'), ('GBP', 'GBP')], validators= [DataRequired()])
    cash = DecimalField('Enter your opening cash balance', validators=[InputRequired('Please enter valid amount. Special characters not permitted.')])
    bank = DecimalField('Enter your opening bank balance', validators = [InputRequired('Please enter valid amount. Special characters not permitted.')])
    payapp = DecimalField('Enter your opening payapp balance', validators = [InputRequired('Please enter valid amount. Special characters not permitted.')])
    submit = SubmitField('Submit Opening Balances')

class TransactionForm(FlaskForm):
    date = StringField('Date - Enter dd/mm/yy', validators = [DataRequired()])
    # debit = BooleanField('Was this a debit?') #need to remove this field and adjust the rest of the app
    transtype = SelectField ('Please select the type of this transaction', choices = [('debit', 'Expense'), ('receipt', 'Receipt'), ('banktopayapp', 'Transfer from Own Bank Account to Own Pay App Account'), ('payapptobank', 'Transfer from Own PayApp Account to Own Bank Account')])
    amount = DecimalField("Amount", validators = [DataRequired("Please Enter Numbers Only")])
    type = SelectField('Receipt/Payment Mode', choices = [('Cash', 'Cash'), ('Bank', 'Bank'), ('PayApp', 'PayApp')], validators = [DataRequired()])
    category = SelectField('Transaction Category', choices = [('Allowance', 'Allowance'), ('Clothes', 'Clothes'), ('Drinks', 'Drinks'), ('Entertainment', 'Entertainment'), ('Food and Beverage', 'Food and Beverage'), ('Fuel', 'Fuel'), ('Gift', 'Gift'), ('Groceries', 'Groceries'), ('Health', 'Health'), ('Holiday', 'Holiday'),
    ('Home', 'Home'), ('Laundry', 'Laundry'), ('Rent', 'Rent'), ('Salary', 'Salary'), ('Shopping', 'Shopping'), ('Transport', 'Transport'), ('Others', 'Others')], validators = [DataRequired()])
    description = StringField('Describe your transaction (e.g GoJek trip back home)', validators = [DataRequired()])
    submit = SubmitField('Log Transaction')


