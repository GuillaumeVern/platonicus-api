from models.user import User
from pydantic import BaseModel # base python types
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import connector
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, APIRouter, HTTPException, status, Body, Request, Response
from typing import Annotated

SECRET_KEY = "64200080dce3f7c3add3e05032c7821da987ba041de82977e8f528d2b6617c35"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = connector.connect()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str = None, token: str = None):
    result = None
    print(username, password)
    if password is not None:
        try:
            query = "SELECT app_user.email, username, password, token.token FROM app_user LEFT JOIN token ON app_user.email = token.email WHERE username = %s AND password = %s LIMIT 1"
            cursor = db.cursor()
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
        except Exception as e:
            print(e)
    elif token is not None:
        try:
            query = "SELECT app_user.email, username, password, token.token FROM app_user LEFT JOIN token ON app_user.email = token.email WHERE token.token = %s LIMIT 1"
            cursor = db.cursor()
            cursor.execute(query, (token,))
            result = cursor.fetchone()
            cursor.close()
        except Exception as e:
            print(e)
    if result is not None:
        userdb = User(*result)
        return userdb
    else:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    add_access_token_to_user(data["email"], encoded_jwt)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # control
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = authenticate_user(username=username, token=token)
    if user is None:
        raise credentials_exception

    return user

def add_access_token_to_user(email: str, token: str):
    try:
        query = "INSERT INTO token (email, token) VALUES (%s, %s)"
        cursor = db.cursor()
        cursor.execute(query, (email, token))
        db.commit()
        cursor.close()
    except Exception as e:
        print(e)
    

@router.post("/", tags=["auth"], response_model=Token)
async def login_for_access_token(request: Request, response: Response) -> Token:
    form_data = await request.json()

    user = authenticate_user(username=form_data["username"], password=form_data["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = user.dict()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.put("/", tags=["auth"], response_model=Token)
async def register(request: Request, response: Response) -> Token:
    form_data = await request.json()
    try:
        query = "INSERT INTO app_user (email, username, password) VALUES (%s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(query, (form_data["username"], form_data["username"], form_data["password"]))
        db.commit()
        cursor.close()
    except Exception as e:
        print(e)
    return await login_for_access_token(request, response)
