from collections import OrderedDict

from flask import abort
from flask_sqlalchemy import SQLAlchemy

from app import app


# Register Flask-SQLAlchemy instance
db = SQLAlchemy(app)



class BaseModel(db.Model):

	__abstract__ = True

	# Columns to be hidden from view
	__hidden_columns__ = ['created_at', 'updated_at']

	### Column related methods

	@classmethod
	def columns(cls):
		return [col for col in cls.__mapper__.columns
			if col.key not in cls.__hidden_columns__]

	@classmethod
	def column_keys(cls):
		return [col.key for col in cls.columns()]

	### Query related methods

	@classmethod
	def all(cls):
		return cls.query.all()

	@classmethod
	def count(cls):
		return cls.query.count()

	@classmethod
	def first(cls):
		return cls.query.first()

	@classmethod
	def filter(cls, *args, **kwargs):
		return cls.query.filter(*args, **kwargs)

	@classmethod
	def filter_by(cls, **kwargs):
		return cls.query.filter_by(**kwargs)

	@classmethod
	def get(cls, id):
		return cls.query.get(id)

	@classmethod
	def get_by(cls, **kwargs):
		return cls.filter_by(**kwargs).first()

	@classmethod
	def get_or_404(cls, id):
		rv = cls.get(id)
		if rv is None:
			abort(404)
		return rv

	@classmethod
	def get_or_create(cls, **kwargs):
		r = cls.get_by(**kwargs)
		if not r:
			r = cls.create(**kwargs)
		return r

	@classmethod
	def create(cls, **kwargs):
		r = cls(**kwargs)
		return r

	def __init__(self, *args, **kwargs):
		db.Model.__init__(self, *args, **kwargs)
		if hasattr(self, 'on_create'):
			self.on_create()

	def save(self, commit=False):
		db.session.add(self)
		if hasattr(self, 'on_save'):
			self.on_save()
		if commit:
			db.session.commit()

	def delete(self, commit=False):
		if hasattr(self, 'on_delete'):
			self.on_delete()
		db.session.delete(self)
		if commit:
			db.session.commit()

	def update(self, **kwargs):
		for key, value in kwargs.iteritems():
			self[key] = value
		if hasattr(self, 'on_update'):
			self.on_update()
		return self # Allow method chaining

	def filter_string(self):
		return self.__str__()

	def _asdict(self): # Implemented for simplejson
		return OrderedDict(self)

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)

	def __iter__(self):
		for col in self.columns():
			yield col.key, getattr(self, col.key)

	def __getitem__(self, key):
		if not hasattr(self, key):
			raise AttributeError("'%s' has no attribute '%s'" %
				(self.__class__.__name__, key))
		return getattr(self, key)

	def __setitem__(self, key, value):
		if not hasattr(self, key):
			raise AttributeError("'%s' has no attribute '%s'" %
				(self.__class__.__name__, key))
		return setattr(self, key, value)

	def __repr__(self):
		values = ', '.join("%s=%r" % iter(self))
		return "%s(%s)" % (self.__class__.__name__, values)



from users import User
from auth import AuthRole, AuthPermission
from events import Event, EventCategory, EventEnrollment
