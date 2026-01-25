import strawberry
from sqlmodel import Session, text, select
from datetime import datetime

from routers.graphql.schema import UserType, CreateUser
from routers.user.routes import get_password_hash
from routers.user.models import User
from db.main import engine

@strawberry.type
class Mutation:
    @strawberry.field
    def createUser(self, user_input: CreateUser) -> UserType:
        with Session(engine) as session:
            # 1. Map input to DB Model
            db_user = User(
                username=user_input.username,
                password=get_password_hash(user_input.password),
                created_at=datetime.now(),
                last_login=datetime.now()
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        # 2. Map DB Model -> Strawberry Type
        return UserType(
            id=db_user.id,
            username=db_user.username,
            password=db_user.password,
            created_at=db_user.created_at,
            last_login=db_user.last_login
        )