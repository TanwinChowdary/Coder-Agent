from dotenv import load_dotenv
from langchain_core.globals import set_verbose, set_debug
from langchain_groq import ChatGroq

from agent.prompts import *
from agent.states import *
from agent.tools import *
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain.agents import create_agent

_ = load_dotenv()
# set_debug(True)
# set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b")


# simple progress bar
def progress(label, percent):
    bar_len = 20
    filled = int(bar_len * (percent / 100))
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"{label}: [{bar}] {percent}%")


def planner_agent(state: dict) -> dict:
    print("\n=== PLANNER AGENT STARTED ===")
    progress("Planner", 10)

    user_prompt = state["user_prompt"]
    progress("Planner", 40)

    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    progress("Planner", 80)

    if resp is None:
        raise ValueError("Planner did not return a response.")

    progress("Planner", 100)
    print("Planner finished.\n")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    print("\n=== ARCHITECT AGENT STARTED ===")
    progress("Architect", 10)

    plan: Plan = state["plan"]
    progress("Architect", 35)

    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    progress("Architect", 75)

    if resp is None:
        raise ValueError("Architect did not return a response.")

    resp.plan = plan
    progress("Architect", 100)
    print("Architect finished.\n")
    return {"task_plan": resp}


def coding_agent(state: dict) -> dict:
    print("\n=== CODER AGENT STARTED ===")
    progress("Coder", 5)

    coder_state = state.get("coder_state")

    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"],
            current_step_idx=0
        )
    progress("Coder", 20)

    steps = coder_state.task_plan.implementation_steps

    if coder_state.current_step_idx >= len(steps):
        progress("Coder", 100)
        print("Coder completed all steps.\n")
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    progress("Coder", 40)

    init_project_root()
    existing_content = read_file.run(current_task.filepath)
    progress("Coder", 55)

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "When saving changes, call the tool `repo_browser.write_file(path, content)`.\n"
        "Only use these tools: repo_browser.read_file, repo_browser.write_file, "
        "repo_browser.list_files, repo_browser.get_current_directory, repo_browser.run_cmd.\n"
        "Do NOT call any other tools."
    )
    progress("Coder", 70)

    coder_tools = [
        read_file, write_file, list_files,
        get_current_directory, run_cmd, print_tree
    ]

    react_agent = create_agent(llm, coder_tools)
    progress("Coder", 80)

    react_agent.invoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    })
    progress("Coder", 95)

    coder_state.current_step_idx += 1
    progress("Coder", 100)
    print("Coder finished step.\n")

    return {"coder_state": coder_state}


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coding_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")

agent = graph.compile()