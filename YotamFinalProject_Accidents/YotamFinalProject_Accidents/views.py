"""
Routes and views for the flask application.
"""
from YotamFinalProject_Accidents import app
from YotamFinalProject_Accidents.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
from YotamFinalProject_Accidents.Models.QueryFormStructure import UserRegistrationFormStructure 
from YotamFinalProject_Accidents.Models.Forms import ExpandForm
from YotamFinalProject_Accidents.Models.Forms import CollapseForm
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask import render_template
from datetime import datetime
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json 
import requests
import io
import base64
from os import path
from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'nuwanda'
db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Contact me'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='About the project'
    )

@app.route('/data')
def data():
    """Renders the about page."""
    return render_template(
        'data.html',
        title='Data',
        year = datetime.now().year,
    )

@app.route('/data/AccidentsData' , methods = ['GET' , 'POST'])
def AccidentsData():
    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\US_Accidents_Dec19.csv'))
    raw_data_table = ''
 
    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''
 
    
 
    return render_template(
        'AccidentsData.html',
        title='Accidents data',
        year=datetime.now().year,
        message='The Data itself',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            return redirect('/login')
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/login')
def login():
    """Renders the about page."""
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        message='Login page'
    )

@app.route('/query')
def query():
    """Renders the about page."""
    return render_template(
        'query.html',
        title='Query',
        year=datetime.now().year,
        message='Query page and data visualizing'
    )