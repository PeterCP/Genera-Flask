import sqlalchemy as sa

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import _BoundDeclarativeMeta as BDA

from app import app
from app.models import db

# @MigrateCommand.option('-c', '--clear', dest='clear', default=False,
	# help='Clear all tables before running seeds.')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', Server(port=8000))
manager.add_command('db', MigrateCommand)

@manager.command
def createroles(verbose=False):
	"""Create auth roles as defined in config.auth"""
	from config.auth import roles
	from scripts.auth import create_or_update_role
	for role in roles:
		create_or_update_role(role)
		if verbose:
			print role['key']
	        for perm in role['permissions']:
	            print '  %s' % perm

# @manager.command
def cleardb():
	models = [m for m in db.Model._decl_class_registry.values()
		if isinstance(m, BDA)]

	passes = 0
	while passes < 3:
		finished = True
		for model in models:
			# try:
			deleted = model.query.delete()
				# print 'Deleted from %s: %s' %(model.__tablename__, deleted)
			# except sa.exc.IntegrityError:
				# print 'Error'
				# finished = False
		db.session.commit()

		if finished:
			break

if __name__ == '__main__':
	manager.run()
