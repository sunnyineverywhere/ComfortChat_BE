from sqlalchemy.orm import Session, joinedload
from scheme import AccountCreateReq
from passlib.context import CryptContext

from model import Account, Chat

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# account
def find_account_by_email(db: Session, email: str):
    db_account = db.query(Account).filter(email == Account.email)
    if db_account:
        for account in db_account:
            return account


def create_user(new_user: AccountCreateReq, db: Session):
    user = Account(
        email=new_user.email,
        password=pwd_context.hash(new_user.password),
        name=new_user.name,
        guardian=new_user.guardian
    )
    db.add(user)
    db.commit()


# chat
def create_chat(db: Session, chat: Chat):
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat
