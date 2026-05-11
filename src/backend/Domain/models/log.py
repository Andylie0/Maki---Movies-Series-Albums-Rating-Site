from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    group_id = Column(String(50), nullable=False)
    action = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)