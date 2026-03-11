# Web Search Agent
Web Search Agent (OpenAI Function‑Calling)
This project implements a clean, production‑ready web‑search agent using OpenAI’s function‑calling API. 
The agent reliably calls a web search tool when the user asks for factual, time‑sensitive, or domain‑specific information.
The design focuses on:
- Strict tool usage
- Deterministic behaviour
- Clear separation of concerns
- A reusable agent loop

# Adding a second tool - Summariser

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


## Test Data
Prompt 1 - Test summariser tool directly (no search)

Please summarise this into 3 bullet points:
The sky is blue because of Rayleigh scattering. Short wavelengths scatter more than long ones..

Prompt 2 - Test web search alone (no summariser)
What is the population of Japan?

Prompt 3 - Test tool‑chaining (search → summariser → answer)
Summarise the latest news about renewable energy in the last 7 days.

Prompt 4 - Test “no tool needed” behaviour
Explain what your tools do.

Prompt 5 - Test ambiguous queries (should trigger search)
What happened with SpaceX yesterday?

Prompt 6 - Test summariser after user‑provided text
Here is some text. Summarise it into 5 points:
"Python’s import system is confusing because it only searches the working directory and installed packages."

Prompt 7 - Test failure mode (search returns nothing)
What are the latest updates about the fictional company Zorblax Industries?

Prompt 8 - Test long‑form summarisation after search
Find recent articles about AI safety and summarise the key points.








