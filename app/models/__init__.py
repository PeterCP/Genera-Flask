from flask_sqlalchemy import SQLAlchemy

from app import app


# Register Flask-SQLAlchemy instance
db = SQLAlchemy(app)



class ModelMixin:
	
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

	def update(self, data):
		for key, value in data:
			if hasattr(self, key):
				setattr(self, key, value)



from users import User
from auth import AuthRole, AuthPermission
from events import Event, EventCategory

