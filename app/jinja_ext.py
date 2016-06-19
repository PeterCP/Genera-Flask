import re

from wtforms.compat import iteritems, text_type
try:
	from html import escape
except ImportError:
	from cgi import escape

from app import helpers



def html_params(**kwargs):
	"""
	Generate HTML attribute syntax from inputted keyword arguments.

	The output value is sorted by the passed keys, to provide consistent output
	each time this function is called with the same parameters. Because of the
	frequent use of the normally reserved keywords `class` and `for`, suffixing
	these with an underscore will allow them to be used.

	In order to facilitate the use of ``data-`` attributes, the first underscore
	behind the ``data``-element is replaced with a hyphen.

	>>> html_params(data_any_attribute='something')
	'data-any_attribute="something"'

	In addition, the values ``True`` and ``False`` are special:
	  * ``attr=True`` generates the HTML compact output of a boolean attribute,
	    e.g. ``checked=True`` will generate simply ``checked``
	  * ``attr=False`` will be ignored and generate no output.

	>>> html_params(name='text1', id='f', class_='text')
	'class="text" id="f" name="text1"'
	>>> html_params(checked=True, readonly=False, name="text1", abc="hello")
	'abc="hello" checked name="text1"'
	"""
	params = []
	for k, v in sorted(iteritems(kwargs)):
		if k in ('class_', 'class__', 'for_'):
			k = k[:-1]
		else:
			k = k.replace('_', '-')

		if v is True:
			params.append(k)
		elif v is False:
			pass
		else:
			params.append('%s="%s"' % (text_type(k), escape(text_type(v), quote=True)))

	return ' '.join(params)



def extend_app(app):
	# Template filter to format dates.
	@app.template_filter('format_date')
	def _jinja2_filter_datetime(date, format='%b %d, %Y'):
		try:
			return date.strftime(format)
		except ValueError:
			return date

	# Inject current_user into each context.
	@app.context_processor
	def inject_current_user():
		return dict(current_user=helpers.current_user())

	# Add globals
	app.jinja_env.globals['html_params'] = html_params
	app.jinja_env.globals['event_image_url'] = helpers.get_event_image_url
	app.jinja_env.globals['re'] = re
