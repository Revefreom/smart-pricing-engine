from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Hotel, Room

# Bağlantı
DATABASE_URL = "postgresql://admin:sifre123@localhost:5432/otel_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def veri_ekle():
    # 1. Yeni bir Otel Nesnesi oluştur (Henüz DB'de değil, RAM'de)
    yeni_otel = Hotel(name="Python Palas", address="Kod Vadisi", stars=5)
    
    # 2. Otele Oda Nesneleri ekle (Liste olarak)
    yeni_otel.rooms = [
        Room(room_type="Standart", base_price=1500.00),
        Room(room_type="King Suite", base_price=5000.00)
    ]

    # 3. Session'a ekle ve kaydet (Commit)
    try:
        session.add(yeni_otel)
        session.commit()
        print(f"✅ Başarılı! '{yeni_otel.name}' ve {len(yeni_otel.rooms)} odası veritabanına eklendi.")
    except Exception as e:
        session.rollback() # Hata olursa işlemi geri al
        print(f"❌ Hata: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    veri_ekle()