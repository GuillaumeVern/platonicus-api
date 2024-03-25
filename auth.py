from models.user import User
from pydantic import BaseModel # base python types
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import connector
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, APIRouter, HTTPException, status
from typing import Annotated

SECRET_KEY = "64200080dce3f7c3add3e05032c7821da987ba041de82977e8f528d2b6617c35"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = connector.connect()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str = None, token: str = None):
    if password is not None or token is not None:
        query = "SELECT app_user.email, username, password, token.token FROM app_user LEFT JOIN token ON app_user.email = token.email WHERE password = %s OR token = %s LIMIT 1"
        cursor = db.cursor()
        cursor.execute(query, (password, token))
        result = cursor.fetchone()
        cursor.close()
    if result is not None:
        print(result)
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
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        # control
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
        user = authenticate_user(email=email, token=token)
        if user is None:
            raise credentials_exception

        return user

@router.post("/", tags=["auth"], response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
