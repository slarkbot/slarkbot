from functools import wraps
from src import constants
from src.bot.services import hero_services


def require_hero_args(func):
    """
    Validates that a hero name or hero alias was given as args,
    and retrieves the hero from the database. Fails if no
    hero was given or if a hero doesn't exist.
    """

    @wraps(func)
    def inner(update, context):
        if not context.args:
            update.message.reply_markdown_v2(constants.MISSING_HERO_ARGUMENT_MESSAGE)
            return

        hero_name_parts = context.args

        hero_name = " ".join(hero_name_parts)

        hero = hero_services.get_hero_by_name(hero_name)

        if not hero:
            hero_alias = hero_services.get_hero_alias_by_name(hero_name)

            if hero_alias:
                hero = hero_services.get_hero_by_id(hero_alias.hero_id)

        if not hero:
            update.message.reply_markdown_v2(
                constants.HERO_NOT_FOUND_MESSAGE % hero_name
            )

        func(update, hero)

    return inner
