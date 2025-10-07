from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from flask import Flask, request, jsonify
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

app = Flask(__name__)

# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define agent node
def chatbot(state: State):
    llm = ChatOpenAI(model="gpt-4")
    return {"messages": [llm.invoke(state["messages"])]}

# Build graph with memory
workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# Flask endpoint with session management
@app.route("/chat", methods=["POST"])
def chat():
    user_id = request.json.get("user_id", "default")
    message = request.json.get("message")
    
    config = {"configurable": {"thread_id": user_id}}
    result = graph.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config
    )
    
    return jsonify({"reply": result["messages"][-1].content})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
