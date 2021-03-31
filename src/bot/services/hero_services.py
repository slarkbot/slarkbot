from src.bot.models.sessions import create_session
from src.bot.models.hero import Hero


def get_hero_by_name(hero_name):
    session = create_session()
    return session.query(Hero).filter(Hero.localized_name == hero_name).first()


def get_hero_by_id(hero_id):
    session = create_session()
    return session.query(Hero).filter(Hero.id == hero_id).first()
