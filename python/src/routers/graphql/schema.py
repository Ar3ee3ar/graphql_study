import strawberry
from datetime import datetime

@strawberry.type
class UserType:
    id: int
    username: str
    password: str
    created_at: datetime
    last_login: datetime
    first_name: str
    last_name: str
    email: str

@strawberry.input
class CreateUser:
    # id: int | None = strawberry.UNSET # NULLABLE (default value is UNSET)
    # variable: type = "" (NON-NULLABLE if not provide value default will be "")
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""

@strawberry.input
class UpdateUser:
    username: str
    new_username: str | None = strawberry.UNSET
    password: str
    new_password: str | None = strawberry.UNSET
    first_name: str | None = strawberry.UNSET
    last_name: str | None = strawberry.UNSET
    email: str | None = strawberry.UNSET
