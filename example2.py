from flask import Flask, request, jsonify
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

app = Flask(__name__)

class State(TypedDict):
    user_input: str
    user_feedback: str
    status: str

def process_request(state):
    """First step - process user request"""
    return {"status": "processing"}

def request_approval(state):
    """Pause here and ask for approval"""
    # This pauses execution and saves state
    approval = interrupt({
        "question": "Do you approve this action?",
        "request": state["user_input"]
    })
    return {"user_feedback": approval}

def execute_action(state):
    """Final step after approval"""
    return {"status": f"completed with feedback: {state['user_feedback']}"}

# Build graph
builder = StateGraph(State)
builder.add_node("process", process_request)
builder.add_node("approval", request_approval)
builder.add_node("execute", execute_action)
builder.add_edge(START, "process")
builder.add_edge("process", "approval")
builder.add_edge("approval", "execute")
builder.add_edge("execute", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

@app.route("/start", methods=["POST"])
def start_workflow():
    """Initiate workflow - will pause at interrupt"""
    session_id = request.json.get("session_id")
    user_input = request.json.get("input")
    
    config = {"configurable": {"thread_id": session_id}}
    result = graph.invoke({"user_input": user_input}, config=config)
    
    # Check if interrupted
    if "__interrupt__" in result:
        interrupt_info = result["__interrupt__"][0]
        return jsonify({
            "status": "awaiting_approval",
            "question": interrupt_info.value["question"],
            "session_id": session_id
        })
    
    return jsonify({"status": "completed", "result": result})

@app.route("/resume", methods=["POST"])
def resume_workflow():
    """Resume with user's approval"""
    session_id = request.json.get("session_id")
    approval_response = request.json.get("approval")
    
    config = {"configurable": {"thread_id": session_id}}
    
    # Resume with Command
    result = graph.invoke(Command(resume=approval_response), config=config)
    
    return jsonify({
        "status": "completed",
        "result": result.get("status"),
        "feedback": result.get("user_feedback")
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
