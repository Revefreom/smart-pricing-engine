from pydantic import BaseModel, field_validator
from datetime import date

class BookingCreate(BaseModel):
    room_id: int
    customer_email: str
    check_in: date
    check_out: date

    @field_validator('check_out')
    def check_dates(cls, check_out, info):
        if 'check_in' in info.data:
            check_in = info.data['check_in']
            if check_in >= check_out:
                raise ValueError('Check-out date must be after check-in date')
        return check_out

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