from datetime import datetime

import bbcode

from app.models import db, BaseModel



class Event(BaseModel):

	__tablename__ = 'events'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	body = db.Column(db.Text, nullable=False)
	points = db.Column(db.Integer, nullable=False)
	date = db.Column(db.Date, nullable=False)
	time = db.Column(db.Time, nullable=False)
	location_name = db.Column(db.String(255))
	latitude = db.Column(db.Numeric(scale=16))
	longitude = db.Column(db.Numeric(scale=16))
	price = db.Column(db.Numeric(precision=2))
	max_attendants = db.Column(db.Integer)
	image_path = db.Column(db.String(255))
	category_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'),
		nullable=False)
	publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'),
		nullable=False)
	published_on = db.Column(db.DateTime, nullable=False,
		default=datetime.now())
	""" Backref Event.publisher from User.events_published """
	""" Backref Event.category from EventCategory.events """
	""" Backref Event.attendants from User.events_attended """
	""" Backref Event.enrollments from EventEnrollment.event """

	def __repr__(self):
		return ('<Event id={event.id}, title=\'{event.title}\', '
			'points=\'{event.points}\'>').format(event=self)

	@property
	def rendered_body(self):
		return bbcode.render_html(self.body)

	@property
	def date_time(self):
		return datetime.combine(self.date, self.time)

	@date_time.setter
	def date_time(self, value):
		self.date = value.date()
		self.time = value.time()

	def on_delete(self):
		from app.helpers import delete_event_image
		delete_event_image(self)



class EventCategory(BaseModel):

	__tablename__ = 'event_categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	events = db.relationship('Event', backref='category')

	def __repr__(self):
		return '<EventCategory id={ec.id}, name=\'{ec.name}\'>'.format(ec=self)



class EventEnrollment(BaseModel):

	__tablename__ = 'event_enrollments'

	id = db.Column(db.Integer, primary_key=True)
	event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	reason = db.Column(db.Text, nullable=True)

	event = db.relationship('Event', backref='enrollments')
	user = db.relationship('User', backref='event_enrollments')

	def __repr__(self):
		return ('<EventEnrollment id={ee.id}, user_id={ee.user_id}, '
			'event_id={ee.event_id}>').format(ee=self)
