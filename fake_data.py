import os
import random
from datetime import timedelta, date
from faker import Faker
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Room, Booking

# 1. Ayarlar
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

fake = Faker() # Yalan makinesi :)

def create_fake_bookings(num_bookings=100):
    print("🚀 Sahte veri üretimi başladı...")
    
    # Tüm odaları çek
    rooms = session.query(Room).all()
    if not rooms:
        print("❌ Hata: Önce 'seed_data.py' ile odaları oluşturmalısın!")
        return

    count = 0
    # İstediğimiz sayıya ulaşana kadar döngü kur
    while count < num_bookings:
        # Rastgele bir oda seç
        room = random.choice(rooms)
        
        # Rastgele bir tarih aralığı seç (Son 1 yıl içinden)
        # Bugün: 2025, Geçmişe dönük analiz yapacağımız için geçmiş tarih seçiyoruz
        start_date = fake.date_between(start_date='-1y', end_date='today')
        stay_duration = random.randint(1, 5) # 1 ile 5 gün arası kalsın
        end_date = start_date + timedelta(days=stay_duration)
        
        # Çakışma Kontrolü (Bizim API'deki mantığın aynısı)
        # Fake veri basarken veritabanı hatası almamak için Python tarafında kontrol ediyoruz
        overlap = session.query(Booking).filter(
            Booking.room_id == room.id,
            Booking.check_in < end_date,
            Booking.check_out > start_date
        ).first()
        
        if overlap:
            continue # Bu tarih doluysa pas geç, döngü başa dönsün
            
        # Fiyat Hesapla (Basit mantık)
        total_price = float(room.base_price) * stay_duration
        # Hafta sonu ise biraz zam yapalım (Rastgelelik olsun diye)
        if start_date.weekday() >= 5:
            total_price *= 1.2

        # Kaydet
        new_booking = Booking(
            room_id=room.id,
            customer_email=fake.email(),
            check_in=start_date,
            check_out=end_date,
            total_price=round(total_price, 2)
        )
        
        session.add(new_booking)
        try:
            session.commit()
            count += 1
            if count % 10 == 0:
                print(f"✅ {count} adet rezervasyon oluşturuldu...")
        except:
            session.rollback()

    print(f"🎉 BİTTİ! Toplam {count} adet sahte rezervasyon veritabanına eklendi.")

if __name__ == "__main__":
    # Kaç tane veri basalım? 200 iyi bir sayı.
    create_fake_bookings(200)