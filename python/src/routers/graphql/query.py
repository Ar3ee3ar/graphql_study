import strawberry
from sqlmodel import Session, text, select

from routers.graphql.schema import UserType
from db.main import engine

@strawberry.type
class Query:
    @strawberry.field
    def getAllUsers(self, info: strawberry.Info) -> list[UserType]:
        user = info.context.get("user")
        if not user:
            raise Exception("Authentication required")
        
        with Session(engine) as session:
            statement = text("SELECT * FROM users;")
            result = session.execute(statement)
            return result
    @strawberry.field
    def getUserId(self, id:int, info: strawberry.Info) -> UserType:
        user = info.context.get("user")
        if not user:
            raise Exception("Authentication required")
        with Session(engine) as session:
            # statement = select(UserType).where(UserType.username == username)
            statement = text(f"SELECT * FROM users WHERE id = {id};")
            user_info = session.exec(statement).first()
            return user_info