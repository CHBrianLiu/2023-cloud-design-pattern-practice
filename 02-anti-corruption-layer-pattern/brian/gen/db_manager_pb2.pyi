from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserRequest(_message.Message):
    __slots__ = ["email", "id"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ["content", "created", "updated"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    content: str
    created: _timestamp_pb2.Timestamp
    updated: _timestamp_pb2.Timestamp
    def __init__(self, created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., content: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["email", "id", "posts"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSTS_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: str
    posts: _containers.RepeatedCompositeFieldContainer[Post]
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., posts: _Optional[_Iterable[_Union[Post, _Mapping]]] = ...) -> None: ...
