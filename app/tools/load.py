import random

from app.tools.keep import (
    add_to_shopping_list,
    check_shopping_list,
    remove_from_shopping_list,
)
from app.tools.timer import set_timer, get_timers, cancel_timer
from app.tools.weather import get_weather
from app.tools.es import get_zigbee_device_names


def random_number(x, y):
    """Generate a random number between x and y, inclusive."""
    return random.randint(x, y)


# Mapping of function names to functions
tool_functions = {
    "add_to_shopping_list": add_to_shopping_list,
    "check_shopping_list": check_shopping_list,
    "remove_from_shopping_list": remove_from_shopping_list,
    "set_timer": set_timer,
    "get_timers": get_timers,
    "cancel_timer": cancel_timer,
    "random_number": random_number,
    "get_weather": get_weather,
    "get_zigbee_device_names": get_zigbee_device_names,
}


def use_tool(name, args=None):
    # Getting the function from the dictionary
    func = tool_functions.get(name)

    try:
        # Check if the function exists, then call it
        if func:
            if args is not None:
                return func(**args)
            else:
                return func()
        else:
            print(f"Tool '{name}' not found.")
            return "Tool not found."
    except Exception as e:
        print(f"Error using tool '{name}': {e}")
        return f"Error using tool '{name}': {e}"
