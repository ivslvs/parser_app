from flask_sqlalchemy import SQLAlchemy
from . import app

db = SQLAlchemy(app)


class Url(db.Model):
    """URL id"""
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())


db.create_all()
