from flask import Flask, request, jsonify
from langgraph.graph import StateGraph, START
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from typing import Literal

app = Flask(__name__)

class ChatState(TypedDict):
    message: str
    intent: str
    result: str

def classifier(state: ChatState) -> Command[Literal["search", "summarize", "help"]]:
    """Classify intent and route dynamically"""
    message = state["message"].lower()
    
    # Determine intent and route
    if "search" in message:
        return Command(
            update={"intent": "search"},
            goto="search"
        )
    elif "summarize" in message:
        return Command(
            update={"intent": "summarize"},
            goto="summarize"
        )
    else:
        return Command(
            update={"intent": "help"},
            goto="help"
        )

def search_handler(state: ChatState) -> Command[Literal["__end__"]]:
    """Handle search requests"""
    return Command(
        update={"result": f"Search results for: {state['message']}"},
        goto="__end__"
    )

def summarize_handler(state: ChatState) -> Command[Literal["__end__"]]:
    """Handle summarization"""
    return Command(
        update={"result": f"Summary: {state['message'][:50]}..."},
        goto="__end__"
    )

def help_handler(state: ChatState) -> Command[Literal["__end__"]]:
    """Handle help requests"""
    return Command(
        update={"result": "I can help you search or summarize. Just ask!"},
        goto="__end__"
    )

# Build edgeless graph - Command handles all routing
builder = StateGraph(ChatState)
builder.add_node("classifier", classifier)
builder.add_node("search", search_handler)
builder.add_node("summarize", summarize_handler)
builder.add_node("help", help_handler)
builder.add_edge(START, "classifier")
# No edges needed between classifier and handlers - Command routes dynamically!

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

@app.route("/process", methods=["POST"])
def process():
    message = request.json.get("message")
    session_id = request.json.get("session_id", "default")
    
    config = {"configurable": {"thread_id": session_id}}
    result = graph.invoke({"message": message}, config=config)
    
    return jsonify({
        "intent": result.get("intent"),
        "result": result.get("result")
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
