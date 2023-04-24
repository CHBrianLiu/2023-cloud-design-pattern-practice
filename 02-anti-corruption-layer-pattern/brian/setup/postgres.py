from models.db import postgres_db
from models.users import User

from pony import orm


def _build_connection():
    postgres_db.bind(
        provider='postgres',
        user='postgres',
        password='example',
        host='relational-db',
        database='postgres',
    )


def _build_tables():
    postgres_db.generate_mapping(create_tables=True)


@orm.db_session
def _insert_initial_data():
    print("creating a new user...")
    new_user = User(email="abc@gmail.com")
    print(f"new user created. id: {new_user.id}")
    return str(new_user.id)


def setup():
    _build_connection()
    _build_tables()
    return _insert_initial_data()
