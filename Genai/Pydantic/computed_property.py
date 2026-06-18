from pydantic import BaseModel, computed_field, Field

class Product(BaseModel):
    price : float
    qty : int

    @computed_field
    @property
    def total_price(self) -> float :
        return self.price * self.qty
    
class Booking(BaseModel) :
    user_id: int
    room_no: int
    nights: int = Field(..., ge=1)
    rate_per_night: float

    @computed_field
    @property
    def total_prices(self) -> float:
        return self.nights * self.rate_per_night
    
mohit_booking = Booking(
    user_id=123,
    room_no=94,
    nights=4,
    rate_per_night=1000
)

person_booking = Booking(
    user_id=456,
    room_no=9,
    nights=1,
    rate_per_night=2000
)

print(mohit_booking.total_prices)
print(mohit_booking.model_dump()) # this provide the whole object of this object instance
print(person_booking.total_prices)