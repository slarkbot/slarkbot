from src.bot.services import item_services, hero_services
from src.lib import endpoints
from src.lib import web_scraper
from src import constants
from src.bot.commands import helpers
from telegram.utils.helpers import escape_markdown


def run_suggested_builds_command(update, context):
    if not context.args:
        update.message.reply_markdown_v2(
            constants.MISSING_ARGUMENT_MESSAGE % "/build <hero name or alias>"
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


def run_get_hero_aliases(update, context):
    if not context.args:
        udpate.message.reply_markdown_v2(
            constants.MISSING_ARGUMENT_MESSAGE % "/alias <hero>"
        )

    hero_name_parts = context.args
    hero_name = "".join(hero_name_parts)

    hero = hero_services.get_hero_by_name(hero_name)

    if not hero:
        update.message.reply_markdown_v2(constants.HERO_NOT_FOUND_MESSAGE % hero_name)

    hero_aliases = hero_services.get_hero_aliases_by_hero_id(hero.id)

    aliases = [alias.alias for alias in hero_aliases]

    output = "Aliases\n%s" % "\n".join(aliases)

    output = escape_markdown(output, version=2)

    update.message.reply_markdown_v2(output)


def run_get_hero_counters_command(update, context):
    if not context.args:
        message = escape_markdown(
            constants.MISSING_ARGUMENT_MESSAGE % "/counter <hero or alias>", version=2
        )
        update.message.reply_markdown_v2(message)

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

    counters = web_scraper.get_hero_counters(hero.localized_name)

    if not counters:
        update.message.reply_markdown_v2(
            f"Oops, something went wrong and I don't what happened, try again"
        )

    column_headers = "Hero | Disadvantage | Hero win rate\n"
    output = f"{hero.localized_name.title()} counters\n{column_headers}"

    for counter in counters:
        row = f"{counter[0]} | {counter[1]}% | {counter[2]}%\n"
        output += row

    output = escape_markdown(output, version=2)
    update.message.reply_markdown_v2(output)
