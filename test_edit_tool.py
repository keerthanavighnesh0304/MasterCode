from agent.tools import edit_file, read_file

result = edit_file(
    "calculator.py",
    """# Updated calculator
a = 50
b = 35
result = a + b
print(result)
"""
)

print("Edit result:", result)
print("Updated content:")
print(read_file("calculator.py"))
