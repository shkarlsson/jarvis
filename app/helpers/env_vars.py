# Description: This file is used to load environment variables from the .env file and make them available to the entire project.

import os
from dotenv import load_dotenv

load_dotenv()


def try_float_conversion(value):
    if value.replace(".", "").isdigit() and value.count(".") == 1:
        return float(value)
    else:
        return None


def try_int_conversion(value):
    if value.isdigit():
        return int(value)
    else:
        return None


def try_bool_conversion(value):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        return None


def try_all_conversions(value):
    if try_int_conversion(value) is not None:
        return try_int_conversion(value)

    if try_float_conversion(value) is not None:
        return try_float_conversion(value)

    if try_bool_conversion(value) is not None:
        return try_bool_conversion(value)

    # If no conversion is possible, return the original string value
    return value


env_var = {key: try_all_conversions(value) for key, value in os.environ.items()}

globals().update(env_var)
