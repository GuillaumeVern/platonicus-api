from fastapi import APIRouter, Depends
import connector
import auth
from typing import Annotated

router = APIRouter()
db = connector.connect()

@router.get("/", tags=["scores"])
def get_scores():
    query = "SELECT * FROM scores"
    db.query(query)
    result = db.store_result()
    result = result.fetch_row(maxrows=0)
    return result


@router.get("/me", tags=["scores"])
def get_score_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["scores"])
def get_score_user(username: str):
    return {"username": username}