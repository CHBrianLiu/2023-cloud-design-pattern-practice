from datetime import datetime
from pymongo import MongoClient

from models import db

_posts = [
    {
        "author_id": "",
        "created": datetime.utcnow(),
        "content": "This is my first post."
    },
    {
        "author_id": "",
        "created": datetime.utcnow(),
        "content": "This is my second post."
    },
]


def setup(author_id: str):
    posts = db.mongo_db.posts
    print(f"adding {len(_posts)} posts...")
    posts.insert_many(map(lambda p: {**p, "author_id": author_id}, _posts))
    print("posts added")
