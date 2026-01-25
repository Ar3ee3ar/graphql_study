import strawberry
from datetime import datetime

@strawberry.type
class UserType:
    id: int
    username: str
    password: str
    created_at: datetime
    last_login: datetime

@strawberry.input
class CreateUser:
    # id: int | None
    username: str
    password: str
    created_at: datetime | None = strawberry.UNSET
    last_login: datetime | None = strawberry.UNSET
