from datetime import datetime, timedelta

import bbcode

from app import db, bcrypt


# Relationship table used by User and Event for the
# event attendance relationship.
user_event_rel = db.Table('user_event_rel',
	db.Column('user', db.Integer, db.ForeignKey('users.id')),
	db.Column('event', db.Integer, db.ForeignKey('events.id')))

user_role_rel = db.Table('user_role_rel',
	db.Column('user', db.Integer, db.ForeignKey('users.id')),
	db.Column('role', db.Integer, db.ForeignKey('auth_roles.id')))

# Relationship table used by AuthRole and AuthPermission
# for the authorization system.
role_permission_rel = db.Table('role_permission_rel',
	db.Column('role', db.Integer, db.ForeignKey('auth_roles.id')),
	db.Column('permission', db.Integer, db.ForeignKey('permissions.id')))



class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	
	# Used as login credentials.
	email = db.Column(db.String(255), unique=True, nullable=False)
	pw_hash = db.Column(db.String(), nullable=False)

	# Personal info fields.
	name = db.Column(db.String(255), nullable=False)
	# birth_date = db.Column(db.Date())

	# To be used for permission and auth module.
	roles = db.relationship('AuthRole',
		secondary=user_role_rel, backref='users')

	# Event related fields.
	events_attended = db.relationship('Event',
		secondary=user_event_rel, backref='attendants')

	events_published = db.relationship('Event', backref='publisher')

	def __init__(self, email, password, name):
		self.name = name
		self.email = email
		self.pw_hash = bcrypt.generate_password_hash(password)

	def __repr__(self):
		return '<User name={user.name}, '\
			'email={user.email}>'\
			.format(user=self)

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)

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
			self.pw_hash = bcrypt.generate_password_hash(password)
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



class AuthRole(db.Model):

	__tablename__ = 'auth_roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	""" Backref AuthRole.users from User.roles """
	permissions = db.relationship('AuthPermission',
		secondary=role_permission_rel, backref='roles')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<AuthRole name={ar.name}>'.format(ar=self)

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)



class AuthPermission(db.Model):

	__tablename__ = 'permissions'

	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.Integer, unique=True, nullable=False)
	description = db.Column(db.String(255))
	""" Backref AuthPermission.roles from AuthRole.permissions """



class Event(db.Model):

	__tablename__ = 'events'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	text = db.Column(db.String)
	points = db.Column(db.Integer)
	date = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'))
	publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	published_on = db.Column(db.DateTime)
	""" Backref Event.publisher from User.events_published """
	""" Backref Event.attendants from User.events_attended """
	""" Backref Event.category from EventCategory.events """

	def __repr__(self):
		return '<Event title={event.title}, points={event.points}>'\
			.format(event=self)

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)

	@property
	def rendered_text(self):
		return bbcode.render_html(self.text)



class EventCategory(db.Model):

	__tablename__ = 'event_categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	events = db.relationship('Event', backref='category')

	def __repr__(self):
		return '<EventCategory name={ec.name}>'.format(ec=self)

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)

