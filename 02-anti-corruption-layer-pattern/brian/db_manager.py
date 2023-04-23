from concurrent import futures

import grpc
from pony import orm

from gen import db_manager_pb2_grpc, db_manager_pb2
from models import db, users, posts


@orm.db_session
def get_user_meta(_id: str = "", email: str = "") -> users.User:
    if _id:
        user = users.User.get(id=_id)
    else:
        user = users.User.get(email=email)
    return user


def get_posts_from_user(user_id: str) -> list[posts.Post]:
    return db.mongo_db.posts.find({"author_id": user_id})


class DbManagerServicer(db_manager_pb2_grpc.DbManagerServicer):
    def GetUser(self, request: db_manager_pb2.GetUserRequest, context):
        if not request.id and not request.email:
            return grpc.StatusCode.INVALID_ARGUMENT
        user_mata = get_user_meta(request.id, request.email)
        posts_from_user = get_posts_from_user(str(user_mata.id))

        posts_in_proto = []
        for post in posts_from_user:
            post_in_proto = db_manager_pb2.Post()
            post_in_proto.content = post["content"]
            post_in_proto.created.FromDatetime(post["created"])
            post_in_proto.updated.FromDatetime(post["created"])
            posts_in_proto.append(post_in_proto)
        user = db_manager_pb2.User(id=str(user_mata.id), email=user_mata.email, posts=posts_in_proto)
        return user


def initialize_postgres_connection():
    db.postgres_db.bind(
        provider='postgres',
        user='postgres',
        password='example',
        host='relational-db',
        database='postgres',
    )
    db.postgres_db.generate_mapping()


def serve():
    initialize_postgres_connection()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_manager_pb2_grpc.add_DbManagerServicer_to_server(
        DbManagerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
