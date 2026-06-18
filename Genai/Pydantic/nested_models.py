from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street : str
    city : str
    postal_code : str

class Person(BaseModel):
    id : int
    name : str
    address : Address 

home_address = Address(
    street="4th street",
    city="sikar",
    postal_code="333029"
)

mohit = Person(
    id = 1233,
    name= "Mohit Soni",
    address=home_address
)

user2_data = {
    "id": 456,
    "name" : "Mohit Soni",
    "address" : {
        "street" : "user2 _ street",
        "city" : "Surat",
        "postal_code" : "456ASD"
    }
}

user2_details = Person(**user2_data)


print(mohit)
print(user2_details)