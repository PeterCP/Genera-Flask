import os

from flask import current_app, session, url_for
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
	savedir = 'images/events/%s' % event.id
	filename = 'main_image%s' % ext
	path = os.path.join(savedir, filename)
	storagedir = current_app.config.get('STORAGE_FOLDER')
	try:
		image.save(os.path.join(storagedir, path))
	except(IOError):
		os.mkdir(os.path.join(storagedir, savedir))
		image.save(os.path.join(storagedir, path))
	return path

def delete_event_image(event):
	if not event.image_path:
		return False
	else:
		storagedir = current_app.config.get('STORAGE_FOLDER')
		try:
			os.remove(os.path.join(storagedir, event.image_path))
			image_dir = os.path.join(storagedir, os.path.dirname(event.image_path))
			if len(os.listdir(image_dir)) == 0:
				os.removedirs(image_dir)
			event.image_path = None
			return True
		except(OSError) as e:
			return False

def get_event_image_url(event):
	if event.image_path:
		return url_for('storage', filename=event.image_path)
	return url_for('static', filename='images/events/placeholder/main_image.jpg')
