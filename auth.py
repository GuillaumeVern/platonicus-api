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

def authenticate_user(username: str = None, password: str = None, token: str = None):
    if token is not None:
        token = token.split("Bearer ")[1]
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = token_data["username"]
        password = token_data["password"]

    result = None
    if password is not None:
        try:
            query = "SELECT id_user, username, password, email FROM app_user WHERE username = %s AND password = %s LIMIT 1"
            cursor = db.cursor()
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
        except Exception as e:
            print("authenticate_user: ", e)
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
    add_access_token_to_user(data["username"], encoded_jwt)
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
        
    user = authenticate_user(token=token)
    if user is None:
        raise credentials_exception

    return user

def add_access_token_to_user(username: str, token: str):
    try:
        user = get_user(username)
        if user is not None:
            return
        # insert token
        query = "INSERT INTO token (id_user, token) VALUES (%s, %s)"
        cursor = db.cursor()
        cursor.execute(query, (user_id, token))
        db.commit()
        cursor.close()
    except Exception as e:
        print("add_access_token_to_user: ", e)
    
def get_user(username: str):
    try:
        query = "SELECT * FROM app_user WHERE username = %s LIMIT 1"
        cursor = db.cursor()
        cursor.execute(query, [username])
        result = cursor.fetchone()
        cursor.close()
        return User(*result)
    except Exception as e:
        print("get_user: ", e)
        return None

@router.post("/login", tags=["auth"], response_model=Token)
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

@router.post("/token", tags=["auth"], response_model=Token)
async def login_with_token(request: Request, response: Response) -> Token:
    form_data = await request.json()
    token_data = jwt.decode(form_data["token"], SECRET_KEY, algorithms=[ALGORITHM])
    user = authenticate_user(username=token_data["username"], password=token_data["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = user.dict()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
    



@router.post("/register", tags=["auth"], response_model=Token)
async def register(request: Request, response: Response) -> Token:
    form_data = await request.json()
    try:
        user = get_user(form_data["username"])
        if user is not None:
            response.status_code = 401 # obfuscation
            return response
        query = "INSERT INTO app_user (username, password) VALUES (%s, %s)"
        cursor = db.cursor()
        cursor.execute(query, (form_data["username"], form_data["password"]))
        db.commit()
        cursor.close()
    except Exception as e:
        print("register: ", e)
    response.status_code = 201
    return response
