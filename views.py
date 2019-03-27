import os
import json
import sqlite3
import requests

from flask import (
		  Flask, session, flash, request, redirect, render_template,
		  url_for, jsonify
)
from flask_login import login_user, logout_user, login_required, current_user,\
					LoginManager
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

from credentials import API_KEY, API_SECRET

from forms import LoginForm, SignUpForm, SearchForm, CommentForm
from models import User, db, Books, Comment

app = Flask(__name__)
login_manager = LoginManager()
app.config.from_object('_config')
db.init_app(app)
db.create_all(app=app)


def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])


@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index(results=None):
	query = SearchForm(request.form)
	if request.method == 'POST':
		results = search_results(query)
	return render_template('index.html', form=query, results=results)


@app.route('/results')
@login_required
def search_results(query):
	if query:
		search_query = query.data['query']
		if search_query:
			search_result = Books.query.filter(
				(Books.year==search_query) |
				(Books.title==search_query) |
				(Books.author==search_query) |
				(Books.isbn==search_query)).all()
			return search_result
	return redirect('/index/')


@app.route("/", methods=['GET', 'POST'])
def login():
	error = None
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			username = form.username.data
			password = form.password.data

			user = User.query.filter_by(username=username).first()
			if user is not None and user.verify_password(password):
				login_user(user)
				next = request.args.get('next')
				if next is None or not next.startswith('/'):
					next = url_for('index')
				return redirect(next)
			else:
				error = 'Invalid username or password.'
		else:
			return render_template('login.html',form=form, error=error)
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
				return render_template('register.html', form=form, error=error)
		else:
			return render_template('register.html', form=form, error=error)
	if request.method == 'GET':
		return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Goodbye!')
	return redirect(url_for('login'))


@app.route('/book-detail/<isbn>', methods=['GET', 'POST'])
@login_required
def book_detail(isbn=None, error=None):
	user = current_user._get_current_object()
	all_comments = Comment.query.filter_by()
	book_query = Books.query.filter_by(isbn=isbn).first()
	book_comments = book_query.comments.order_by(Comment.timestamp.asc())
	user_comment = book_comments.filter_by(author_id=user.id).all()
	book_comments = book_comments.all()
	response = requests.get(
		"https://www.goodreads.com/book/review_counts.json",
		params={"key":API_KEY, "isbns": isbn})
	if response.status_code == 200:
		response = response.json()
	else:
		error = 'No books match those ISBNs.'
	comment_form = CommentForm(request.form)
	if request.method == "POST":
		if user_comment is not None:
			flash('You can only review the book once.')
		else:
			if comment_form.validate_on_submit():
				comment = Comment(body=comment_form.body.data,
								  book_id=book_query.id,
								  author_id=user.id)
				db.session.add(comment)
				db.session.commit()
				flash('Your comment has been published.')
				return redirect(url_for('book_detail', isbn=isbn))
	return render_template('book_detail.html',
					isbn=isbn, response=response['books'],
					book=book_query ,error=error,
					comment_form=comment_form,
					book_comments=book_comments)


@app.route('/api/<isbn>', methods=['GET'])
def api_book_detail(isbn=None, error=None):
	book = Books.query.filter_by(isbn=isbn).first()
	res = requests.get("https://www.goodreads.com/book/review_counts.json",
		params={"key":API_KEY, "isbns": isbn})
	if res.status_code == 200:
		res = res.json()
	response = jsonify({
			'id': book.id,
			'isbn': book.isbn,
			'title': book.title,
			'author': book.author,
			'year': book.year,
			'reviews_count':'' ,
			'average_score':'' ,
		})
	response.status_code = 200
	return response