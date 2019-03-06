from views import app, login_manager
from models import AnonymousUser
from _config import SECRET_KEY

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
	return None

app.run(debug=True)