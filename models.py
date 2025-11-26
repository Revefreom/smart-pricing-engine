from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, DECIMAL, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# Base yapısını kuruyoruz
Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(String)
    stars = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # İlişki: Bir otelin birden fazla odası olabilir
    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Hotel(name='{self.name}', stars={self.stars})>"

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id', ondelete='CASCADE'), nullable=False)
    room_type = Column(String(50), nullable=False)
    base_price = Column(DECIMAL(10,2), nullable=False)

    # İlişki: Her oda bir otele aittir
    hotel = relationship("Hotel", back_populates="rooms")

    def __repr__(self):
        return f"<Room(type='{self.room_type}', price={self.base_price})>"
