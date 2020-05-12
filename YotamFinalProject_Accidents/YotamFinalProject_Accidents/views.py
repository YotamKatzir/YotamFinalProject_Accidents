#########
#IMPORTS#
#########
from YotamFinalProject_Accidents import app
from YotamFinalProject_Accidents.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
from YotamFinalProject_Accidents.Models.QueryFormStructure import UserRegistrationFormStructure 
from YotamFinalProject_Accidents.Models.QueryFormStructure import LoginFormStructure
from YotamFinalProject_Accidents.Models.QueryFormStructure import QueryFormStructure
from YotamFinalProject_Accidents.Models.Forms import ExpandForm
from YotamFinalProject_Accidents.Models.Forms import CollapseForm
from YotamFinalProject_Accidents.Models.PlotServiceFunctions import plot_to_img
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask import render_template
from datetime import datetime
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from os import path
from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json 
import requests
import io
import base64

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'nuwanda'
db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')

@app.route('/home') #The route for the home page
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact') #The route for the contact page
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Contact me'
    )

@app.route('/about') #The route for the about page
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='About the project'
    )

@app.route('/data') #The route for the data page
def data():
    return render_template(
        'data.html',
        title='Data',
        year = datetime.now().year,
    )

@app.route('/data/AccidentsData' , methods = ['GET' , 'POST']) #The route for the CSV page
def AccidentsData():#Defining the form actions for the data table
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


@app.route('/register', methods=['GET', 'POST']) #The route for the register page
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)): #defining the register form
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

@app.route('/login', methods=['GET', 'POST']) #The route for the login page
def login(): 
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()): #defining the register form
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('/query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/NonLoginQuery') #The route for the non login query page
def NonLoginQuery():
    return render_template(
        'NonLoginQuery.html',
        title='Data',
        year = datetime.now().year,
    )

@app.route('/query', methods=['GET', 'POST']) #The route for the login-only query page
def query():
        form = QueryFormStructure(request.form) #defining the query form
        chart = ""
        if(request.method=='POST'):
            fig, ax = plt.subplots()
            plt.tight_layout()
            secpar = form.secpar.data
            df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\US_Accidents_Dec19.csv'))
            dfc= df.drop(['TMC','Start_Lat','Start_Lng','Distance\(mi)','Description','Number','Street','Side','City','County','State','Wind_Direction','Precipitation(in)','Weather_Condition', 'Sunrise_Sunset', 'Turning_Loop'], 1)
            dfg=dfc[['Severity', secpar]]
            dfg=dfg.groupby('Severity').sum()
            graph = dfg.plot.pie(subplots=True, ax = ax)

        return render_template('query.html',
            title='User Data Query',
            form = form,
            img_under_construction = '/static/images/under_construction.png',
            chart = chart ,
            height = "300" ,
            width = "750",
            year=datetime.now().year
        )