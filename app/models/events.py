import bbcode

from app.models import db



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
		return ('<Event id={event.id}, title=\'{event.title}\', '
			'points=\'{event.points}\'>').format(event=self)

	@property
	def rendered_text(self):
		return bbcode.render_html(self.text)



class EventCategory(db.Model):

	__tablename__ = 'event_categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	events = db.relationship('Event', backref='category')

	def __repr__(self):
		return '<EventCategory id={ec.id}, name=\'{ec.name}\'>'.format(ec=self)

