from models import Booking, Room, Base
from sqlalchemy import inspect

def verify_models():
    print("Verifying models...")
    
    # Check if Booking table exists in metadata
    if 'bookings' in Base.metadata.tables:
        print("SUCCESS: 'bookings' table found in metadata.")
    else:
        print("ERROR: 'bookings' table NOT found in metadata.")
        return

    # Inspect Booking model
    mapper = inspect(Booking)
    columns = [c.key for c in mapper.columns]
    expected_columns = ['id', 'room_id', 'customer_email', 'check_in', 'check_out', 'total_price']
    
    missing_columns = [col for col in expected_columns if col not in columns]
    if not missing_columns:
        print("SUCCESS: All expected columns found in Booking model.")
    else:
        print(f"ERROR: Missing columns in Booking model: {missing_columns}")

    # Check relationships
    if 'room' in mapper.relationships:
        print("SUCCESS: 'room' relationship found in Booking model.")
    else:
        print("ERROR: 'room' relationship NOT found in Booking model.")

    room_mapper = inspect(Room)
    if 'bookings' in room_mapper.relationships:
        print("SUCCESS: 'bookings' relationship found in Room model.")
    else:
        print("ERROR: 'bookings' relationship NOT found in Room model.")

if __name__ == "__main__":
    verify_models()
