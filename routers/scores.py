from fastapi import APIRouter, Depends, Body, Request, Response
import connector
import auth
from typing import Annotated
import json

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

@router.post("/add", tags=["scores"])
async def add_score(req: Request, res: Response):
    if auth.authenticate_user(token=req.headers["Authorization"]):
        try:
            query = "SELECT app_user.username, player.id_player, app_user.id_user, player.id_user FROM player JOIN app_user ON app_user.id_user = player.id_user WHERE username = %s LIMIT 1"
            cursor = db.cursor()
            cursor.execute(query, [auth.authenticate_user(token=req.headers["Authorization"]).username])
            playerID = cursor.fetchone()[1]
            cursor.close()
            print(playerID)

            query = "INSERT INTO score (score, id_player) VALUES (%s, %s)"
            cursor = db.cursor()
            data = await req.json()
            cursor.execute(query, [data["score"], playerID])
            db.commit()
            cursor.close()
        except Exception as e:
            print("add_score: ", e)
