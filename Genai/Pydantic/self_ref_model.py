from pydantic import BaseModel
from typing import List, Optional

class Comment(BaseModel):
    id : int
    content : str
    replies : Optional[List['Comment']] = None # this is self referencing

Comment.model_rebuild() # this line needed to increase the performance

user_comment = {
    "id" : 123,
    "content" : "New Video uploaded",
    "replies" : [
        {
            "id" : 456,
            "content" : "Great Video",
            "replies" : [
                {
                    "id" : 123,
                    "content" : "Thank you for the compliment"
                }
            ]
        }
    ]
}

mohit_video = Comment(**user_comment)
print(mohit_video)