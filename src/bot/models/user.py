from . import Base
from sqlalchemy import Column, String, Integer, BigInteger


class User(Base):

    __tablename__ = "bot_users"

    def __init__(self, telegram_handle, account_id, chat_id):
        self.telegram_handle = telegram_handle
        self.account_id = account_id
        self.chat_id = chat_id

    user_id = Column(Integer, primary_key=True)
    telegram_handle = Column(String)
    account_id = Column(BigInteger)
    chat_id = Column(BigInteger)
