
from functools import wraps

from src.bot.services import hero_services


def require_hero_args(func):
    @wraps(func)
    def inner(update, context):
        if not context.args:
            update.message.reply_markdown_v2(
                constants.MISSING_ARGUMENT_MESSAGE % "/build <hero name or alias>"
            )

        hero_name_parts = context.args

        hero_name = " ".join(hero_name_parts)

        hero = hero_services.get_hero_by_name(hero_name)

        if not hero:
            hero_alias = hero_services.get_hero_alias_by_name(hero_name)

            if hero_alias:
                hero = hero_services.get_hero_by_id(hero_alias.hero_id)

        if not hero:
            update.message.reply_markdown_v2(
                f"I couldn't find a hero by the name {hero_name} D:"
            )

        func(update, hero)

    return inner
