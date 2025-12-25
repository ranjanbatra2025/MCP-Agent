# agent_client.py - Context-Aware Agent using MCP tools
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters import MCPToolAdapter
from langchain_groq import ChatGroq
import asyncio

# Connect to MCP server
mcp_adapter = MCPToolAdapter(mcp_url="http://localhost:8001")

# Get tools automatically from MCP server
tools = mcp_adapter.get_tools()
tool_node = ToolNode(tools)

# LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
model_with_tools = llm.bind_tools(tools)

# Agent state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Nodes
def chatbot(state: AgentState):
    return {"messages": [model_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(AgentState)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", tool_node)

builder.add_edge(START, "chatbot")
builder.add_conditional_edges(
    "chatbot",
    lambda x: "tools" if x["messages"][-1].tool_calls else END,
)
builder.add_edge("tools", "chatbot")

graph = builder.compile()

# Run interactive agent
print("LIVECONTEXT AGENT READY")
print("Ask anything — it will use real-time tools when needed.\n")

while True:
    try:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit"]:
            print("Agent offline.")
            break

        print("Agent: ", end="", flush=True)
        for chunk in graph.stream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="values"
        ):
            chunk["messages"][-1].pretty_print()

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")