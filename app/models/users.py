from datetime import datetime, timedelta

from app import bcrypt
from app.models import db, ModelMixin
from app.models.relationship_tables import user_event_rel, user_role_rel


class User(db.Model, ModelMixin):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	
	# Used as login credentials.
	email = db.Column(db.String(255), unique=True, nullable=False)
	pw_hash = db.Column(db.String(), nullable=False)

	# Personal info fields.
	first_name = db.Column(db.String(255), nullable=False)
	last_name = db.Column(db.String(255), nullable=False)
	gender = db.Column(db.Boolean(), nullable=False) # True='male', False='female'
	birth_date = db.Column(db.Date(), nullable=False)

	# To be used for permission and auth module.
	roles = db.relationship('AuthRole',
		secondary=user_role_rel, backref='users')

	# Event related fields.
	events_attended = db.relationship('Event',
		secondary=user_event_rel, backref='attendants')

	events_published = db.relationship('Event', backref='publisher')


	def __repr__(self):
		return ('<User id={user.id}, email=\'{user.email}\', '
			'name=\'{user.first_name} {user.last_name}\'>'
			).format(user=self)

	@property
	def full_name(self):
	    return '{} {}'.format(self.first_name, self.last_name)
	
	@property
	def password(self):
		return self.pw_hash

	@password.setter
	def password(self, new_pw):
		self.pw_hash = bcrypt.generate_password_hash(new_pw)

	@property
	def total_score(self):
		"""
		Returns the score a user has from all events attended.
		"""
		return self.get_score()

	@property
	def recent_score(self):
		"""
		Returns the score a user has from events attended in the last month.
		"""
		one_month_ago = datetime.now() - timedelta(days=30)
		return self.get_score(when=one_month_ago)

	def authenticate(self, password):
		"""
		Returns True if the user introduced the correct
		password and False otherwise.
		"""
		return bcrypt.check_password_hash(self.pw_hash, password)

	def change_password(self, old_pw, new_pw):
		"""
		Attempts to change the old password for a new one.
		Returns True if successful and False otherwise.
		"""
		if self.authenticate(old_pw):
			self.password = new_pw
			return True
		else:
			return False

	def get_score(self, when=None):
		"""
		Returns the user score from attending
		events newer than :param when:
		"""
		score = 0
		for event in self.events_attended:
			if when is None or event.date > when:
				score += event.points
		return score

	def has_permission(self, perm_key):
		"""
		Returns True if a permission with perm_key exists within user roles.
		"""
		for role in self.roles:
			for permission in role.permissions:
				if permission.key == perm_key:
					return True
		return False

