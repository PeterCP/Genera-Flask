from app import app

@app.cli.command('initdb')
def initdb():
	from app import models
	models.db.create_all()
	print 'Database initialized successfully!'

@app.cli.command('run')
def run():
	app.run()

