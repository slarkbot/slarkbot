from src.bot.services import item_services, hero_services
from src.lib import endpoints
from src import constants
from src.bot.commands import helpers


def run_suggested_builds_command(update, context):
    if not context.args:
        update.message.reply_markdown_v2(
            "No arguments given\! Try `/winrate <hero name>` or `/winrate <username> <hero name>`"
        )

    hero_name_parts = context.args

    hero_name = "".join(hero_name_parts)

    hero = hero_services.get_hero_by_name(hero_name)

    if not hero:
        hero_alias = hero_services.get_hero_alias_by_name(hero_name)

        if hero_alias:
            hero = hero_services.get_hero_by_id(hero_alias.hero_id)

    if not hero:
        update.message.reply_markdown_v2(
            f"I couldn't find a hero by the name {hero_name} D:"
        )

    response, status_code = endpoints.get_hero_item_popularity(hero.id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = helpers.create_suggested_build_message(
        hero.localized_name, response
    )
    update.message.reply_markdown_v2(output_message)
