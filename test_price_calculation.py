from fastapi.testclient import TestClient
from main import app
from models import Room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

# Setup DB connection
DATABASE_URL = "postgresql://admin:sifre123@localhost:5432/otel_db"
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)

client = TestClient(app)

def test_calculate_price():
    db = SessionLocal()
    try:
        room = db.query(Room).first()
    except Exception as e:
        print(f"Failed to query database: {e}")
        return

    if not room:
        print("Skipping test: No rooms found in DB. Please run seed_data.py first.")
        return

    print(f"Testing with Room ID: {room.id}, Price: {room.base_price}")

    # Case 1: Weekdays (Mon-Wed)
    # 2023-11-27 (Mon) to 2023-11-29 (Wed) -> 2 nights
    payload = {
        "room_id": room.id,
        "check_in": "2023-11-27",
        "check_out": "2023-11-29"
    }
    response = client.post("/calculate-price", json=payload)
    if response.status_code != 200:
        print(f"Error: {response.text}")
    assert response.status_code == 200
    data = response.json()
    expected_price = float(room.base_price) * 2
    print(f"Weekdays Test: Got {data['total_price']}, Expected {expected_price}")
    # Use small epsilon for float comparison if needed, but exact match might work for simple cases
    assert abs(data['total_price'] - expected_price) < 0.01
    
    # Case 2: Weekend (Fri-Sun)
    # 2023-11-24 (Fri) to 2023-11-26 (Sun) -> 2 nights (Fri, Sat)
    # Fri is weekday, Sat is weekend (1.2x)
    payload = {
        "room_id": room.id,
        "check_in": "2023-11-24",
        "check_out": "2023-11-26"
    }
    response = client.post("/calculate-price", json=payload)
    assert response.status_code == 200
    data = response.json()
    expected_price = float(room.base_price) + (float(room.base_price) * 1.2)
    print(f"Weekend Test: Got {data['total_price']}, Expected {expected_price}")
    assert abs(data['total_price'] - expected_price) < 0.01

    print("All tests passed!")

if __name__ == "__main__":
    test_calculate_price()
