# core.py
import json
from agent.dispatcher import dispatch_tool_call
from agent.tools.schema import TOOL_SCHEMAS
from openai import OpenAI

client = OpenAI()

#----------------------------------------------------------------
# System Prompt
#----------------------------------------------------------------

SYSTEM_PROMPT ="""
You are a web-search assistant.

You MUST call the web_search tool whenever the user asks for:
- news
- recent events
- updates
- anything time-sensitive
- anything involving a specific date or time range (e.g., "last 7 days")
- anything requiring external facts
- anything involving a website or domain (e.g., wikipedia.org, bbc.com)
- anything the model cannot answer with stable, timeless knowledge

You MUST NOT answer from your own knowledge when a search is required.

Always extract:
- query: the main topic
- recency_days: convert any time references (e.g., "last week", "past 7 days")
- domains: any domains the user mentions

If the user asks for news or recent information, ALWAYS call the tool.
"""

# -----------------------------------------------------------------------------
# Agent Loop 
#-----------------------------------------------------------------------------
def run_agent(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {"role": "user", "content": user_input}
                ],
        tools=TOOL_SCHEMAS,
        tool_choice="auto"
        
        # used for debugging to force the Agent to use the tool
        #tool_choice={
            #"type": "function",
            #"function": {"name": "web_search"}
                    #}
)

    message = response.choices[0].message
    # this for debugging to see if the tool is called
    print("RAW MODEL MESSAGE:", message)

    # ---------------------------------------------------------------------
    # If the model wants to call a tool
    # ---------------------------------------------------------------------
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # Execute the tool via dispatcher
        tool_result = dispatch_tool_call(name, args)

        # Second model call: send tool result back
        followup = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT 
                      + "\n\nYou MUST answer the user using ONLY the tool result provided. "
                      "Do NOT use internal knowledge."


                },
                message,  # the tool call
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                }
            ]
        )

        return followup.choices[0].message.content

    # ---------------------------------------------------------------------
    # If no tool was called, return the model's normal message
    # ---------------------------------------------------------------------
    return message.content or "[No content returned]"
