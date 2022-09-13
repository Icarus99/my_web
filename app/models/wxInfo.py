from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from app.models.base import Base
from flask_login import UserMixin

class wxInfo(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    openid = Column(String(48), nullable=False)
    member_id = Column(Integer, nullable=False)
    updated_time = Column(DateTime, nullable=False)
    created_time = Column(DateTime, nullable=False)

