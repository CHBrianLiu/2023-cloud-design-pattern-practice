from . import postgres, mongo

if __name__ == '__main__':
    user_id = postgres.setup()
    mongo.setup(user_id)
