from fastapi.testclient import TestClient
from main import app, get_db, Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from datetime import date, timedelta

# Use the same database for simplicity in this dev environment, 
# or we could create a separate test db. 
# For now, let's assume it's safe to use the dev db as we are just testing.
# But to be safe, let's try to create a clean state or just pick a random room.

client = TestClient(app)

def test_create_booking():
    print("Testing Booking Endpoint...")
    
    # 1. Create a room first (or ensure one exists)
    # We can use the existing /hotels endpoint to check or just assume ID 1 exists if seeded.
    # Let's try to seed a room if possible or just pick ID 1.
    room_id = 1
    
    # 2. Create a valid booking
    check_in = date.today() + timedelta(days=10)
    check_out = date.today() + timedelta(days=12)
    
    payload = {
        "room_id": room_id,
        "customer_email": "test_booking@example.com",
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat()
    }
    
    response = client.post("/bookings", json=payload)
    if response.status_code == 200:
        print("SUCCESS: Booking created successfully.")
        data = response.json()
        print(f"Booking ID: {data['id']}, Total Price: {data['total_price']}")
    elif response.status_code == 404:
         print("WARNING: Room 1 not found. Please run seed_data.py first.")
         return
    else:
        print(f"ERROR: Failed to create booking. Status: {response.status_code}, Detail: {response.text}")
        return

    # 3. Try to create an overlapping booking (Conflict)
    print("Testing Overlap Check...")
    response_conflict = client.post("/bookings", json=payload)
    if response_conflict.status_code == 409:
        print("SUCCESS: Overlapping booking correctly rejected (409 Conflict).")
    else:
        print(f"ERROR: Overlapping booking NOT rejected. Status: {response_conflict.status_code}")

    # 4. Try to create a booking for non-existent room
    print("Testing Non-existent Room...")
    payload_404 = payload.copy()
    payload_404["room_id"] = 99999
    response_404 = client.post("/bookings", json=payload_404)
    if response_404.status_code == 404:
        print("SUCCESS: Non-existent room correctly returned 404.")
    else:
        print(f"ERROR: Non-existent room check failed. Status: {response_404.status_code}")

if __name__ == "__main__":
    test_create_booking()
