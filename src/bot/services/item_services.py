from src.bot.models.item import Item
from src.bot.models.sessions import create_session


def get_item_by_id(item_id):
    session = create_session()
    return session.query(Item).filter(Item.id == item_id).first()


def get_item_by_name(item_name):
    session = create_session()
    return session.query(Item).filter(Item.item_name == item_name).first()
