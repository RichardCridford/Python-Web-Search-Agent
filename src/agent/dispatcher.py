#dispatcher.py
from agent.tools.web_search import web_search

#-------------------------------------------------------------------
# Dispatcher - a place to register tools and how that tool is called
#-------------------------------------------------------------------


TOOL_FUNCTIONS = {
    "web_search": web_search,
}

def dispatch_tool_call(name, arguments):
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return f"Unknown tool: {name}"
    return func(**arguments)
