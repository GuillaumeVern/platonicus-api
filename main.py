from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel # base python types

from routers import users

app = FastAPI()


app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"Hello": "World"}
