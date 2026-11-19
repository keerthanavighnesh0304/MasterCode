from agent.agent import run_agent_stream


user_prompt = """
Create a Python file named stream_test.py
that prints Hello from the Streamlit workflow.
"""

agent = run_agent_stream(user_prompt)

try:
    event = next(agent)

    while True:

        print("\nAgent event:", event)

        if event["type"] == "approval_required":

            decision = input(
                f"Approve {event['tool_name']}? (yes/no): "
            )

            approved = decision.strip().lower() in ["yes", "y"]

            # Resume the generator with the user's decision
            event = agent.send(approved)

        else:
            # Move to the next event
            event = next(agent)

except StopIteration:
    print("\nAgent workflow completed.")