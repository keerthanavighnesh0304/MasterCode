from agent.tools import run_python_file
from agent.tools import read_file, write_file, edit_file

print("\n--- Successful execution ---")
print(run_python_file("test_run.py"))

print("\n--- Error execution ---")
print(run_python_file("error_test.py"))

print("\n--- Missing file ---")
print(run_python_file("missing.py"))

print("\n--- Path security ---")
print(run_python_file("../main.py"))




print("\n--- READ PATH SECURITY ---")
print(read_file("../.env"))

print("\n--- WRITE PATH SECURITY ---")
print(write_file("../unauthorized.py", "print('Hacked')"))

print("\n--- EDIT PATH SECURITY ---")
print(edit_file("../main.py", "print('Modified')"))


"""from agent.tools import write_file, read_file, list_workspace_files

# Content we want to write
content = 'print("Created by MasterCode!")'

# Test 1: Create a file
print("\n--- Creating file ---")
print(write_file("hello2.py", content))

# Test 2: List workspace files
print("\n--- Listing files ---")
print(list_workspace_files())

# Test 3: Read the file
print("\n--- Reading file ---")
print(read_file("hello2.py"))

# Test 4: Try creating the same file again
print("\n--- Testing overwrite protection ---")
print(write_file("hello2.py", content))



print("\n--- Testing path security ---")

# Test 5: Try reading outside the workspace
print(read_file("../.env"))

# Test 6: Try writing outside the workspace
print(write_file("../unauthorized.py", "print('Hacked')"))
"""