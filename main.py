import json

from fastapi import FastAPI, Depends, UploadFile, APIRouter, Depends, status, HTTPException, Response, Request, Header
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import shutil
import os
import scheme
from model import Account, Chat
from util import gpt_util, whisper_util, jwt_util, mail_util
import bcrypt
from fastapi.responses import JSONResponse
import crud

UPLOAD_DIR = "/tmp"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.redirect_slashes = False


async def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/hello")
async def root():
    return {"message": "Hello! We are ComfortChat!"}


@app.post("/accounts/signup")
async def signup(new_user: scheme.AccountCreateReq, db: Session = Depends(get_db)):
    user = crud.find_account_by_email(email=new_user.email, db=db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    # 회원 가입
    crud.create_user(new_user, db)

    return HTTPException(status_code=status.HTTP_200_OK, detail="Signup successful")


@app.post("/accounts/signin")
async def account_sign_in(req: scheme.AccountSignInfo, db: Session = Depends(get_db)):
    account = crud.find_account_by_email(email=req.email, db=db)
    if not bcrypt.checkpw(req.password.encode('utf-8'), account.password.encode('utf-8')):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Your email or password is not valid."})
    access_token, refresh_token = jwt_util.create_jwt(account.id)
    return {
        "message": "Sign In Request Successes",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@app.post("/chats/text")
async def add_chat(req: scheme.ChatCreateTextReq, Authorization: str = Header(default=None),
                   db: Session = Depends(get_db)):
    account_id = jwt_util.decode_jwt(Authorization)

    response = json.loads(gpt_util.get_gpt_answer(question=req.question))
    chat = crud.create_chat(db=db, chat=Chat(
        question=req.question,
        answer=response["answer"],
        keyword=response["keyword"],
        isOkay=response["isOkay"],
        account=account_id
    ))

    if account_id:
        await mail_util.send_email(
            receiver=crud.find_account(db, account_id).guardian,
            chat=chat
        )

    return scheme.ChatResponse(
        id=chat.id,
        question=chat.question,
        answer=chat.answer,
        isOkay=chat.isOkay,
        keyword=chat.keyword
    )


@app.post("/chats/voice")
async def add_chat_voice(file: UploadFile, db: Session = Depends(get_db)):
    filename = file.filename
    file_obj = file.file
    upload_name = os.path.join(UPLOAD_DIR, filename)
    upload_file = open(upload_name, 'wb+')
    shutil.copyfileobj(file_obj, upload_file)
    upload_file.close()

    question = whisper_util.translate_answer_audio(file=upload_name)
    response = json.loads(gpt_util.get_gpt_answer(question=question))

    chat = crud.create_chat(db=db, chat=Chat(
        question=question,
        answer=response["answer"],
        keyword=response["keyword"],
        isOkay=response["isOkay"]
    ))

    return scheme.ChatResponse(
        id=chat.id,
        question=chat.question,
        answer=chat.answer,
        isOkay=chat.isOkay,
        keyword=chat.keyword
    )
