import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, and_, or_, func, desc
from models import Base, Hotel, Room, Booking
from schemas import BookingRequest, BookingCreate
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

@app.post("/bookings")
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # Start transaction implicitly by using the session
    
    # Lock the room row to prevent race conditions
    # We query the room and lock it. If it doesn't exist, 404.
    room = db.query(Room).filter(Room.id == booking.room_id).with_for_update().first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Check for overlaps
    # Overlap condition: (StartA < EndB) and (EndA > StartB)
    # Here A is existing booking, B is new booking
    overlap = db.query(Booking).filter(
        Booking.room_id == booking.room_id,
        Booking.check_in < booking.check_out,
        Booking.check_out > booking.check_in
    ).first()

    if overlap:
        raise HTTPException(status_code=409, detail="Room is already booked for these dates")

    # Calculate price
    total_price = 0.0
    current_date = booking.check_in
    while current_date < booking.check_out:
        # 5 = Saturday, 6 = Sunday
        if current_date.weekday() >= 5:
            total_price += float(room.base_price) * 1.2
        else:
            total_price += float(room.base_price)
        current_date += timedelta(days=1)

    # Create booking
    new_booking = Booking(
        room_id=booking.room_id,
        customer_email=booking.customer_email,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_price=total_price
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking

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

@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    """
    Veritabanındaki rezervasyonları analiz edip özet rapor sunar.
    SQL Aggregation (Toplama) fonksiyonlarını kullanır.
    """
    
    # 1. Toplam Ciro (Sum)
    # SQL: SELECT SUM(total_price) FROM bookings;
    total_revenue = db.query(func.sum(Booking.total_price)).scalar() or 0.0
    
    # 2. Toplam Rezervasyon Sayısı (Count)
    # SQL: SELECT COUNT(id) FROM bookings;
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0
    
    # 3. Oda Tipine Göre Doluluk (Group By)
    # SQL: SELECT room_type, COUNT(*) FROM rooms JOIN bookings ... GROUP BY room_type;
    occupancy_by_type = db.query(
        Room.room_type,
        func.count(Booking.id).label("count")
    ).join(Booking).group_by(Room.room_type).all()
    
    # 4. En Popüler Oda (Sıralama)
    most_popular = "Yok"
    if occupancy_by_type:
        # Python tarafında sıralama yapıyoruz (Matematiksel max bulma)
        # Listeyi 'count' değerine göre tersten sırala ve ilkini al
        top_room = sorted(occupancy_by_type, key=lambda x: x[1], reverse=True)[0]
        most_popular = f"{top_room[0]} ({top_room[1]} rezervasyon)"

    # Sonucu JSON olarak dön
    return {
        "total_revenue": round(total_revenue, 2),
        "total_bookings": total_bookings,
        "average_price": round(total_revenue / total_bookings, 2) if total_bookings > 0 else 0,
        "most_popular_room_type": most_popular,
        "breakdown": [
            {"type": r[0], "count": r[1]} for r in occupancy_by_type
        ]
    }