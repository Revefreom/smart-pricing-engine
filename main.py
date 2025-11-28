import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from models import Base, Hotel, Room
from schemas import BookingRequest
from datetime import timedelta

# 1. Ortam değişkenlerini yükle
load_dotenv()

# 2. URL'i gizli dosyadan çek
DATABASE_URL = os.getenv("DATABASE_URL")


# Engine ve SessionLocal oluşturma
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı tablolarını oluştur (Eğer yoksa)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Otel Fiyatlandırma API'sine Hoş Geldiniz"}

@app.get("/hotels")
def get_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    return hotels

@app.post("/calculate-price")
def calculate_price(booking: BookingRequest, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    total_price = 0.0
    weekend_days = 0
    weekday_days = 0
    
    current_date = booking.check_in
    while current_date < booking.check_out:
        # 5 = Saturday, 6 = Sunday
        if current_date.weekday() >= 5:
            total_price += float(room.base_price) * 1.2
            weekend_days += 1
        else:
            total_price += float(room.base_price)
            weekday_days += 1
        
        current_date += timedelta(days=1)
    
    return {
        "total_price": total_price,
        "breakdown": f"Hafta içi: {weekday_days} gün, Hafta sonu: {weekend_days} gün"
    }
