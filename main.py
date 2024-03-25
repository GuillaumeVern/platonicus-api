from typing import Union
from fastapi import FastAPI
from routers import players, scores, users
import auth

app = FastAPI()


app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(scores.router, prefix="/scores", tags=["scores"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"Hello": "World"}
