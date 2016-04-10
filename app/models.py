from datetime import datetime, timedelta

import bbcode

from app import db, bcrypt


# Relationship table used by User and Event for the
# event attendance relationship.
event_attendance = db.Table('event_attendance',
	db.Column('user', db.Integer, db.ForeignKey('users.id')),
	db.Column('event', db.Integer, db.ForeignKey('events.id')))



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
	role = db.Column(db.Integer, db.ForeignKey('user_roles.id'))

	# Relationship fields.
	events_attended = db.relationship('Event',
		secondary=event_attendance,
		backref=db.backref('users'))
	events_published = db.relationship('Event')

	def __init__(self, name, email, password, role):
		self.name = name
		self.email = email
		self.pw_hash = bcrypt.generate_password_hash(password)
		self.role = role

	def __repr__(self):
		return '<User name={user.name}, '\
			'email={user.email}, '\
			'role={user.role}>'\
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



class UserRole(db.Model):

	__tablename__ = 'user_roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	users = db.relationship('User')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<UserRole name={ur.name}>'.format(ur=self)

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)



class Event(db.Model):

	__tablename__ = 'events'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	text = db.Column(db.String)
	points = db.Column(db.Integer)
	date = db.Column(db.DateTime)
	category = db.Column(db.Integer, db.ForeignKey('event_categories.id'))
	publisher = db.Column(db.Integer, db.ForeignKey('users.id'))
	published_on = db.Column(db.DateTime)
	attendees = db.relationship('User',
		secondary=event_attendance,
		backref=db.backref('events'))

	def __init__(self, title, text, points, date, category, publisher):
		self.title = title
		self.text = text
		self.points = points
		self.date = date
		self.category = category
		self.publisher = publisher
		self.published_on = datetime.now()

	def __repr__(self):
		return '<Event title={event.title}, points={event.points}, '\
			'date={event.date}, publisher={event.publisher}>'\
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
	events = db.relationship('Event')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<EventCategory name={ec.name}>'.format(ec=self)

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)
