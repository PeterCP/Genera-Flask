from datetime import datetime

from flask import (Blueprint, request, redirect, render_template, flash,
	url_for, abort)

from app import helpers, app
from app.forms import CreateEventForm, EventAttendanceForm, EventEnrollmentForm
from app.models import User, Event, EventCategory, EventEnrollment


events_blueprint = Blueprint('events', __name__, url_prefix='/events')


@events_blueprint.route('/', methods=['GET'])
def index():
	events = Event.all()
	return render_template('events/index.html.j2', events=events)


@events_blueprint.route('/<int:evt_id>/', methods=['GET'])
def show(evt_id):
	event = Event.get(evt_id)

	if not event:
		return abort(404)

	return render_template('events/show.html.j2', event=event,
		can_edit=helpers.current_user() == event.publisher)


@events_blueprint.route('/<int:evt_id>/attendance', methods=['GET', 'POST'])
def attendance(evt_id):
	user = helpers.current_user()
	event = Event.get(evt_id)

	if not event:
		return abort(404)
	if not user or user != event.publisher:
		return abort(403)

	form = EventAttendanceForm(data=dict(
		attendant_ids=[u.id for u in event.attendants]
	))
	form.attendant_ids.choices = [(user.id, user.full_name) for user in User.all()]

	if form.validate_on_submit():
		new_attendance_list = [User.get(user_id) for user_id in form.attendant_ids.data]
		event.attendants = new_attendance_list
		event.save(commit=True)
		flash('Event attendance registered successfully', category='success')
		return redirect(url_for('events.show', evt_id=evt_id))

	return render_template('events/attendance.html.j2', form=form, evt_id=event.id)


@events_blueprint.route('/<int:evt_id>/enroll', methods=['GET', 'POST'])
def enroll(evt_id):
	user = helpers.current_user()
	event = Event.get(evt_id)

	if not event:
		return abort(404)
	if not user:
		return abort(403)

	form = EventEnrollmentForm()

	if form.validate_on_submit():
		enrollment = EventEnrollment.filter_by(
			user_id=user.id,
			event_id=event.id
		).first()

		if enrollment:
			flash('You are already enrolled to this event', category='danger')
		else:
			new_enrollment = EventEnrollment(user_id=user.id, event_id=event.id,
				reason=form.reason.data)
			new_enrollment.save(commit=True)
			flash('You successfully enrolled to the event "%s"' % event.title, category='success')

		return redirect(url_for('events.show', evt_id=event.id))

	return render_template('events/enrollment.html.j2', event=event, form=form)

@events_blueprint.route('/create', methods=['GET', 'POST'])
def create():
	user = helpers.current_user()
	if not user:
		return abort(403)
	form = CreateEventForm()
	form.category_id.choices = [(ec.id, ec.name) for ec in EventCategory.all()]

	if form.validate_on_submit():
		data = dict(form.data)
		data.pop('image')
		event = Event(**data)
		event.publisher = user
		event.published_on = datetime.now()
		event.save()
		image = form.image.data
		if image:
			path = helpers.save_event_image(event, image)
			event.image_path = path
		event.save(commit=True)
		flash('Event creation successful!', category='success')
		return redirect(url_for('events.show', evt_id=event.id))

	return render_template('events/create.html.j2', form=form)


# @events_blueprint.route('/<int:evt_id>/settings', methods=['GET', 'POST'])
# def settings(evt_id):
# 	event = Event.query.get(evt_id)
#
# 	if not event:
# 		return abort(404)
# 	elif event.publisher != helpers.current_user():
# 		return abort(403)
#
# 	return render_template('events/settings.html.j2')
