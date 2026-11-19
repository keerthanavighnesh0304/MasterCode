"""from agent.agent import run_agent

user_prompt = "List all the files in my workspace."

run_agent(user_prompt)"""
'''
from agent.agent import run_agent

user_prompt = """
Create a Python file named calculator.py.
The program should add two numbers, 25 and 35,
and print the result.
After creating the file, execute it and tell me the output.
"""

run_agent(user_prompt)'''

from agent.agent import run_agent

#user_prompt = "Read sample.py and explain what the program does."
user_prompt = """
List all files in my workspace and read sample.py.
Report both results.
"""
run_agent(user_prompt)