from fastapi import Depends, APIRouter, HTTPException, status
import connector
import auth
from typing import Annotated
from models.user import User

router = APIRouter()
db = connector.connect()


@router.get("/", tags=["users"])
def get_users():
    query = "SELECT * FROM app_user"
    db.query(query)
    result = db.store_result()
    result = result.fetch_row(maxrows=0)
    return result

@router.get("/me", tags=["users"])
def get_user_me(response_model=User):
    return auth.get_current_user(token)
    


@router.get("/{username}", tags=["users"])
def get_user(username: str):
    return {"username": username}