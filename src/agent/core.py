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

You MUST obey the following grounding rule at all times:

After any tool call, you MUST answer using ONLY the information contained in the tool result.
If a fact, detail, URL, source, or example is not present in the tool result, you MUST NOT include it.
You MUST NOT use internal knowledge, prior knowledge, or assumptions.
You MUST NOT add context, speculation, rumours, or helpful background information.
If the tool result does not contain enough information to answer the user's question, you MUST say so explicitly.


Your job is to decide when to call tools and to return grounded, non-hallucinated answers.

You have access to two tools:

1. web_search  
   Use this to retrieve external, factual, time-sensitive, or domain-specific information.

2. extract_facts  
   Use this to convert unstructured text into structured JSON according to a user-defined schema.

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

You MUST NOT answer from your own knowledge when a search is required.

Always extract:
- query: the main topic
- recency_days: convert any time references (e.g., "last week", "past 7 days")
- domains: any domains the user mentions

If the user asks for news or recent information, ALWAYS call web_search.

----------------------------------------------------------------------
WHEN TO CALL extract_facts
----------------------------------------------------------------------

Call extract_facts when:

- The user requests structured information (lists, tables, timelines, metadata, summaries)
- The search results contain unstructured text that must be converted into a specific format
- The user provides a schema or clearly implies a structured output
- You need to transform raw text into clean JSON before answering

Examples:
- “Give me a timeline of events…”
- “Extract all dates and names…”
- “Turn this into a structured list…”
- “Summarise this into JSON with fields X, Y, Z…”

The schema must be a JSON-serialisable string describing the desired structure.

----------------------------------------------------------------------
TOOL CHAINING
----------------------------------------------------------------------

You may call extract_facts AFTER web_search if:

- The search results need structuring
- The user wants structured output
- The user wants a timeline, list, table, or JSON

Do NOT call extract_facts before web_search unless the user directly provides the text.

----------------------------------------------------------------------
AFTER A TOOL CALL
----------------------------------------------------------------------

After a tool call, you will receive the tool result.

You MUST answer the user using ONLY the tool result provided.
Do NOT use internal knowledge.
Do NOT add information that was not present in the tool result.

If information is not present in the tool result, you MUST say that the information was not found. 
Do NOT add external sources, URLs, examples, or context unless they appear in the tool result.

You are not allowed to mention or reference any website, URL, or source unless it appears in the tool result.

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
