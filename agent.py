import asyncio
from typing import Annotated, TypedDict
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage

# 1. Ορίζουμε το State του Agent (κρατάει το ιστορικό των μηνυμάτων)
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

async def main():
    # Ορισμός του MCP Server subprocess
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Φόρτωση tools από τον MCP server
            tools = await load_mcp_tools(session)
            print(f"Loaded tools from MCP Server: {[t.name for t in tools]}")

            # Σύνδεση με το τοπικό Ollama
            llm = ChatOllama(model="qwen2.5:7b", temperature=0)
            llm_with_tools = llm.bind_tools(tools)

            # 2. Ορίζουμε τα nodes του Graph
            def call_model(state: State):
                response = llm_with_tools.invoke(state["messages"])
                return {"messages": [response]}

            def should_continue(state: State):
                last_message = state["messages"][-1]
                # Αν το LLM ζήτησε tool call, πάμε στο node 'tools', αλλιώς τελειώνουμε
                if last_message.tool_calls:
                    return "tools"
                return END

            # 3. Χτίζουμε το StateGraph
            workflow = StateGraph(State)
            workflow.add_node("agent", call_model)
            workflow.add_node("tools", ToolNode(tools)) # Το επίσημο ToolNode του LangGraph

            # Συνδέουμε τα nodes μεταξύ τους
            workflow.add_edge(START, "agent")
            workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
            workflow.add_edge("tools", "agent") # Κύκλος: από τα tools ξαναγυρνάμε στον agent με το αποτέλεσμα

            app = workflow.compile()

            # 4. Εκτέλεση ερώτησης
            query = "Πόση συνολική παραγωγή ενέργειας (generation_mwh) είχαμε από Lignite;"
            print(f"\nUser Query: {query}\n" + "-"*40)
            
            result = await app.ainvoke({"messages": [("user", query)]})
            
            print("\nFinal Agent Answer:")
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())