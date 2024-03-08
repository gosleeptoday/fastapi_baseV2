from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    email: str
    roleid: int

class UserCreate(BaseModel):
    email: str
    password: str
    
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    id: int
    email: str
