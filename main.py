from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import players, scores, users
import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(scores.router, prefix="/scores", tags=["scores"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"Hello": "World"}
