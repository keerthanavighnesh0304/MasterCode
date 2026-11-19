def approve_action(tool_name):

    print("Approval required for:", tool_name)

    decision = input("Approve? (yes/no): ")

    return decision.lower() == "yes"


def perform_action(approval_callback):

    tool_name = "write_file"

    if approval_callback(tool_name):
        print("Action approved!")
    else:
        print("Action rejected!")


perform_action(approve_action)