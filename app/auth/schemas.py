from pydantic import BaseModel, EmailStr, constr

class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    first_name: str = None
    last_name: str = None

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
