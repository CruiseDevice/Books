from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	role = db.Column(db.String, default='user')
	comments = db.relationship('Comment', backref='author', lazy='dynamic')

	def verify_password(self, password):
		return check_password_hash(self.password, password)

	def __init__(self, username=None, email=None, password=None, role=None):
		self.username = username
		self.email = email
		self.password = password
		self.role = role

	def __repr__(self):
		return '<User: {0}>'.format(self.username)


class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False


class Books(db.Model):
	__tablename__ = 'books'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	isbn = db.Column(db.Integer, unique=True, nullable=False)
	title = db.Column(db.String, nullable=False)
	author = db.Column(db.String, nullable=False)
	year = db.Column(db.Integer, nullable=False)
	comments = db.relationship('Comment', backref='post', lazy='dynamic')

	def __init__(self, isbn=None, title=None, author=None, year=None):
		self.isbn = isbn
		self.title = title
		self.author = author
		self.year = year

	def __repr__(self):
		return '<Book: {0}>'.format(self.title)


class Rating(db.Model):
	__tablename__ = 'ratings'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	score = db.Column(db.Integer, nullable=False)

	# Define relationship to user
	user = db.relationship("User", backref=db.backref("ratings", order_by=id))
	# Define relationship to Book
	book = db.relationship("Books", backref=db.backref("ratings", order_by=id))

	def __repr__(self):
		return "<Rating: id={0} book_id={1} user_id={2} score={3}>".format(
			self.id, self.book_id, self.user_id, self.score)


class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	disabled = db.Column(db.Boolean)
	comment_author = db.Column(db.Integer, db.ForeignKey('users.id'))
	book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

	def __init__(
		self,
		body=None,
		timestamp=None, disabled=None, author_id=None, book_id=None):

		self.body = body
		self.timestamp = timestamp
		self.disabled = disabled
		self.author_id = author_id
		self.book_id = book_id

	def __repr__(self):
		return '<Comment: {0} \n by User:{1}>'.format(
			self.body, self.author_id.username)