
from google.genai import types

# Define the function Gemini is allowed to request.
list_files_declaration = types.FunctionDeclaration(
    name="list_workspace_files",
    description="Lists the names of all files in MasterCode's workspace.",
    parameters_json_schema={
        "type": "object",
        "properties": {}
    }
)

# Group the function declaration into a Tool.
list_files_tool = types.Tool(
    function_declarations=[list_files_declaration]
)




read_file_declaration = types.FunctionDeclaration(
    name="read_file",
    description="Reads the contents of a file inside MasterCode's workspace.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file to read."
            }
        },
        "required": ["filename"]
    }
)

read_file_tool = types.Tool(
    function_declarations=[read_file_declaration]
)




write_file_declaration = types.FunctionDeclaration(
    name="write_file",
    description="Creates a new file inside MasterCode's workspace with the provided content. Does not overwrite existing files.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file to create."
            },
            "content": {
                "type": "string",
                "description": "The content to write into the file."
            }
        },
        "required": ["filename", "content"]
    }
)

write_file_tool = types.Tool(
    function_declarations=[write_file_declaration]
)


edit_file_declaration = types.FunctionDeclaration(
    name="edit_file",
    description=(
        "Updates the content of an existing file inside "
        "MasterCode's workspace. Use this only when the "
        "user requests modification of an existing file."
    ),
    parameters_json_schema={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "Name of the existing file to edit."
            },
            "content": {
                "type": "string",
                "description": "The complete updated file content."
            }
        },
        "required": ["filename", "content"]
    }
)

edit_file_tool = types.Tool(
    function_declarations=[edit_file_declaration]
)




run_file_declaration = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file inside MasterCode's workspace and returns its output.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the Python file to execute."
            }
        },
        "required": ["filename"]
    }
)

run_file_tool = types.Tool(
    function_declarations=[run_file_declaration]
)


mastercode_tool = types.Tool(
    function_declarations=[
        list_files_declaration,
        read_file_declaration,
        write_file_declaration,
        edit_file_declaration,
        run_file_declaration
    ]
)