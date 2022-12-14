#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr, PaymentCardNumber

#FastApi
from fastapi import FastAPI, status, Body, Query, Path, Form, Header, Cookie


app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city:str = Field(
        ...,
        min_length = 3,
        max_length = 12)
    state:str = Field(
        ...,
        min_length = 3,
        max_length = 20)
    country:str = Field(
        ...,
        min_length = 3,
        max_length = 12)

class PersonBase(BaseModel):
    first_name: str = Field(
    ...,
    min_length = 1,
    max_length = 50,
    example="Luis" 
    )
    last_name: str = Field(
            ...,
    min_length = 1,
    max_length = 50,
    example="Martinez" 
    )
    age: int = Field(
    ...,
    gt = 0,
    le = 115,
    example="17"
    )
    mail: EmailStr = Field(
        ...,
        example="a@b.c"
        )
    hair_color: Optional[HairColor] = Field(
        default = None,
        example="white"
        ) 
    isMarried: Optional[bool] = Field(
        default = None,
        example=False
        )

class Person(PersonBase):
    password: str = Field(...,
                          min_length=8)

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username:str = Field(
        ...,
        max_length=20,
        example = "Lokochris37"
        )

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello":"World"}


#Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body()):
    return person

#Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length = 1, 
        max_length = 50,
        title = "Person Name",
        description = "This is the person name. It's between 1 and 50 character",
        example = "Rocio"
        ),
    age: int = Query(
        title = "Person Age",
        description = "This is the person age. It's required",
        example = 25
    )
):
    return {name : age}

#Validaciones: Path Parameters

@app.get(
    path="/persons/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = "Person Id",
        description = "This is te person ID, It's required",
        example = 225 
        )
):
    return {person_id:"It exist!"}

#Validacions: request body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        description = "This is the person ID",
        gt = 0,
        example = 225
    ),
    person: Person = Body(),
    location: Location = Body()
):
    results = person.dict(), 
    results.update(location.dict())
    return results


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(), password: str = Form()):
    return  LoginOut(username=username)

#Cookies and Headers Parameters

@app.post(
    path= "/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent