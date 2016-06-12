from flask_sqlalchemy import SQLAlchemy

from app import app


# Register Flask-SQLAlchemy instance
db = SQLAlchemy(app)



class BaseModel(db.Model):

	__abstract__ = True

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def update(self, **data):
		for key, value in data.iteritems():
			if hasattr(self, key):
				setattr(self, key, value)

	def __iter__(self):
		values = vars(self)
		for attr in self.__mapper__.columns.keys():
			if attr in values:
				yield attr, values[attr]



from users import User
from auth import AuthRole, AuthPermission
from events import Event, EventCategory
