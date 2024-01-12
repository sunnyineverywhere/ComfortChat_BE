import json

from fastapi import FastAPI, Depends, UploadFile
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import shutil
import os
import scheme
from model import Account, Chat
from util import gpt_util, whisper_util

UPLOAD_DIR = "/tmp"
import crud

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.redirect_slashes = False


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/hello")
async def root():
    return {"message": "Hello! We are ComfortChat!"}


@app.post("/chats/text")
async def add_chat(req: scheme.ChatCreateTextReq, db: Session = Depends(get_db)):
    response = json.loads(gpt_util.get_gpt_answer(question=req.question))
    chat = crud.create_chat(db=db, chat=Chat(
        question=req.question,
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
