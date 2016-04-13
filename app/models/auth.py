from app.models import db
from app.models.relationship_tables import role_permission_rel



class AuthRole(db.Model, Comparable):

	__tablename__ = 'auth_roles'

	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(255), unique=True, nullable=False)
	description = db.Column(db.String(255))
	""" Backref AuthRole.users from User.roles """
	permissions = db.relationship('AuthPermission',
		secondary=role_permission_rel, backref='roles')

	def __repr__(self):
		return '<AuthRole id={ar.id}, key=\'{ar.key}\'>'.format(ar=self)



class AuthPermission(db.Model, Comparable):

	__tablename__ = 'auth_permissions'

	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(255), unique=True, nullable=False)
	description = db.Column(db.String(255))
	""" Backref AuthPermission.roles from AuthRole.permissions """

	def __repr__(self):
		return '<AuthPermission id={ap.id}, key=\'{ap.key}\'>'.format(ap=self)

