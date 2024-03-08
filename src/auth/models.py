from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from passlib.hash import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"

class UserInfo(Model):
    id = fields.IntField(pk=True, index=True)
    FirstName = fields.CharField(max_length=255, null=False)
    SecondName = fields.CharField(max_length=255, null=False)
    SurName = fields.CharField(max_length=255, null=False)
    user_id = fields.IntField(null=False, unique=True)

class User(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(max_length=255, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

UserPydantic = pydantic_model_creator(UserInfo, name="User", exclude_readonly=True)
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserPydanticList = pydantic_queryset_creator(User)