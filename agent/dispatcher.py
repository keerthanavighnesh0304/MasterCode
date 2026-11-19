from agent.tools import (
    list_workspace_files,
    read_file,
    write_file,
    edit_file,
    run_python_file
)

AVAILABLE_FUNCTIONS = {
    "list_workspace_files": list_workspace_files,
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "run_python_file": run_python_file
}


def execute_tool(function_name, arguments):

    if function_name not in AVAILABLE_FUNCTIONS:
        return {"error": f"Unknown tool: {function_name}"}

    function_to_call = AVAILABLE_FUNCTIONS[function_name]

    try:
        result = function_to_call(**arguments)
        return {"result": result}

    except Exception as error:
        return {"error": str(error)}