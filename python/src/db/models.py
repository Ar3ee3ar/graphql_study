from datetime import datetime
import uuid

from sqlmodel import Field, SQLModel

class ApiUserBase(SQLModel, table=True):
    # real db name in psql
    __tablename__ = "api_usage"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True,description="The user that owned api key") #  allow faster lookups in the database when reading data filtered by this column.
    active: bool = Field(description="Whether the api key is active or not")
    key_name: str = Field(max_length = 50 ,description="The api key's name")
    api_key: uuid.UUID = Field(description="The api key value")
    monthly_credits: int | None = Field(default=0, description="The number of credits the user has for the month")
    curr_credits: int = Field(default=0, description="The number of credits the user has left for the month") 
    created_at: datetime = Field(description="The date and time the api key was created")
    updated_at: datetime = Field(description="The date and time the api key was updated")

class User(SQLModel, table=True):
    # real db name in psql
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, description="User name")
    password: str = Field(max_length=255, description="password")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, 
        nullable=False
    )
    last_login: datetime | None = Field()
    first_name: str = Field(max_length=150, description="first name")
    last_name: str = Field(max_length=150, description="last name")
    email: str = Field(max_length=254, description="email")