from typing import Optional,List
from fastapi import FastAPI,HTTPException
#from sqlalchemy.testing.suite.test_reflection import users

from model import User,UserUpdateRequest,UserLoginSchema
from uuid import UUID,uuid4
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from auth_handler import signJWT
from auth_bearer import JWTBearer

app = FastAPI()

db: List[User]= []

def check_user(user: UserLoginSchema):
    for user in user:
        if user.externalId == user.externalId and user.password == user.password:
            return True
    return False

@app.post("/scim/Token")
async def signup_user(user: UserLoginSchema):
    #db.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.externalId)

@app.post("/scim/v2/Users/login")
def user_login(user: UserLoginSchema):
    if check_user(user):
        return signJWT(user.externalId)
    return {
        "error": "Wrong login details!"
    }
@app.get("/")
async def read_root():
    return db

@app.get("/scim/v2/Users",dependencies=[Depends(JWTBearer())])
async def fetch_users():
    #return db
    user_schema = {
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"],
    "active": True,
    "displayName":"",
    "userName": "Test_User_ab6490ee-1e48-479e-a20b-2d77186b5dd1",
    "externalId": "0a21f0f2-8d2a-4f8e-bf98-7363c4aed4ef",
    "email":"venakat@outlook.com"
}
    return user_schema

@app.post("/scim/v2/Users",dependencies=[Depends(JWTBearer())])
async def create_user(user:User):
    db.append(user)
    return {"externalId":user.externalId}

@app.delete("/scim/v2/Users/{externalId}",dependencies=[Depends(JWTBearer())])
async def delete_user(externalId):
    for user in db:
        if user.externalId==externalId:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {externalId} does not exist"
    )

@app.put("scim/v2/Users/{externalId}",dependencies=[Depends(JWTBearer())])
async def update_user(user_update:UserUpdateRequest,externalId:str):
    for user in db:
        if user.externalId == externalId:
            if user_update.displayName is not None:
                user.displayName = user_update.displayName+" Updated"
            #if user_update.businessPhones is not None:
            #    user.businessPhones = user_update.businessPhones
            #if user_update.mobilePhone is not None:
            #    user.mobilePhone = user_update.mobilePhone
            #if user_update.officeLocation is not None:
            #    user.officeLocation = user_update.officeLocation
            #if user_update.jobTitle is not None:
            #    user.jobTitle = user_update.jobTitle
            return user.displayName
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {externalId} does not exist"
    )