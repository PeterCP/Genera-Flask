import os

from flask import session, url_for
from werkzeug import secure_filename

from app.models import User


def current_user():
	user_id = session.get('user_id', None)
	if user_id:
		user = User.query.get(user_id)
		if user:
			return user
	return None

def login(user):
	session['user_id'] = user.id

def logout():
	session.pop('user_id')

def save_event_image(event, image):
	if not event or not image:
		raise RuntimeError('Must supply both an event and an image')
	name, ext = os.path.splitext(secure_filename(image.filename))
	path = 'images/events/{event.id}/main_image{ext}' \
		.format(event=event, ext=ext)
	try:
		image.save(path)
	except(IOError):
		os.mkdir('images/events/{event.id}'.format(event=event))
		image.save(path)
	return path

def delete_event_image(event):
	if not event.image_path:
		return False
	else:
		os.remove(event.image_path)
		image_dir = os.path.dirname(event.iamge_path)
		if len(os.listdir(image_dir)) == 0:
			os.removedirs(image_dir)
		event.image_path = None
		return True

def get_event_image_url(event):
	filename = event.image_path or 'images/events/placeholder/main_image.jpg'
	return url_for('storage', filename=filename)
