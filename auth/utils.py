from datetime import datetime, timedelta
import time
from jwt import PyJWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from src.auth.models import User, UserInfo

JWT_SECRET = "test"
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_IN_SECONDS = 365 * 24 * 60 * 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except PyJWTError:
        raise credentials_exception

async def authenticate_user(email: str, password: str):
    user = await User.get(email=email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user    

async def generate_token(email: str, password: str):
    user = await authenticate_user(email, password)
    if user:
        user_info = await UserInfo.get(user_id=user.id)

        expiration_time = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRE_IN_SECONDS)
        token_data = {
            'id': user.id,
            'FirstName': user_info.FirstName,
            'SecondName': user_info.SecondName,
            'SurName': user_info.SurName,
            'exp': expiration_time
        }
        token = jwt.encode(token_data, JWT_SECRET)
        return {'status': 'success', 'access_token': token}
    else: 
        return {'status': 'error'}

async def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}