from pydantic import BaseModel


class AccountCreateReq(BaseModel):
    email: str
    password: str
    name: str
    guardian: str


class ChatCreateTextReq(BaseModel):
    question: str
