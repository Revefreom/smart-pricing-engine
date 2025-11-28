from pydantic import BaseModel
from datetime import date

class BookingRequest(BaseModel):
    room_id: int
    check_in: date
    check_out: date

class Config:
        json_schema_extra = {
            "example": {
                "room_id": 1,
                "check_in": "2023-12-01",
                "check_out": "2023-12-05"
            }
        }

class PriceResponse(BaseModel):
    total_price: float
    breakdown: str