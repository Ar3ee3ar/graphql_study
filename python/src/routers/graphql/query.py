import strawberry
from sqlmodel import Session, text, select

from routers.graphql.schema import UserType
from db.main import engine

@strawberry.type
class Query:
    @strawberry.field
    def getAllUsers(self) -> list[UserType]:
        with Session(engine) as session:
            statement = text("SELECT * FROM users;")
            result = session.execute(statement)
            return result
    @strawberry.field
    def getUserId(self, id:int) -> UserType:
        with Session(engine) as session:
            # statement = select(UserType).where(UserType.username == username)
            statement = text(f"SELECT * FROM users WHERE id = {id};")
            user_info = session.exec(statement).first()
            return user_info