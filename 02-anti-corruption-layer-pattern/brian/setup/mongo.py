from datetime import datetime
from pymongo import MongoClient

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


def setup(author_id):
    client = MongoClient("mongodb://root:example@document-db")
    db = client.social_platform
    posts = db.posts
    posts.insert.insert_many(map(lambda p: {**p, "author_id": author_id}, _posts))
