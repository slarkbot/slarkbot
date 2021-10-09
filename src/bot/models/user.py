from sqlalchemy.sql.sqltypes import DateTime
from . import Base
from sqlalchemy import Column, String, Integer, BigInteger


class User(Base):

    __tablename__ = "bot_users"

    __mapper_args__ = {
        "order_by":updated_at
    }

    def __init__(self, telegram_handle, account_id, chat_id):
        self.telegram_handle = telegram_handle
        self.account_id = account_id
        self.chat_id = chat_id
        self.updated_at = updated_at

    user_id = Column(Integer, primary_key=True)
    telegram_handle = Column(String)
    account_id = Column(BigInteger)
    chat_id = Column(BigInteger)
    updated_at = Column(DateTime)
