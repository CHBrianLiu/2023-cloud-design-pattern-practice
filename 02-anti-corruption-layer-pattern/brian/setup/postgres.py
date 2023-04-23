from models.db import db
from models.users import User

from pony import orm


def _build_connection():
    db.bind(
        provider='postgres',
        user='postgres',
        password='example',
        host='relational-db',
        database='postgres',
    )


def _build_tables():
    db.generate_mapping(create_tables=True)


@orm.db_session
def _insert_initial_data():
    new_user = User(email="abc@gmail.com")
    return new_user.id


def setup():
    _build_connection()
    _build_tables()
    return _insert_initial_data()
