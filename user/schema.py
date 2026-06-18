from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import timedelta

class SignUpSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    username: str = Field(max_length=50)
    email: EmailStr
    phone_number: str = Field(max_length=20)
    password: str = Field(min_length=8)
    conf_password: str = Field(min_length=8)

    model_config = {
        'from_attribute': True,
        'json_schema_extra': {
            'example': {
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'johndoe',
                'email': 'usa20070302@gmail.com',
                'phone_number': '+998901234567',
                'password': 'password123',
                'conf_password': 'password123'
            }
        }
    }

class LoginSchema(BaseModel):
    username: str
    password: str = Field(min_length=8)

    class Config:
        from_attribute=True

class ProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(max_length=50)
    last_name: Optional[str] = Field(max_length=50)
    username: str
    email: Optional[EmailStr]
    phone_number: Optional[str] = Field(max_length=20)

    model_config = {
        'from_attribute': True,
        'json_schema_extra': {
            'example': {
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'johndoe',
                'email': 'usa20070302@gmail.com',
                'phone_number': '+998901234567'
            }
        }
    }

class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str
    conf_password: str

    class Config:
        from_attribute=True

class Settings(BaseModel):
    authjwt_secret_key: str = "6baee8af421b2cbea062847e4bf9678bc1ef773e7684e15dbe9605874aaada45"
    authjwt_access_token_expires: timedelta = timedelta(minutes=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=1)