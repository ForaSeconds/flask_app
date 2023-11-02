from app import app, db
from flask import request, jsonify, render_template, redirect, url_for, session, flash, typing as ft
from app.main.views import login_required, api_authentication_required
from app.event.models import Event, EventUser
from app.event.forms import EventForm
from app.user.models import User
from flask.views import View, MethodView


@login_required
@app.route("/events", methods=['GET'])
def get_events():
    if request.method == "GET":
        events = Event.query.all()
        my_list_events = {
            "events": events,
        }
        return render_template("event/list.html", **my_list_events)


@login_required
@app.route("/events/create", methods=['GET', 'POST'])
def create_new_events():
    form = EventForm()

    if form.validate_on_submit():
        user_id = session.get("user_id")
        event = Event(created_by=user_id)

        form.populate_obj(event)
        db.session.add(event)
        db.session.commit()
        flash("Event created successfully", "success")
        return redirect(url_for('get_events_id', id=event.id))
    else:
        flash("Unauthorized", "error")

    return render_template("event/create.html", form=form)


@login_required
@app.route("/events/<int:id>/update", methods=['GET', 'POST'])
def update_event_id(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash("Event updated successfully", "success")
        return redirect(url_for('get_events_id', id=event.id))
    elif request.method == 'POST':
        flash("Validation failed. Please check your input.", "error")

    return render_template("event/update.html", form=form, event=event)


@login_required
@app.route("/events/<int:id>", methods=['GET'])
def get_events_id(id):
    if request.method == "GET":
        event = Event.query.get(id)
        if event is None:
            return "No Event", 404
        elif event:
            return render_template("event/detail.html", event=event)


@login_required
@app.route("/events/<int:id>/users", methods=['GET'])
def get_events_id_users(id):
    if request.method == "GET":
        event = Event.query.get(id)
        if not event:
            return "No events", 404

        events_user = EventUser.query.filter_by(event_id=id).all()
        user_info = []
        for user_event in events_user:
            user = User.query.get(user_event.user_id)
            user_info.append({
                "id": user_event.id,
                "username": user.username,
            })

        return render_template("event/users.html", event=event, users_info=user_info), 200


@api_authentication_required
@app.route("/api/events/", methods=["POST"])
def create_event():
    events = Event.query.all()
    event_list = []
    for event in events:
        event_data = {
            "id": event.id,
            "title": event.title,
            'description': event.description,
            'begin_at': event.begin_at.strftime('%Y-%m-%d'),
            'end_at': event.end_at.strftime('%Y-%m-%d'),
            'max_users': event.max_users,
            'is_active': event.is_active,
            'created_by': event.created_by
        }
        event_list.append(event_data)

    return jsonify(event_list), 201


@api_authentication_required(allowed_usernames=["root", "admin", "user"])
@app.route("/api/events/<int:id>/", methods=["PATCH"])
def update_event_endpoint(id):
    data = request.get_json()
    return jsonify(data), 200


@app.route("/api/events/<int:id>/", methods=["DELETE"])
def delete_event(id):
    return "", 204


@api_authentication_required
@app.route("/api/events/<int:id>/users", methods=['GET'])
def get_events_id_users_api(id):
    if request.method == "GET":
        event = Event.query.get(id)
        if not event:
            return jsonify(message="Event not found"), 404

        events_user = EventUser.query.filter_by(event_id=id).all()
        user_info = []
        for user_event in events_user:
            user = User.query.get(user_event.user_id)
            user_info.append({
                "id": user_event.id,
                "username": user.username,
            })

        return jsonify(users=user_info)


@api_authentication_required
@app.route('/api/users/', methods=['GET'])
def get_users():
    response = []
    return jsonify(response), 200


@app.route("/api/users/", methods=["POST"])
@api_authentication_required(allowed_usernames=["root", "admin", "user"])
def create_users():
    users = User.query.all()
    users_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        }
        users_list.append(user_data)
    return jsonify(users_list), 201


@app.route('/api/users/<int:id>/', methods=['PATCH'])
@api_authentication_required(allowed_usernames=["root", "admin", "user"])
def update_user(id):
    data = request.get_json()
    return jsonify(data), 200


@api_authentication_required
@app.route('/api/users/<int:id>/', methods=['DELETE'])
def delete_user(id):
    return "", 204


class ListView(View):
    def __init__(self, model):
        self.model = model

    def dispatch_request(self) -> ft.ResponseReturnValue:
        objects = self.model.query.all()
        return render_template("class/list.html", objects=objects)


app.add_url_rule(
    "/class/users", view_func=ListView.as_view('user-list', User)
)

app.add_url_rule(
    "/class/events", view_func=ListView.as_view('event-list', Event)
)


class ListViewDetails(View):
    def __init__(self, model):
        self.model = model

    def dispatch_request(self, id) -> ft.ResponseReturnValue:
        item = self.model.query.get(id)
        return render_template("class/detail.html", item=item)


app.add_url_rule("/class/users/<int:id>",
                 view_func=ListViewDetails.as_view("user-detail", User))
app.add_url_rule("/class/events/<int:id>",
                 view_func=ListViewDetails.as_view("event-detail", Event))
