from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Veritabanı bağlantı bilgileri (docker-compose.yml dosyasından alındı)
DB_USER = 'admin'
DB_PASSWORD = 'sifre123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'otel_db'

# Bağlantı URL'si oluşturma
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def test_connection():
    try:
        # Engine oluşturma
        engine = create_engine(DATABASE_URL)
        
        # Bağlantıyı test etme
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print("Bağlantı Başarılı")
            print(f"Veritabanı Versiyonu: {version}")
            
    except SQLAlchemyError as e:
        print("Bağlantı Hatası:")
        print(e)
    except Exception as e:
        print("Beklenmeyen bir hata oluştu:")
        print(e)

if __name__ == "__main__":
    test_connection()
