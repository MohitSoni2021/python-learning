from pydantic import BaseModel

# adding the pydantic validations --
class User(BaseModel):
    id: int
    name: str
    is_active: bool

data = {"id": 12, "name" : "Mohit Soni", "is_active": True}

mohit = User(**data)

print(mohit)