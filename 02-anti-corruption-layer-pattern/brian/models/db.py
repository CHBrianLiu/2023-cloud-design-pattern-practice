from pony import orm
from pymongo import MongoClient

postgres_db = orm.Database()

client = MongoClient("mongodb://root:example@document-db")
mongo_db = client.social_platform
