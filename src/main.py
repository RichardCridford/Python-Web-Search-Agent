from agent.core import run_agent

def main():
    print("Web Search Agent (SERPAPI powered)")
    print("Type 'exit' to quit.\n")

    # As the agent is starting to get more complex, the user input is now handled in main.py whereas in the previous 
    # project it was in the core.py  
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = run_agent(user_input)
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()