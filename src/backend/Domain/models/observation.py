from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from database import Base

class ObservationModel(Base):
    __tablename__ = "observation_list"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    reason = Column(String(500), nullable=False)
    severity = Column(String(50), default="Medium")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserModel", back_populates="observations")