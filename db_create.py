from views import db
from models import User

db.create_all()

db.session.add(
	User("admin","ad@min.com","admin","admin"))

db.session.commit()