import strawberry
from sqlmodel import Session, text, select, func
from datetime import datetime
from fastapi import HTTPException, status

from routers.graphql.schema import UserType, CreateUser, UpdateUser
from routers.user.routes import get_password_hash,verify_password
from db.models import User
from db.main import engine

@strawberry.type
class Mutation:
    @strawberry.field
    def createUser(self, user_input: CreateUser) -> UserType:
        with Session(engine) as session:
            statement = select(User).where(User.username == user_input.username)
            db_user = session.exec(statement).first()
            if(len(list(db_user)) == 0):
                # 1. Map input to DB Model
                db_user = User(
                    username=user_input.username,
                    password=get_password_hash(user_input.password),
                    created_at=datetime.now(),
                    last_login=datetime.now(),
                    first_name = user_input.first_name,
                    last_name = user_input.last_name,
                    email = user_input.email
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
                    last_login=db_user.last_login,
                    first_name = db_user.first_name,
                    last_name = db_user.last_name,
                    email = db_user.email
                )
            else:
                raise HTTPException(
                        status_code=409,
                        detail="This username already taken",
                    )
    @strawberry.field
    def updateUser(self, user_input: UpdateUser) -> UserType:
        # hashed_password  = get_password_hash(user_input.old_password)
        with Session(engine) as session:
            # statement = text(f"SELECT password from users where username = '{user_input.username}';")
            statement = select(User).where(User.username == user_input.username)
            db_user = session.exec(statement).first()
            if(len(list(db_user)) != 0):
                if(verify_password(user_input.password, db_user.password)):
                    # changed current data
                    if(user_input.new_username is not strawberry.UNSET):
                        statement_chkUser = select(func.count(User.id)).where(User.username == user_input.new_username)
                        chkUser_count = session.exec(statement_chkUser).one()
                        if(chkUser_count == 0):
                            db_user.username = user_input.new_username
                        else:
                            raise HTTPException(
                                status_code=409,
                                detail="This username already taken",
                            )
                    if(user_input.first_name is not strawberry.UNSET):
                        db_user.first_name = user_input.first_name
                    if(user_input.last_name is not strawberry.UNSET):
                        db_user.last_name = user_input.last_name
                    if(user_input.email is not strawberry.UNSET):
                        db_user.email = user_input.email
                    if(user_input.new_password is not strawberry.UNSET):
                        db_user.password = get_password_hash(user_input.new_password)
                    # update to database
                    session.add(db_user)
                    session.commit()
                    session.refresh(db_user)
                    # Map DB Model -> Strawberry Type
                    return UserType(
                        id=db_user.id,
                        username=db_user.username,
                        password=db_user.password,
                        created_at=db_user.created_at,
                        last_login=db_user.last_login,
                        first_name = db_user.first_name,
                        last_name = db_user.last_name,
                        email = db_user.email
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password",
                    )
            else:
                raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password",
                    )
    @strawberry.field
    def delUser(self, id: int) -> UserType:
        with Session(engine) as session:
            statement = select(User).where(User.id == id)
            db_user = session.exec(statement).one()
            if(len(list(db_user)) != 0):
                session.delete(db_user)
                session.commit()
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Not found user with id: {id}",
                )
        return UserType(
                    id=db_user.id,
                    username=db_user.username,
                    password=db_user.password,
                    created_at=db_user.created_at,
                    last_login=db_user.last_login,
                    first_name = db_user.first_name,
                    last_name = db_user.last_name,
                    email = db_user.email
                )
