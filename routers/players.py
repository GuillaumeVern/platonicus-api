from fastapi import APIRouter, Depends
import connector
import auth
from typing import Annotated

router = APIRouter()
db = connector.connect()


@router.get("/", tags=["players"])
def get_players():
    query = "SELECT * FROM player"
    db.query(query)
    result = db.store_result()
    result = result.fetch_row(maxrows=0)
    return result


@router.get("/me", tags=["players"])
def get_player_me():
    return auth.decode_token(oauth2_scheme   )


@router.get("/{username}", tags=["players"])
def get_player(username: str):
    return {"username": username}