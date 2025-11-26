from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Hotel, Room

# Veritabanı bağlantı bilgileri
DATABASE_URL = "postgresql://admin:sifre123@localhost:5432/otel_db"

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
