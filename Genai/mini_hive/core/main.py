from services.agent_service import run_agent
from pprint import pprint

if __name__ == "__main__":
    while True:
        user_input = input("\nAsk something: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        result = run_agent(user_input)
        print("\n[Final Result]\n")
        pprint(result)
        # print("\n" + result)