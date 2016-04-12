from flask import Blueprint, render_template, abort

from app import helpers
from app.models import Event


events_blueprint = Blueprint('events', __name__, url_prefix='/events')


@events_blueprint.route('/', methods=['GET'])
def view_all():
	return render_template('events/index.html')


@events_blueprint.route('/<int:evt_id>/', methods=['GET'])
def view_single(evt_id):
	event = Event.query.get(evt_id)
	
	if not event:
		return abort(404)
	
	return render_template('events/view_single.html')



# @events_blueprint.route('/<int:evt_id>/settings', methods=['GET', 'POST'])
# def settings(evt_id):
# 	event = Event.query.get(evt_id)

# 	if not event:
# 		return abort(404)
# 	elif event.publisher != helpers.current_user():
# 		return abort(403)

# 	return render_template('events/settings.html')

