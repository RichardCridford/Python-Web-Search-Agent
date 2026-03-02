# Web Search Agent
Web Search Agent (OpenAI Function‑Calling)
This project implements a clean, production‑ready web‑search agent using OpenAI’s function‑calling API. 
The agent reliably calls a web search tool when the user asks for factual, time‑sensitive, or domain‑specific information.
The design focuses on:
- Strict tool usage
- Deterministic behaviour
- Clear separation of concerns
- A reusable agent loop

# Adding a second tool 

## Features
Automatic tool calling
The agent calls the web_search tool whenever the user asks for:
- news
- recent events
- updates
- anything involving a date range (“last 7 days”)
- anything requiring external facts
- anything involving a domain (“from wikipedia.org”)

Deterministic follow‑up behaviour
After the tool runs, the agent is instructed to:
“Answer the user using only the tool result. Do not use internal knowledge.”

This eliminates hallucinations and ensures the final answer is grounded in real search results.








