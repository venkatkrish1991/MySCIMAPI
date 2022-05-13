from typing import Optional
from uuid import UUID,uuid4
from pydantic import BaseModel

class User(BaseModel):
    schemas:list
    active: bool
    displayName:str
    userName: str
    externalId:str
    email:str

    #phoneNumbers:list=[{"value":value,"type":type}]

class UserUpdateRequest(BaseModel):
    schemas:list
    active: bool
    displayName:str
    userName: str
    externalId:str
    email:str

class UserLoginSchema(BaseModel):
    externalId:str
    password:str
