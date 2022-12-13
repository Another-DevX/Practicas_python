#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr, PaymentCardNumber

#FastApi
from fastapi import FastAPI, Body, Query, Path


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


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50 
        )
    last_name: str = Field(
                ...,
        min_length = 1,
        max_length = 50 
    )
    age: int = Field(
        ...,
        gt = 0,
        le = 115
    )
    mail: EmailStr = Field()
    creditCar: PaymentCardNumber = Field()
    hair_color: Optional[HairColor] = Field(default = None) 
    isMarried: Optional[bool] = Field(default = None)
    
    class Config():
        schema_extra = {
            "example": {
                "first_name" : "Luis",
                "last_name" : "Velasquez",
                "age" : 17,
                "mail" : "xyz@gmail.com",
                "creditCar" : 1234567890123,
                "hair_color" : "black",
                "isMarried" : False
            }
        }

@app.get("/")
def home():
    return {"Hello":"World"}


#Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body()):
    return person

#Validaciones: Query Parameters

@app.get("/person/detail")
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

@app.get("/persons/detail/{person_id}")
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

@app.put("/person/{person_id}")
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


