from . import postgres, mongo

if __name__ == '__main__':
    print("setting up postgresql...")
    user_id = postgres.setup()
    print("setting up mongodb...")
    mongo.setup(user_id)
