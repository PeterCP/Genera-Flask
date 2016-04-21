from datetime import datetime

from flask import (Blueprint, request, render_template, redirect, url_for, abort)

from app import helpers, app
from app.forms import CreateEventForm, EventAttendanceForm
from app.models import User, Event


events_blueprint = Blueprint('events', __name__, url_prefix='/events')


@events_blueprint.route('/', methods=['GET'])
def view_all():
	events = Event.query.all()
	return render_template('events/index.html.j2', events=events)


@events_blueprint.route('/<int:evt_id>/', methods=['GET'])
def view_single(evt_id):
	event = Event.query.get(evt_id)
	
	if not event:
		return abort(404)
	
	return render_template('events/view_single.html.j2', event=event,
		can_edit=helpers.current_user() == event.publisher)


@events_blueprint.route('/<int:evt_id>/attendance', methods=['GET', 'POST'])
def attendance(evt_id):
	user = helpers.current_user()
	event = Event.query.get(evt_id)
	
	if not user or not event or user != event.publisher:
		return abort(403)

	form = EventAttendanceForm(data={
		'event_id': event.id,
		'user_id': user.id,
		'attendant_ids': [u.id for u in event.attendants]
		})
	
	if form.validate_on_submit():
		new_attendance_list = [User.query.get(user_id) for user_id in form.attendant_ids.data]
		event.attendants = new_attendance_list
		event.save()
		# for user_id in form.attendant_ids:
		# 	new_attendance_list.append(User.query.get(user_id))
		return redirect(url_for('events.view_single', evt_id=evt_id))

	return render_template('events/attendance.html.j2', form=form)


@events_blueprint.route('/new', methods=['GET', 'POST'])
def new():
	form = CreateEventForm()
	user = helpers.current_user()
	if not user:
		return abort(403)

	if form.validate_on_submit():
		data = dict(form.data)
		event = Event(**data)
		event.publisher = user
		event.published_on = datetime.now()
		event.save()
		return redirect(url_for('events.view_single', evt_id=event.id))

	return render_template('events/new.html.j2', form=form, request=request)


# @events_blueprint.route('/<int:evt_id>/settings', methods=['GET', 'POST'])
# def settings(evt_id):
# 	event = Event.query.get(evt_id)

# 	if not event:
# 		return abort(404)
# 	elif event.publisher != helpers.current_user():
# 		return abort(403)

# 	return render_template('events/settings.html.j2')

