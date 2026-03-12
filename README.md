# Web Search Agent
Web Search Agent (OpenAI Function‑Calling)
This project implements a clean, production‑ready web‑search agent using OpenAI’s function‑calling API. 
The agent reliably calls a web search tool when the user asks for factual, time‑sensitive, or domain‑specific information.
The design focuses on:
- Strict tool usage
- Deterministic behaviour
- Clear separation of concerns
- A reusable agent loop

## Features
Automatic tool calling
The agent calls the web_search tool whenever the user asks for:
- news
- recent events
- updates
- anything involving a date range (“last 7 days”)
- anything requiring external facts
- anything involving a domain (“from wikipedia.org”)

### Deterministic follow‑up behaviour
After the tool runs, the agent is instructed to:
“Answer the user using only the tool result. Do not use internal knowledge.”

This eliminates hallucinations and ensures the final answer is grounded in real search results.

# Adding a second tool - Summariser
The summariser is a simple, deterministic tool that takes a block of text and returns a concise set of bullet‑point key insights. It is used to condense either:
• 	text provided directly by the user
• 	text returned from a web search (as part of tool‑chaining)
The summariser never adds new information. It only restructures and condenses what it receives.

## When the Agent Uses the Summariser
The agent automatically calls the summariser when:
- the user explicitly asks for a summary
- the user requests “bullet points”, “key points”, or a “condensed version”
- the agent performs a web search and the user wants a summary of the search results
- the user asks for a summary across multiple turns
(e.g., “Summarise this” → user sends text in next message)
The agent does not call the summariser for general questions or conversational replies.

# Tool‑Chaining (Search → Summariser → Answer)
The agent supports automatic multi‑step tool‑chaining when the user asks for a summary of information that must first be retrieved from the web.

## How tool‑chaining works
When the user asks for something like:
“Summarise the latest news about renewable energy in the last 7 days.”

the agent performs the following sequence:

- web_search
The agent detects that the request requires external, time‑sensitive information and calls the web search tool.

- summariser
After receiving the search results, the agent detects that the user wants a summary and calls the summariser tool to condense the search output into bullet‑points.

- Final grounded answer
The agent returns a final answer using only the summariser output, ensuring the response is factual, hallucination‑free while still staying concise. 

### When tool‑chaining is triggered
Tool‑chaining occurs automatically when:
- the user asks for a summary of information that must be retrieved externally
- the user asks for “latest”, “recent”, or date‑range‑based summaries
- the user requests a summary of news, events, or updates
- the user asks for a summary of something that cannot be answered from internal knowledge

### Grounding guarantee
After tool‑chaining:
- The final answer is grounded only in the summariser output.
- No additional facts or assumptions are added.
- If the search results lack information, the agent explicitly states that.



# Test Data prompts
Prompt 1 - Test the summariser tool directly (no search)

"Please summarise this into 3 bullet points:
The sky is blue because of Rayleigh scattering. Short wavelengths scatter more than long ones.."

Prompt 2 - Test the web search tool alone (no summariser)
"What is the population of Japan?"

Prompt 3 - Test tool‑chaining (search → summariser → answer)
"Summarise the latest news about renewable energy in the last 7 days".

Prompt 4 - Test “no tool needed” behaviour
"Explain what your tools do".

Prompt 5 - Test ambiguous queries (this should trigger the web search tool)
"What happened with SpaceX yesterday?"

Prompt 6 - Test summariser after with user‑provided text
"Here is some text. Summarise it into 5 points:"
"Python’s import system is confusing because it only searches the working directory and installed packages."

Prompt 7 - Test failure mode (search returns nothing)
"What are the latest updates about the fictional company Zorblax Industries?"

Prompt 8 - Test long‑form summarisation after search
"Find recent articles about AI safety and summarise the key points".








