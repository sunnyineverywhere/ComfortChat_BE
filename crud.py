from sqlalchemy.orm import Session, joinedload
from model import Account, Chat


# account
def find_account_by_email(db: Session, email):
    db_account = db.query(Account).filter(email == Account.email)
    if db_account:
        for account in db_account:
            return account


# chat
def create_chat(db: Session, chat: Chat):
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat