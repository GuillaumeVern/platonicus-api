from pydantic import BaseModel

class User(BaseModel):
    id_user: int
    username: str
    password: str
    email: str | None = None
    token: str | None = None

    def __init__(self, id_user: int, username: str, password: str, email: str | None = None):
        super().__init__(id_user=id_user, username=username, password=password, email=email)
