from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from src.auth.auth import JWTBearer
from src.auth.utils import generate_token, get_current_user
from src.auth.models import UserPydantic, User, UserInPydantic, UserInfo
from passlib.hash import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/add_info", dependencies=[Depends(JWTBearer())])
async def add_info(current_user: UserInPydantic = Depends(get_current_user)): # type: ignore
    return current_user

@router.get("/user", response_model=UserPydantic)
async def get_login(user_id: int):
    user_obj = await UserInfo.get(id=user_id)
    return user_obj

@router.get('/users/signup')
async def get_user_login():
    return 'regpage'

@router.post("/user/signup")
async def create_user(user: UserInPydantic, userinf: UserPydantic, request: Request): # type: ignore
    try:
        data = await request.json()
        user = UserInPydantic(**data["user"])
        userinfo = UserPydantic(**data["userinf"])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    existing_user = await User.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)
    user_obj = await User.create(email=user.email, password=hashed_password)
    await user_obj.save()


    userinfo = await UserInfo.create(user_id = user_obj.id, FirstName = userinfo.FirstName, SecondName = userinfo.SecondName, SurName = userinfo.SurName)
    await userinfo.save()

    return await generate_token(user.email, user.password)

@router.get('/users/login')
async def get_user_login():
    return 'loginpage'

@router.post('/users/login')
async def user_login(user: UserInPydantic): # type: ignore
    return await generate_token(user.email, user.password)
