from flask_nav.elements import *
from app.helpers import current_user


def user_nav_item():
	user = current_user()
	if not user:
		return View('Login', 'login')
	else:
		return Subgroup(user.full_name,
			View('View profile', 'users.view_single', user_id=user.id),
			Separator(),
			View('Logout', 'logout'))

def navbar():
	return Navbar(
		View('Genera', 'index'),
		View('Home', 'index'),
		View('Users', 'users.view_all'),
		View('Events', 'events.view_all'),
		user_nav_item())
