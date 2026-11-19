
import streamlit as st


from agent.agent import run_agent_stream, create_chat
from agent.tools import list_workspace_files, read_file


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="MasterCode",
    page_icon="💻",
    layout="wide"
)

st.title("💻 MasterCode")
st.caption("Your AI coding assistant")


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "activity" not in st.session_state:
    st.session_state.activity = []

if "agent_generator" not in st.session_state:
    st.session_state.agent_generator = None

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = create_chat()

# --------------------------------------------------
# WORKSPACE FILE EXPLORER
# --------------------------------------------------

st.sidebar.title("📁 Workspace")

if st.sidebar.button("🔄 Refresh files"):
    st.rerun()

files = list_workspace_files()

if files:

    selected_file = st.sidebar.selectbox(
        "Select a file",
        files
    )

    if selected_file:

        st.sidebar.divider()
        st.sidebar.subheader(f"📄 {selected_file}")

        file_content = read_file(selected_file)

        if isinstance(file_content, str):
            st.sidebar.code(
                file_content,
                language="python"
            )
        else:
            st.sidebar.warning("Unable to display this file.")

else:
    st.sidebar.info("No files found in workspace.")


# --------------------------------------------------
# AGENT EVENT HANDLER
# --------------------------------------------------

def advance_agent(generator, decision=None):

    try:

        # Start the generator or resume it after approval
        if decision is None:
            event = next(generator)
        else:
            event = generator.send(decision)

        while True:

            event_type = event.get("type")

            # --------------------------------------
            # APPROVAL REQUIRED
            # --------------------------------------

            if event_type == "approval_required":

                st.session_state.pending_approval = event
                return

            # Store other events in activity history
            st.session_state.activity.append(event)

            # --------------------------------------
            # FINAL ANSWER
            # --------------------------------------

            if event_type == "final":

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": event["text"]
                })

                st.session_state.agent_generator = None
                st.session_state.pending_approval = None
                return

            # --------------------------------------
            # ITERATION LIMIT
            # --------------------------------------

            if event_type == "limit":

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": event["text"]
                })

                st.session_state.agent_generator = None
                st.session_state.pending_approval = None
                return

            # --------------------------------------
            # MOVE TO NEXT EVENT
            # --------------------------------------

            event = next(generator)

    except StopIteration:

        st.session_state.agent_generator = None
        st.session_state.pending_approval = None

    except Exception as error:

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"An error occurred: {error}"
        })

        st.session_state.agent_generator = None
        st.session_state.pending_approval = None


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# TOOL ACTIVITY PANEL
# --------------------------------------------------

with st.expander("🔧 Tool activity", expanded=True):

    if not st.session_state.activity:

        st.caption("No tool activity yet.")

    for event in st.session_state.activity:

        event_type = event.get("type")

        # ------------------------------------------
        # TOOL REQUEST
        # ------------------------------------------

        if event_type == "tool_requested":

            st.write(
                f"🔧 Requested: {event['tool_name']}"
            )

            st.json(event["arguments"])

        # ------------------------------------------
        # TOOL RESULT
        # ------------------------------------------

        elif event_type == "tool_result":

            tool_name = event["tool_name"]
            result = event["result"]

            st.write(f"✅ Completed: {tool_name}")

            if tool_name == "run_python_file":

                execution = result.get("result", {})

                if isinstance(execution, dict) and "stdout" in execution:

                    st.markdown("**Program Output**")

                    st.code(
                        execution["stdout"] or "No output",
                        language="text"
                    )

                    if execution.get("stderr"):
                        st.markdown("**Errors**")
                        st.error(execution["stderr"])

                    if execution.get("returncode") == 0:
                        st.success("Execution completed successfully.")
                    else:
                        st.error(
                            f"Program exited with code "
                            f"{execution.get('returncode')}."
                        )

                else:

                    st.error(
                        result.get("error", "Execution failed.")
                    )

            else:

                st.json(result)


# --------------------------------------------------
# APPROVAL SECTION
# --------------------------------------------------

pending = st.session_state.pending_approval

if pending:

    st.warning("⚠️ MasterCode is requesting your approval.")

    st.write("**Tool:**", pending["tool_name"])

    st.write("**Arguments:**")
    st.json(pending["arguments"])

    col1, col2 = st.columns(2)

    # ----------------------------------------------
    # APPROVE
    # ----------------------------------------------

    with col1:

        if st.button(
            "✅ Approve",
            type="primary",
            use_container_width=True
        ):

            st.session_state.pending_approval = None

            advance_agent(
                st.session_state.agent_generator,
                True
            )

            st.rerun()

    # ----------------------------------------------
    # REJECT
    # ----------------------------------------------

    with col2:

        if st.button(
            "❌ Reject",
            use_container_width=True
        ):

            st.session_state.pending_approval = None

            advance_agent(
                st.session_state.agent_generator,
                False
            )

            st.rerun()


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_prompt = st.chat_input(
    "Ask MasterCode to read, create or run a Python file...",
    disabled=st.session_state.agent_generator is not None
)

if user_prompt:

    # Save the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    # Clear previous tool activity for the new request
    st.session_state.activity = []

    # Start a new agent execution
    st.session_state.agent_generator = run_agent_stream(
        user_prompt,
        st.session_state.gemini_chat
    )

    # Start processing agent events
    advance_agent(
        st.session_state.agent_generator
    )

    st.rerun()
