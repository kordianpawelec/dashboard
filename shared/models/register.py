from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    fullname: str
    password: str
    token: str
    email: str