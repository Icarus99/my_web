from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from app.models.base import Base
from flask_login import UserMixin

class partnerRequests(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    adder = Column(Integer, nullable=False)
    partner = Column(Integer, nullable=False)
    created_time = Column(DateTime, nullable=False)
    status = Column(String(32), default="pending")

