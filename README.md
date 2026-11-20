# 💻 MasterCode – AI-Powered Coding Assistant

MasterCode is an AI-powered coding assistant built using Python, Google's Gemini API, and Streamlit. It enables users to interact with an AI agent that can inspect, create, edit, and execute Python files inside a designated workspace.

The project demonstrates AI function calling, tool orchestration, user approval workflows, file management, and controlled Python execution.

## 🚀 Features

- **AI-powered interaction:** Communicate with the coding assistant using natural language.
- **Workspace exploration:** List and inspect files inside the workspace.
- **File creation:** Create new Python files through AI tool calls.
- **File editing:** Modify existing files with automatic backups.
- **Python execution:** Execute Python files and capture standard output, errors, and exit codes.
- **Approval mechanism:** Require user approval before creating, editing, or executing files.
- **Workspace path protection:** Restrict file operations to the designated workspace directory.
- **Execution timeout:** Stop Python programs that exceed the configured execution time.
- **Gemini retry mechanism:** Retry selected temporary API errors using exponential backoff.
- **Interactive interface:** Use a Streamlit chat interface with workspace explorer and tool activity panel.
- **Conversation continuity:** Maintain chat context during a Streamlit session.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| AI model/API | Google Gemini API |
| AI SDK | Google Gen AI SDK |
| Frontend | Streamlit |
| Configuration | python-dotenv |
| Tool execution | Python subprocess |
| Version control | Git and GitHub |

## 🏗️ Project Architecture

MasterCode follows a modular architecture:

1. **Streamlit Interface (`app.py`)** – Handles user interaction, chat history, workspace exploration, approval prompts, and tool activity.
2. **Agent (`agent/agent.py`)** – Manages conversations with Gemini, processes function calls, and coordinates the agent execution loop.
3. **Tool Definitions (`agent/gemini_tools.py`)** – Declares the functions that Gemini can request.
4. **Dispatcher (`agent/dispatcher.py`)** – Maps requested function names to their corresponding Python implementations.
5. **Tool Implementations (`agent/tools.py`)** – Performs workspace operations, file management, and Python execution.

### Agent Workflow

User Prompt → Streamlit Interface → Gemini Agent → Function Call → User Approval (when required) → Tool Dispatcher → Tool Execution → Result Returned to Gemini → Final Response

## 📁 Project Structure

```text
MasterCode/
│
├── agent/
│   ├── agent.py
│   ├── tools.py
│   ├── gemini_tools.py
│   └── dispatcher.py
│
├── workspace/
│   └── calculator.py
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── test_*.py
```

The workspace is the designated directory in which MasterCode performs file operations.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/keerthanavighnesh0304/MasterCode.git
cd MasterCode
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key.

**Important:** Never upload your `.env` file or expose your API key in source code or public repositories.

## ▶️ Running MasterCode

Start the Streamlit application:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

You can now interact with MasterCode through the chat interface.

## 🧪 Testing

The project includes tests for different components and behaviours, including:

- Workspace file operations
- File reading, writing, and editing
- Path traversal protection
- Python file execution
- Execution timeout handling
- User approval and rejection
- Automatic file backups
- Gemini function calling and tool dispatch
- Agent execution loop
- API retry handling
- API failure propagation

Run individual tests using:

```powershell
python test_tools.py
```

For other tests, use:

```powershell
python test_retry_failure.py
python test_stream_api_failure.py
```

## 🔐 Security Considerations and Limitations

MasterCode includes several safeguards:

- Workspace path validation to prevent operations outside the designated workspace.
- User approval before file creation, modification, and execution.
- Automatic backups before editing existing files.
- Restrictions on the type of files that can be executed.
- Execution timeout to prevent indefinitely running programs.
- Environment variables for API key configuration.

**Important limitation:** Python execution currently uses `subprocess` and runs with the permissions of the operating-system user. It is not a secure sandbox. A Python program may access files, networks, and processes available to that user. Do not execute untrusted code. Stronger isolation would require a dedicated sandbox or container with restricted permissions.

## 🎯 Project Objective

The objective of MasterCode is to explore how AI agents can interact with development environments through function calling and tool execution.

It demonstrates how an AI assistant can move beyond generating code to performing practical coding operations through a modular agent architecture and human approval workflow.

## 👩‍💻 Author

**Keerthana Vighnesh**

GitHub: [keerthanavighnesh0304](https://github.com/keerthanavighnesh0304)

Project Repository: [MasterCode](https://github.com/keerthanavighnesh0304/MasterCode)