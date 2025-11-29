from schemas import BookingCreate
from datetime import date, timedelta
from pydantic import ValidationError

def verify_schema():
    print("Verifying BookingCreate schema...")

    # Test valid case
    try:
        valid_booking = BookingCreate(
            room_id=1,
            customer_email="test@example.com",
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1)
        )
        print("SUCCESS: Valid booking created.")
    except ValidationError as e:
        print(f"ERROR: Valid booking failed validation: {e}")

    # Test invalid case (check_in > check_out)
    try:
        BookingCreate(
            room_id=1,
            customer_email="test@example.com",
            check_in=date.today() + timedelta(days=1),
            check_out=date.today()
        )
        print("ERROR: Invalid booking (check_in > check_out) passed validation.")
    except ValidationError as e:
        print("SUCCESS: Invalid booking failed validation as expected.")
        # print(e)

    # Test invalid case (check_in == check_out) - wait, user said check_in < check_out, usually equal is also invalid for hotels but let's see my code.
    # My code: if check_in >= check_out: raise ValueError
    # So equal should fail too.
    try:
        BookingCreate(
            room_id=1,
            customer_email="test@example.com",
            check_in=date.today(),
            check_out=date.today()
        )
        print("ERROR: Invalid booking (check_in == check_out) passed validation.")
    except ValidationError as e:
        print("SUCCESS: Invalid booking (equal dates) failed validation as expected.")

if __name__ == "__main__":
    verify_schema()
