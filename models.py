from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	role = db.Column(db.String, default='user')

	def __init__(self, username=None, email=None, password=None, role=None):
		self.username = username
		self.email = email
		self.password = password
		self.role = role

	def __repr__(self):
		return '<User: {0}>'.format(self.username)

		