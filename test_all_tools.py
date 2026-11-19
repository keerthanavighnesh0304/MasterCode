from agent.gemini_tools import mastercode_tool

print("MasterCode tool registered successfully!")

for function in mastercode_tool.function_declarations:
    print(function.name)