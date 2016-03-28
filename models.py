from datetime import datetime
import bcrypt, bbcode
from genera import db


# Relationship table used by User and Event for the
# event attendance relationship.
event_attendance = db.Table('event_attendance',
	db.Column('user', db.Integer, db.ForeignKey('users.id')),
	db.Column('event', db.Integer, db.ForeignKey('events.id')))



class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	pw_hash = db.Column(db.String(), nullable=False)
	role = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
	events_attended = db.relationship('Event',
		secondary=event_attendance,
		backref=db.backref('users'))
	events_published = db.relationship('Event')

	def __init__(self, name, email, password, role):
		self.name = name
		self.email = email
		self.pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
		self.role = role

	def __repr__(self):
		return '<User name={user.name}, '\
			'email={user.email}, '\
			'role={user.role}>'\
			.format(user=self)

	def __eq__(self, other):
		if type(self) is type(other) and self.id == other.id:
			return True
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	@property
	def score(self):
		score = 0
		for event in self.events_attended:
			score += event.points
		return score

	def authenticate(self, password):
		"""
		Returns True if the user introduced the correct
		password and False otherwise.
		"""
		return bcrypt.hashpw(password, self.pw_hash) == self.pw_hash

	def change_password(self, old_pw, new_pw):
		"""
		Attempts to change the old password for a new one.
		Returns True if successful and False otherwise.
		"""
		if self.authenticate(old_pw):
			self.pw_hash = bcrypt.hashpw(new_pw, bcrypt.gensalt())
			return True
		else:
			return False



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
		if type(self) is type(other) and self.id == other.id:
			return True
		else:
			return False

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
		if type(self) is type(other) and self.id == other.id:
			return True
		else:
			return False

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
		if type(self) is type(other) and self.id == other.id:
			return True
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)
