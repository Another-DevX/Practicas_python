from uuid import UUID
from datetime import date, datetime
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#Fast API
from fastapi import FastAPI

app = FastAPI()

#MODELS
class UserBase(BaseModel):
    user_id : UUID = Field()
    mail : EmailStr = Field()

class UserLogin(UserBase):
    password : str  = Field(
        ..., 
        min_length=8,
        max_length=64
        )

class User(UserBase):
    username : str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    birth_date: Optional[date] = Field(default=None)
class Tweet(BaseModel):
    tweet_id : UUID = Field()
    content : str = Field(
        ...,
        max_length=256,
        min_length=1
    )
    created_at : datetime = Field(default=datetime.now())
    updated_at : Optional[datetime] = Field(default=None)
    by : User = Field()



@app.get(path="/")
def home():
    return {"Twitter API" : "Working!"}

