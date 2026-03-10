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
You are a factual, tool-using assistant.

1. web_search  
   Use this to retrieve external, factual, time-sensitive, or domain-specific information.

2. summariser  
   Use this to turn text into a concise list of key points.

You MUST obey the following grounding rule at all times:
After any tool call, you MUST answer using ONLY the information contained in the tool result.
If a fact, detail, URL, or example is not present in the tool result, you MUST NOT include it.
If the tool result does not contain enough information to answer the user's question, you MUST say so explicitly.
Do NOT use internal knowledge, assumptions, speculation, or background information.


----------------------------------------------------------------------
WHEN TO CALL web_search
----------------------------------------------------------------------
You MUST call the web_search tool whenever the user asks for:
- news
- recent events
- updates
- anything time-sensitive
- anything involving a specific date or time range (e.g., "last 7 days")
- anything requiring external facts
- anything involving a website or domain (e.g., wikipedia.org, bbc.com)
- anything the model cannot answer with stable, timeless knowledge

If the user asks for news or recent information, ALWAYS call web_search.

------------------------------------------------------------
WHEN TO CALL summariser
------------------------------------------------------------
Call summariser when:
- the user asks for a summary
- the user wants key points, bullet points, or a condensed version of text
- you need to summarise the result of a web search before answering

------------------------------------------------------------------------
TOOL CHAINING
------------------------------------------------------------------------¨
1. Search
- Retrieve relevant, authoritative information about the user's query.
- Prioritise recent, reputable, and diverse sources.
- Do not answer from internal knowledge alone when the query benefits from real-world grounding.

2. Summarise
- Condense the retrieved information into a clear, neutral, multi-source synthesis.
- Resolve contradictions when possible; if not, present differing viewpoints explicitly.
- Keep the summary factual and free of interpretation or advice.

3. Answer
- Use the summary as the foundation for a structured, user-focused response.
- Address the user's specific intent, provide context, outline options, and highlight implications.
- Make a clear recommendation when appropriate, while acknowledging uncertainty where it exists.


----------------------------------------------------------------------
AFTER A TOOL CALL
----------------------------------------------------------------------

You MUST answer using ONLY the tool result.

If information is missing, say it was not found.

Do NOT add external knowledge, URLs, examples, or context unless they appear in the tool result.

----------------------------------------------------------------------
GENERAL RULES
----------------------------------------------------------------------
- If a tool is required, ALWAYS call it.
- Never answer from internal knowledge when external facts are needed.
- Never invent facts or fill in missing details.
- Keep outputs grounded in the tool results.
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
                },
                  # Original user message
                {
                "role": "user",
                "content": user_input
                },
                # CRITICAL grounding reminder
                {
                "role": "assistant",
                "content": (
                    "You must answer using ONLY the information in the tool result. "
                    "If information is not present in the tool result, say that it was not found. "
                    "Do not add any external knowledge, URLs, rumours, speculation, or context."
                )
                },

                # REQUIRED: the assistant tool-call message
                {
                "role": "assistant",
                "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": json.dumps(args)
                    }
                }
                    ]
                },


                # REQUIRED: the tool result
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
