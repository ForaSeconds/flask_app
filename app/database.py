from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.user import models
from app.event import models