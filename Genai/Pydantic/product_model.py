from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True

product1 = Product(id=123, name="Lenovo LOQ 2024", price=60000.00, in_stock=True)

product2 = Product(id=456, name="Lenovo Legion 2026", price=120000.00)

# if the int passed in the form of the int automatically converted to the int itself, same for the other types
# "true" -> True
# "90000.00" ->  90000.00
product3 = Product(id="789", name="HP Viktus", price="90000.00")

print(product1)
print(product2) 