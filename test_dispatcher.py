from agent.dispatcher import execute_tool

print("\n--- Test 1: List files ---")
print(execute_tool("list_workspace_files", {}))


print("\n--- Test 2: Read a file ---")
print(execute_tool(
    "read_file",
    {"filename": "sample.py"}
))


print("\n--- Test 3: Write a new file ---")
print(execute_tool(
    "write_file",
    {
        "filename": "dispatcher_created.py",
        "content": 'print("Created through dispatcher!")'
    }
))


print("\n--- Test 4: Run a Python file ---")
print(execute_tool(
    "run_python_file",
    {"filename": "test_run.py"}
))


print("\n--- Test 5: Unknown tool ---")
print(execute_tool("delete_everything", {}))