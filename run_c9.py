from os import getenv

if __name__ == '__main__':
	host = getenv('IP', '0.0.0.0')
	port = int(getenv('PORT', 5000))
	app.run(host=host, port=port)
