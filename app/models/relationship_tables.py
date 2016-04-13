from app.models import db


# Relationship table used by User and Event for the
# event attendance relationship.
user_event_rel = db.Table('user_event_rel',
	db.Column('user', db.Integer, db.ForeignKey('users.id')),
	db.Column('event', db.Integer, db.ForeignKey('events.id')))

# Relationship table used by User and AuthRole
# for the authorization system.
user_role_rel = db.Table('user_role_rel',
	db.Column('user', db.Integer, db.ForeignKey('users.id')),
	db.Column('role', db.Integer, db.ForeignKey('auth_roles.id')))

# Relationship table used by AuthRole and AuthPermission
# for the authorization system.
role_permission_rel = db.Table('role_permission_rel',
	db.Column('role', db.Integer, db.ForeignKey('auth_roles.id')),
	db.Column('permission', db.Integer, db.ForeignKey('auth_permissions.id')))