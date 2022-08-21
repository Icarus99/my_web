from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class recipe(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    summary = Column(String(1000))
    image = Column(String(50))

