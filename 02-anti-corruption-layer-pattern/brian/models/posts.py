from datetime import datetime
from typing import TypedDict


class Post(TypedDict):
    author_id: str
    created: datetime
    content: str
