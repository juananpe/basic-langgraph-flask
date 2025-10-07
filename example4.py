from flask import Flask, request, jsonify
from langgraph.graph import StateGraph, START
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from typing import Literal

app = Flask(__name__)

class WorkflowState(TypedDict):
    action: str
    approved: bool
    result: str

def propose_action(state: WorkflowState) -> Command[Literal["approval"]]:
    """Propose an action"""
    return Command(
        update={"action": "Deploy to production"},
        goto="approval"
    )

def approval_node(state: WorkflowState) -> Command[Literal["execute", "reject"]]:
    """Interrupt for approval, then route based on response"""
    # Pause and ask for approval
    decision = interrupt({
        "question": "Approve this action?",
        "action": state["action"],
        "options": ["approve", "reject"]
    })
    
    # Route based on decision using Command
    if decision == "approve":
        return Command(
            update={"approved": True},
            goto="execute"
        )
    else:
        return Command(
            update={"approved": False},
            goto="reject"
        )

def execute_node(state: WorkflowState) -> Command[Literal["__end__"]]:
    """Execute approved action"""
    return Command(
        update={"result": f"Executed: {state['action']}"},
        goto="__end__"
    )

def reject_node(state: WorkflowState) -> Command[Literal["__end__"]]:
    """Handle rejection"""
    return Command(
        update={"result": f"Rejected: {state['action']}"},
        goto="__end__"
    )

# Build graph
builder = StateGraph(WorkflowState)
builder.add_node("propose", propose_action)
builder.add_node("approval", approval_node)
builder.add_node("execute", execute_node)
builder.add_node("reject", reject_node)
builder.add_edge(START, "propose")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

@app.route("/initiate", methods=["POST"])
def initiate():
    """Start workflow"""
    session_id = request.json.get("session_id")
    config = {"configurable": {"thread_id": session_id}}
    
    result = graph.invoke({}, config=config)
    
    if "__interrupt__" in result:
        interrupt_info = result["__interrupt__"][0]
        return jsonify({
            "status": "awaiting_decision",
            "prompt": interrupt_info.value,
            "session_id": session_id
        })
    
    return jsonify({"status": "completed", "result": result})

@app.route("/decide", methods=["POST"])
def decide():
    """Resume with decision - Command will route appropriately"""
    session_id = request.json.get("session_id")
    decision = request.json.get("decision")  # "approve" or "reject"
    
    config = {"configurable": {"thread_id": session_id}}
    result = graph.invoke(Command(resume=decision), config=config)
    
    return jsonify({
        "status": "completed",
        "approved": result.get("approved"),
        "result": result.get("result")
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
