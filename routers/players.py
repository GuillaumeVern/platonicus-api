from fastapi import APIRouter, Depends
import connector
import auth
from typing import Annotated

router = APIRouter()
db = connector.connect()


@router.get("/", tags=["players"])
def get_players():
    query = "SELECT * FROM player"
    db.cmd_query(query)
    result = db.get_rows()
    return result

@router.post("/", tags=["players"])
def create_player():
    query = "INSERT INTO player (Name, id_User) VALUES (%s, %s, %s)"
    db.cmd_query(query, ("test", "test", "test"))
    return {"username": "test", "password": "test", "email": "test"}


@router.get("/me", tags=["players"])
def get_player_me():
    query = "SELECT * FROM player WHERE username = %s"
    db.cmd_query(query, (auth.get_current_user().username))
    result = db.get_row()
    return result


@router.get("/{username}", tags=["players"])
def get_player(username: str):
    return {"username": username}

