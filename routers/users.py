from fastapi import Depends, APIRouter, HTTPException, status, Body, Request, Response
import connector
import auth
from typing import Annotated
from models.user import User
import json

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
def get_user_me(request: Request, response: Response):
    if auth.authenticate_user(token=request.headers["Authorization"]):
        userInfo = {"username": "",
                    "email": "",
                    "password": "",
                    "pseudo": "",
                    "highscore": "",
                    "gamesplayed": "",
                    }
        try:
            query = "SELECT app_user.id_user, app_user.username, app_user.password, app_user.email, player.id_player, player.pseudo, score.score, score.id_score, COUNT(score.id_score) AS gamesplayed FROM `app_user` JOIN player ON player.id_user = app_user.id_user JOIN score ON player.id_player = score.id_player WHERE app_user.username = %s GROUP BY app_user.id_user ORDER BY score.score DESC; "
            cursor = db.cursor()
            cursor.execute(query, [auth.authenticate_user(token=request.headers["Authorization"]).username])
            result = cursor.fetchone()
            cursor.close()
            userInfo["username"] = result[1]
            userInfo["email"] = result[3]
            userInfo["password"] = result[2]
            userInfo["pseudo"] = result[5]
            userInfo["highscore"] = result[6]
            userInfo["gamesplayed"] = result[8]
            return userInfo
        except Exception as e:
            print("get_user_me: ", e)
            return None
    return None


@router.get("/leaderboard", tags=["users"])
def get_user_leaderboard(request: Request, response: Response):
    if auth.authenticate_user(token=request.headers["Authorization"]):
        try:
            query = "SELECT app_user.id_user, app_user.username, app_user.password, app_user.email, player.id_player, player.pseudo, score.score, score.id_score, COUNT(score.id_score) AS gamesplayed FROM `app_user` JOIN player ON player.id_user = app_user.id_user JOIN score ON player.id_player = score.id_player GROUP BY app_user.id_user ORDER BY score.score DESC; "
            cursor = db.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            print(results)
            cursor.close()
            usersLength = len(results)
            userInfo = [{} for i in range(usersLength)]
            usersLengthRange = range(len(results))
            print(usersLengthRange)
            for i in usersLengthRange:
                print(i)
                userInfo[i]["username"] = results[i][1]
                userInfo[i]["email"] = results[i][3]
                userInfo[i]["password"] = results[i][2]
                userInfo[i]["pseudo"] = results[i][5]
                userInfo[i]["highscore"] = results[i][6]
                userInfo[i]["gamesplayed"] = results[i][8]

            return userInfo
        except Exception as e:
            print("get_user_leaderboard: ", e)
            return None
    return None




@router.get("/{username}", tags=["users"])
def get_user(username: str):
    return {"username": username}