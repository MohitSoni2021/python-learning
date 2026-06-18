from pydantic import BaseModel
from typing import Dict, Optional, List

class Cart(BaseModel):
    user_id: int
    items: List[str]
    qty: Dict[str, int]