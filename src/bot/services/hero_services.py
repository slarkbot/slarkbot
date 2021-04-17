from src.bot.models.sessions import create_session
from src.bot.models.hero import Hero
from src.bot.models.hero_alias import HeroAlias


def get_hero_by_name(hero_name):
    session = create_session()
    output = session.query(Hero).filter(Hero.localized_name.ilike(hero_name)).first()
    session.close()
    return output


def get_hero_by_id(hero_id):
    session = create_session()
    output = session.query(Hero).filter(Hero.id == hero_id).first()
    session.close()
    return output


def get_hero_alias_by_name(hero_alias):
    session = create_session()
    output = session.query(HeroAlias).filter(HeroAlias.alias.ilike(hero_alias)).first()
    session.close()
    return output


def get_hero_aliases_by_hero_id(hero_id):
    session = create_session()
    output = session.query(HeroAlias).filter(HeroAlias.hero_id == hero_id).all()
    session.close()
    return output
