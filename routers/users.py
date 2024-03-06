from fastapi import APIRouter
import connector

router = APIRouter()
db = connector.connect()

@router.get("/", tags=["users"])
def get_users():
    query = "SELECT * FROM player"
    db.query(query)
    result = db.store_result()
    result = result.fetch_row(maxrows=0)
    return result


@router.get("/me", tags=["users"])
def get_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
def get_user(username: str):
    return {"username": username}