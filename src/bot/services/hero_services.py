from src.bot.models.sessions import create_session
from src.bot.models.hero import Hero
from src.bot.models.hero_alias import HeroAlias


def get_hero_by_name(hero_name):
    session = create_session()
    return session.query(Hero).filter(Hero.localized_name == hero_name.lower()).first()


def get_hero_by_id(hero_id):
    session = create_session()
    return session.query(Hero).filter(Hero.id == hero_id).first()


def get_hero_alias_by_name(hero_alias):
    session = create_session()
    return (
        session.query(HeroAlias).filter(HeroAlias.alias == hero_alias.lower()).first()
    )


def get_hero_aliases_by_hero_id(hero_id):
    session = create_session()
    return session.query(HeroAlias).filter(HeroAlias.hero_id == hero_id).all()

def get_hero_id_by_name_or_alias(hero_name):
    try:
        hero = get_hero_by_name(hero_name)
        hero_id = hero.id
    except:
        hero = get_hero_alias_by_name(hero_name)
        hero_id = hero.hero_id
    
    return hero_id