## Problem

> A migration is planned to happen over multiple stages, but integration between new and legacy systems needs to be
> maintained.

## Context

A company stores all the customer data in a relational database. However, they would like to develop a social media
platform that allows users to share thoughts. Moreover, they want to store post data in a non-relational database, but
do not want to migrate the existing data to the new non-relational database due to the complexity.

## Architecture

Instead of letting applications query user metadata and post data from each database respectively, we can add a service
to perform data operations.

![architecture](./architecture.png)

## Demo setup

```shell
docker compose up -d
docker compose exec db-manager python -m setup
docker compose exec -d db-manager python db_manager.py
```

## Run the demo

```shell
docker compose run client \
  -plaintext -proto db_manager.proto \
  -d '{"id": "", "email": "abc@gmail.com"}' \
  db-manager:50051 DbManager.GetUser
```

## Demo

Data is stored in separate databases.

```
$ docker compose exec relational-db psql -U postgres -c 'select * from "user";'
                  id                  |     email     |          created           
--------------------------------------+---------------+----------------------------
 a69c6294-0beb-4cb1-a94c-5207e6d81bbd | abc@gmail.com | 2023-04-23 09:51:08.597678
(1 row)

$ docker compose exec document-db mongosh "mongodb://root:example@localhost"
test> use social_platform
switched to db social_platform
social_platform> db.posts.find()
[
  {
    _id: ObjectId("6444ff8c0e683f2df99264f2"),
    author_id: 'a69c6294-0beb-4cb1-a94c-5207e6d81bbd',
    created: ISODate("2023-04-23T09:51:08.544Z"),
    content: 'This is my first post.'
  },
  {
    _id: ObjectId("6444ff8c0e683f2df99264f3"),
    author_id: 'a69c6294-0beb-4cb1-a94c-5207e6d81bbd',
    created: ISODate("2023-04-23T09:51:08.544Z"),
    content: 'This is my second post.'
  }
]
```

We can use one single gRPC call to get a domain-centric data view.

```
$ docker compose run client \
  -plaintext -proto db_manager.proto \
  -d '{"id": "", "email": "abc@gmail.com"}' \
  db-manager:50051 DbManager.GetUser

{
  "id": "a69c6294-0beb-4cb1-a94c-5207e6d81bbd",
  "email": "abc@gmail.com",
  "posts": [
    {
      "created": "2023-04-23T09:51:08.544Z",
      "updated": "2023-04-23T09:51:08.544Z",
      "content": "This is my first post."
    },
    {
      "created": "2023-04-23T09:51:08.544Z",
      "updated": "2023-04-23T09:51:08.544Z",
      "content": "This is my second post."
    }
  ]
}

```
