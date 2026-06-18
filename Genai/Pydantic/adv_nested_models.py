from pydantic import BaseModel
from typing import Optional, List, Union

class Address(BaseModel):
    street : str
    city : str
    postal_code : str

class Company(BaseModel):
    name : str
    cpy_id : str
    address : Optional[Address] = None

class Person(BaseModel):
    name : str
    company : Optional[Company] = None

codinggita_address = Address(
    street="street 12",
    city="Ahmedabad",
    postal_code="333029"
)

codinggita = Company(
    name="Coding Gita Private Limited",
    cpy_id="CG_PVT_LTD",
    address=codinggita_address
)

mohitsoni = Person(
    name= "Mohit Soni",
    company= codinggita
)

print(mohitsoni)



# another trying...

class TextContent(BaseModel):
    type: str = "text"
    content : str

class ImageContent(BaseModel):
    type: str = "Image"
    url : str
    alt_text : str

class Article(BaseModel):
    title : str
    sections : List[Union[TextContent, ImageContent]]