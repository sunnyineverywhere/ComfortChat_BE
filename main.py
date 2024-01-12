import json

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import database
import scheme
from util import gpt_util

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
async def add_chat(req: scheme.ChatCreateTextReq):
    response = gpt_util.get_gpt_answer(question=req.question)

    return json.loads(response)