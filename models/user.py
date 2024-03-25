from pydantic import BaseModel

class User(BaseModel):
    email: str
    username: str | None = None
    password: str | None = None
    token: str | None = None

    def __init__(self, email: str, username: str | None = None, password: str | None = None, token: str | None = None):
        super().__init__(email=email, username=username, password=password, token=token)
