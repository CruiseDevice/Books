import os
import sqlite3

from flask import Flask, session, flash, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from forms import LoginForm
from models import User

def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])

@app.route('/index/')
def index():
	return render_template('index.html')

@app.route("/", methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if form.validate_on_submit():
		user = User.query.filter_by(name=request.form['name']).first()
		if user is not None and user.password == request.form['password']:
			session['logged_in'] = True
			session['user_id'] = user.id
			session['role'] = user.role
			session['name'] = user.name
			flash('Welcome!')
			return redirect(url_for('index'))
		else:
			error = 'Invalid username or password.'
	return render_template('login.html',form=form, error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Goodbye!')
	return redirect(url_for('login'))