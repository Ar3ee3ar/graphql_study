from datetime import datetime
import strawberry
# from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from sqlmodel import Session, select, text

from db.models import User, ApiUserBase
from db.main import engine
from routers.graphql.query import Query
from routers.graphql.mutation import Mutation

# @strawberry.type
# class UserType:
#     id: int
#     username: str
#     password: str
#     created_at: datetime
#     last_login: datetime


# @strawberry.type
# class Query:
#     @strawberry.field
#     def user(self) -> list[UserType]:
#         with Session(engine) as session:
#             statement = text("SELECT * FROM users;")
#             result = session.execute(statement)
#             # return User(name="Patrick", age=100)
#             return result


schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_app = GraphQLRouter(schema)