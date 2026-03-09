#schema.py

#--------------------------------------------------------------------------------
# Tool Schema - this section is written in JSON so the agent can understand it
#--------------------------------------------------------------------------------
TOOL_SCHEMAS =  [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the web for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query or topic the user wants information about."
                        },          
                        "recency_days": {
                        "type": "integer", 
                        "nullable": True,
                        "description": "Limit results to the past N days. Optional."
                        },
                        "domains": {
                            "type": "array",
                            "items": {"type": "string"},
                            "nullable": True,
                            "description": "Restrict search to specific domains (e.g., ['ign.com']). Optional."
                        }
                    },
                "required": ["query"]
            }
        }
    },

        {
        "type": "function",
        "function": {
            "name": "summariser",
            "description": "Summarises raw text into concise bullet points.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The raw text to summarise."
                    },
                    "max_points": {
                        "type": "integer",
                        "description": "Maximum number of bullet points to return.",
                        "default": 5
                    }
                },
                "required": ["text"]
            }
        }
    }


]