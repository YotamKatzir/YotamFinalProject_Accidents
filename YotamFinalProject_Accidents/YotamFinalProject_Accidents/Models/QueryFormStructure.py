
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

#defining the query form fields and stracture
class QueryFormStructure(FlaskForm):
    secpar = SelectField('Second parameter to analyze by:' , choices=[('Amenity', 'Amenity'), ('Bump', 'Bump'), ('Crossing', 'Crossing'), ('Give_Way', 'Give_Way'), ('Junction', 'Junction'), ('No_Exit', 'No_Exit'), ('Railway', 'Railway'), ('Roundabout', 'Roundabout'), ('Station', 'Station'), ('Stop', 'Stop'), ('Traffic_Calming', 'Traffic_Calming'), ('Traffic_Signal', 'Traffic_Signal')], validators = [DataRequired])
    submit = SubmitField('Submit')

#defining the login form fields and stracture
class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

#defining the register form fields and stracture
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')


