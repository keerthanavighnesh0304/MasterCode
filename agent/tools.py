
from pathlib import Path
import subprocess
import sys
import shutil

# Locate the workspace directory
WORKSPACE_DIR = Path(__file__).resolve().parent.parent / "workspace"


def get_safe_path(filename):
    """
    Resolves a requested filename and ensures it stays
    inside MasterCode's workspace.
    """

    file_path = (WORKSPACE_DIR / filename).resolve()

    if not file_path.is_relative_to(WORKSPACE_DIR.resolve()):
        raise ValueError("Access denied: Path is outside the workspace.")

    return file_path


def list_workspace_files():
    """
    Lists all files present inside MasterCode's workspace.
    """

    if not WORKSPACE_DIR.exists():
        return []

    return [
        item.name
        for item in WORKSPACE_DIR.iterdir()
        if item.is_file()
    ]


def read_file(filename):
    """
    Reads a file from the workspace.
    """

    try:
        file_path = get_safe_path(filename)

        if not file_path.exists():
            return "Error: File does not exist."

        if not file_path.is_file():
            return "Error: The requested path is not a file."

        return file_path.read_text(encoding="utf-8")

    except ValueError as error:
        return str(error)

    except Exception as error:
        return f"Error reading file: {error}"


def write_file(filename, content):
    """
    Creates a new file inside the workspace.
    Does not overwrite existing files.
    """

    try:
        file_path = get_safe_path(filename)

        if file_path.exists():
            return "File already exists. Overwriting is not allowed."

        file_path.write_text(content, encoding="utf-8")

        return f"File '{filename}' created successfully."

    except ValueError as error:
        return str(error)

    except Exception as error:
        return f"Error writing file: {error}"


def edit_file(filename, content):
    """
    Updates an existing file in the workspace.
    Creates a unique backup before modifying the original.
    """

    try:
        file_path = get_safe_path(filename)

        if not file_path.exists():
            return "Error: File does not exist."

        if not file_path.is_file():
            return "Error: The requested path is not a file."

        # Generate a unique backup filename
        backup_path = file_path.with_name(file_path.name + ".bak")

        counter = 1

        while backup_path.exists():
            backup_path = file_path.with_name(
                file_path.name + f".bak.{counter}"
            )
            counter += 1

        # Preserve the original file before editing
        shutil.copy2(file_path, backup_path)

        # Write the updated content
        file_path.write_text(content, encoding="utf-8")

        return {
            "message": f"File '{filename}' updated successfully.",
            "backup": backup_path.name
        }

    except ValueError as error:
        return str(error)

    except Exception as error:
        return f"Error editing file: {error}"


def run_python_file(filename):
    """
    Executes a Python file inside MasterCode's workspace.
    Returns stdout, stderr and return code.
    """

    try:
        file_path = get_safe_path(filename)

        if not file_path.exists():
            return "Error: File does not exist."

        if not file_path.is_file():
            return "Error: The requested path is not a file."

        if file_path.suffix.lower() != ".py":
            return "Error: Only Python files can be executed."

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except ValueError as error:
        return str(error)

    except subprocess.TimeoutExpired:
        return "Error: Program execution timed out."

    except Exception as error:
        return f"Error executing file: {error}"
