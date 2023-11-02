from app import app
from flask import request, render_template, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.config import SECRET_KEY, password
import jwt
import datetime
from app.user.models import User

password_hush = generate_password_hash(password)
ALLOWED_USERS = ["root", "admin", "user"]


@app.route("/login", methods=["GET", "POST"])
def method_login():
    if request.method == "GET":
        return render_template("main/login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password_user = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if check_password_hash(password_hush, password_user):
            session["user_id"] = user.id
            session["username"] = username
            return redirect("/events")
        else:
            return "Unauthorized", 401


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("method_login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/logout", methods=["GET"])
def method_logout():
    if "username" not in session:
        return redirect(url_for("method_login"))
    elif "username" in session:
        del session["username"]
        return redirect(url_for("method_login"))


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password_user = data.get("password")
    if username in ALLOWED_USERS and check_password_hash(password_hush, password_user):
        GENERATED_TOKEN = generate_jwt_token(username)
        return jsonify({"token": GENERATED_TOKEN})
    return jsonify({"message": "Unauthorized"}), 401


def generate_jwt_token(username):
    expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
    load_info = {"username": username, "exp": expiration}
    token = jwt.encode(load_info, SECRET_KEY, algorithm="HS256")
    return token


def api_authentication_required(allowed_usernames=None):
    if allowed_usernames is None:
        allowed_usernames = ALLOWED_USERS

    def decorator(func):
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authentication")

            if not token:
                return jsonify({"message": "Unauthorized"}), 401

            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = data.get("username")
            expiration = data.get("exp")

            if username in allowed_usernames and expiration >= datetime.datetime.now():
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "Unauthorized"}), 401

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator
