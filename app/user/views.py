from app import app
from flask import render_template, redirect, url_for, request
from app.event.views import login_required
from app.database import db
from app.user.models import User
from app.user.forms import UserForm
from werkzeug.security import generate_password_hash


@app.route("/users", methods=['GET'])
@login_required
def users_list():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    my_list_content = {
        "users": users,
    }
    return render_template("user/list.html", **my_list_content)


@app.route("/register", methods=['GET', 'POST'])
def registration_method():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        existing_user = User.query.filter_by(username=new_user.username).first()
        if existing_user:
            return render_template("user/register.html",
                                   form=form, error="User with that username already exists")

        new_user.password = generate_password_hash(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('method_login'))

    return render_template("user/register.html", form=form)
