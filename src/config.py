import os

from src.constants import ENVIRONMENT_VARIABLES_CONFIG
from src.exceptions import MissingEnvironmentVariableException


def check_config():
    for (
        environment_variable,
        environment_variable_settings,
    ) in ENVIRONMENT_VARIABLES_CONFIG.items():
        required = environment_variable_settings["required"]
        environment_variable_value = os.getenv(environment_variable)

        if not environment_variable_value and required:
            raise MissingEnvironmentVariableException(environment_variable)
