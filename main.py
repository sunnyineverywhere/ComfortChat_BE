from fastapi import FastAPI
from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import database
import scheme

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


@app.post("/user")
async def signup(new_user: scheme.AccountCreateReq, db: Session = Depends(get_db)):
    user = crud.find_account_by_email(email=new_user.email, db=db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    #회원 가입
    crud.create_user(new_user, db)

    return HTTPException(status_code=status.HTTP_200_OK, detail="Signup successful")



