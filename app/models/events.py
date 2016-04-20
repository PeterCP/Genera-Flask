from datetime import datetime

import bbcode

from app.models import db, Comparable



class Event(BaseModel):

	__tablename__ = 'events'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	text = db.Column(db.String, nullable=False)
	points = db.Column(db.Integer, nullable=False)
	date = db.Column(db.Date, nullable=False)
	time = db.Column(db.Time, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'),
		nullable=False)
	publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'),
		nullable=False)
	published_on = db.Column(db.DateTime, nullable=False,
		default=datetime.now())
	""" Backref Event.publisher from User.events_published """
	""" Backref Event.attendants from User.events_attended """
	""" Backref Event.category from EventCategory.events """

	def __repr__(self):
		return ('<Event id={event.id}, title=\'{event.title}\', '
			'points=\'{event.points}\'>').format(event=self)

	@property
	def rendered_text(self):
		return bbcode.render_html(self.text)

	@property
	def date_time(self):
		return datetime.combine(self.date, self.time)

	@date_time.setter
	def date_time(self, value):
		self.date = value.date()
		self.time = value.time()



class EventCategory(BaseModel):

	__tablename__ = 'event_categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	events = db.relationship('Event', backref='category')

	def __repr__(self):
		return '<EventCategory id={ec.id}, name=\'{ec.name}\'>'.format(ec=self)

