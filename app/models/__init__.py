from flask_sqlalchemy import SQLAlchemy

from app import app


# Register Flask-SQLAlchemy instance
db = SQLAlchemy(app)



class Comparable:
	
	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)



from users import User
from auth import AuthRole, AuthPermission
from events import Event, EventCategory

