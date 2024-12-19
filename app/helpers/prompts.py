import datetime

from app.tools.load import tool_functions


def get_function_parameters_no_library(func):
    # Get all variable names from the function code object
    varnames = func.__code__.co_varnames

    # The number of positional and keyword-only arguments
    argcount = func.__code__.co_argcount

    # Extract only the positional and keyword-only arguments
    parameters = varnames[:argcount]

    return list(parameters)


def make_tool_descriptions(tool_functions):
    tool_descriptions = []

    for name, func in tool_functions.items():
        desc = func.__doc__
        # Getting the keys of args from the function signature
        args = ", ".join(get_function_parameters_no_library(func))
        tool_descriptions.append(f"{name}({args}) - {desc}")

    return "\n- ".join(tool_descriptions)


tool_descriptions = make_tool_descriptions(tool_functions)

now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

response_fmt = """
{
    "response": str (your message that will be read out loud. Keep it short. Omit if you intend to await the result of a tool call)
    "tool_name": str (the name of the tool),
    "tool_args": dict (the arguments to pass to the tool)
}"""


SYSTEM_PROMPT = f"""You are a home assistant voice bot. You are helping the user with their tasks around the house or answering questions. Keep your answers short. No yapping.

The current time is: {now_str}
                
You can use the following tools:

- {tool_descriptions}

When using a tool, wait until the tool returns a response before saying that the task has been completed.

You have to respond in json format. If no tool is needed, omit the tool key.

THE WHOLE RESPONSE SHOULD BE IN JSON FORMAT:

{response_fmt}
"""

# Printing the prompt to the console
print("SYSTEM PROMPT:")
print("----------------------------")
print(SYSTEM_PROMPT)
