from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class User(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool = True
    createdAt: datetime
    address: Address
    tags: List[str] = []

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime('%d-%m-%Y %H-%M-%S')
        }
    )


mohit = User(
    id="MS_001",
    name="Mohit Soni",
    email="mohitsoni2006ms@gmail.com",
    createdAt=datetime(2024, 3, 15, 14, 30),
    address={
        "street": "street _ 1",
        "city": "Sikar",
        "postal_code": "333029"
    },
    tags=["user", "premium"],
    is_active=False,
)

python_dict = mohit.model_dump()
print(python_dict)
print("==" * 30)
print(mohit)
print("==" * 30)
print(mohit.model_dump_json())