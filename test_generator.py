def my_agent():

    print("Agent started")

    decision = yield "Approval required"

    print("User decision:", decision)

    yield "Agent finished"


agent = my_agent()

message = next(agent)
print("Agent says:", message)

message = agent.send(True)
print("Agent says:", message)