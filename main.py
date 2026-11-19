
from agent.agent import run_agent


def main():

    print("=" * 45)
    print("              MASTERCODE")
    print("          AI Coding Assistant")
    print("=" * 45)

    print("\nWelcome! I am MasterCode.")
    print("I can read, create and execute Python files.")
    print("\nType 'exit' or 'quit' to close MasterCode.")

    while True:

        print("\n" + "-" * 45)

        user_prompt = input("You: ").strip()

        if user_prompt.lower() in ["exit", "quit"]:
            print("\nMasterCode: Goodbye!")
            break

        if not user_prompt:
            print("Please enter a request.")
            continue

        try:
            run_agent(user_prompt)

        except Exception as error:
            print("\nMasterCode encountered an error.")
            print("Error:", error)


if __name__ == "__main__":
    main()
