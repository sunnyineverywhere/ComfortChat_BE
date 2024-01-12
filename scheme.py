from pydantic import BaseModel
from model import Chat


class AccountSignInfo(BaseModel):
    email: str
    password: str

class AccountCreateReq(BaseModel):
    email: str
    password: str
    name: str
    guardian: str


class ChatCreateTextReq(BaseModel):
    question: str


class ChatResponse(BaseModel):
    id: int
    question: str
    answer: str
    isOkay: bool
    keyword: str