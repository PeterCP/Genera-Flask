import sqlalchemy as sa

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import _BoundDeclarativeMeta as BDA

from app import app
from app.models import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', Server(port=8000))
manager.add_command('db', MigrateCommand)

@manager.command
def createroles(verbose=False):
	"""Create auth roles as defined in config.auth"""

	from config.auth import roles
	from scripts.auth import create_or_update_role
	if verbose:
		print 'Current state of roles and permissions in database:'
	for role in roles:
		create_or_update_role(role)
		if verbose:
			print '  %s' % role['key']
			for perm in role['permissions']:
				print '    %s' % perm

@manager.command
def createcategories(verbose=False):
	"""Create event categories as defined in config.events"""

	from config.events import event_categories
	from scripts.events import create_or_update_event_category
	if verbose:
		print 'Current state of event categories in database:'
	for category in event_categories:
		create_or_update_event_category(category)
		if verbose:
			print '  %s' % category['name']

@MigrateCommand.command
def clear(verbose=False):
	"""Clear all entries in the database."""

	models = [m for m in db.Model._decl_class_registry.values()
		if isinstance(m, BDA)]

	for Model in models:
		deleted = 0
		for instance in Model.all():
			instance.delete()
			deleted += 1
		if verbose:
			print "Deleted from %s: %s" % (Model.__tablename__, deleted)

	db.session.commit()

@MigrateCommand.command
def seed(verbose=False):
	createroles(verbose=verbose)
	createcategories(verbose=verbose)


if __name__ == '__main__':
	manager.run()
