import datetime
import json

from sqlalchemy import or_

from sqlalchemy.orm import Session, joinedload
from model import Account
import random


# account
def find_account_by_email(db: Session, email):
    db_account = db.query(Account).filter(email == Account.email)
    if db_account:
        for account in db_account:
            return account