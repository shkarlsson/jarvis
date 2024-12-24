from app.tools.keep import (
    add_to_shopping_list,
    check_shopping_list,
    remove_from_shopping_list,
    test_shopping_list_tools,
)
from app.tools.timer import set_timer, get_timers, cancel_timer
from app.tools.weather import get_weather, test_weather_tool
from app.tools.es import get_zigbee_device_names
from app.tools.random_number import generate_random_number


shopping_list_test_results = test_shopping_list_tools()
weather_test_results = test_weather_tool()
# Mapping of function names to functions
tool_functions_config = {
    "add_to_shopping_list": {
        "function": add_to_shopping_list,
        "dependency": shopping_list_test_results,
    },
    "check_shopping_list": {
        "function": check_shopping_list,
        "dependency": shopping_list_test_results,
    },
    "remove_from_shopping_list": {
        "function": remove_from_shopping_list,
        "dependency": shopping_list_test_results,
    },
    "set_timer": {
        "function": set_timer,
        "dependency": True,
    },
    "get_timers": {
        "function": get_timers,
        "dependency": True,
    },
    "cancel_timer": {
        "function": cancel_timer,
        "dependency": True,
    },
    "generate_random_number": {
        "function": generate_random_number,
        "dependency": True,
    },
    "get_weather": {
        "function": get_weather,
        "dependency": weather_test_results,
    },
    "get_zigbee_device_names": {
        "function": get_zigbee_device_names,
        "dependency": weather_test_results,
    },
}

tool_functions = {}
skipped_tools = []
for name, config in tool_functions_config.items():
    if not config["dependency"]:
        skipped_tools.append(name)
        continue
    tool_functions[name] = config["function"]

if skipped_tools:
    print(f"Skipped tools:\n- {'\n- '.join(skipped_tools)}")


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
