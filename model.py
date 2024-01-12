
from sqlalchemy import Boolean, Column, TIMESTAMP, func, ForeignKey, Date, DateTime, String, BigInteger, func

from sqlalchemy.orm import relationship

from database import Base


class Account(Base):
    __tablename__ = "account"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    guardian = Column(String)



class Chat(Base):
    __tablename__ = "chat"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    question = Column(String)
    answer = Column(String)
    keyword = Column(String)
    isOkay = Column(Boolean)
    Column(TIMESTAMP, server_default=func.current_timestamp())
    account = Column(BigInteger, ForeignKey('account.id'))
    accountEntity = relationship("Account", backref="a")
