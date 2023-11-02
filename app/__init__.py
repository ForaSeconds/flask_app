from dotenv import load_dotenv
from flask_migrate import Migrate
from flask import Flask, render_template
import werkzeug
from app.database import db

load_dotenv()

app: Flask = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)
migrate = Migrate(app, db)


@app.errorhandler(werkzeug.exceptions.NotFound)
def error_404(exc):
    return render_template("exception/404.html", exc=exc)


@app.errorhandler(werkzeug.exceptions.HTTPException)
def error_505(exc):
    return render_template("exception/505.html", exc=exc)
