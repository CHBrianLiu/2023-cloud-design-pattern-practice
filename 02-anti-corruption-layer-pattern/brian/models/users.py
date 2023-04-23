from uuid import UUID, uuid4
from datetime import datetime

from pony import orm

from .db import postgres_db


class User(postgres_db.Entity):
    id = orm.PrimaryKey(UUID, default=uuid4)
    email = orm.Required(str, unique=True, index=True)
    created = orm.Required(datetime, default=datetime.utcnow)
