import os
import sqlite3
import requests

from flask import (
		  Flask, session, flash, request, redirect, render_template,
		  url_for
)
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

from credentials import API_KEY, API_SECRET

from forms import LoginForm, SignUpForm, SearchForm
from models import User, db, Books

app = Flask(__name__)
app.config.from_object('_config')
db.init_app(app)
db.create_all(app=app)

def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])

@app.route('/index/', methods=['GET', 'POST'])
def index():
	query = SearchForm(request.form)
	if request.method == 'POST':
		return search_results(query)
	res = requests.get("https://www.goodreads.com/book/review_counts.json",
			params={"key":API_KEY, "isbns": "9781632168146"})
	return render_template('index.html', form=query)

@app.route('/results')
def search_results(query):
	results = []
	search_query = query.data['query']
	if search_query:
		print(search_query)
		search_result = Books.query.filter(year=search_query)
		print(search_result) 
	return redirect('/index/')


@app.route("/", methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			username = form.username.data
			password = form.password.data

			user = User.query.filter_by(username=username).first()
			if user:
				pasword_hash = user.password
				if check_password_hash(pasword_hash, password):
					session['logged_in'] = True
					session['user_id'] = user.id
					session['role'] = user.role
					session['name'] = user.username
					flash('Welcome!')
					return redirect(url_for('index'))
			else:
				error = 'Invalid username or password.'
		else:
			return render_template('login.html',form=form, error=error)
	if request.method == 'GET':
		return render_template('login.html',form=form, error=error)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	error = None
	form  = SignUpForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			username = form.username.data
			email = form.email.data
			password = form.password.data
			password = generate_password_hash(password)
			new_user = User(username=username, email=email, password=password)
			try:
				db.session.add(new_user)
				db.session.commit()
				flash('Thanks for registering. Please login.')
				return redirect(url_for('login'))
			except IntegrityError:
				error = 'Sorry that username and/or email already exists.'
				return render_template('regieter.html', form=form, error=error)
		else:
			return render_template('register.html', form=form, error=error)
	if request.method == 'GET':
		return render_template('register.html', form=form)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Goodbye!')
	return redirect(url_for('login'))