from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    rating = Column(Float, nullable=False)
    likes = Column(Integer, default=0)

    movie_id = Column(Integer, ForeignKey("SMA.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'movie_id', name='_user_movie_uc'),)

    movie = relationship("SMAModel", back_populates="reviews")
    author = relationship("UserModel", back_populates="reviews")