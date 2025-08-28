from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage
from src.graph_state import State
from src.chatbot_logic import agent
from src.nodes import BasicToolNode
from src.tools.tavily import tools as tavily_tools

def should_continue(state: State) -> str:
    """
    Determines the next step based on the last message.

    If the last message is a tool call, the graph should continue to the 'tools' node.
    Otherwise, it should end the conversation turn.

    Args:
        state (State): The current state of the conversation.

    Returns:
        str: "continue" if a tool should be called, "end" otherwise.
    """
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "continue"
    return "end"

graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("agent", agent)
tool_node = BasicToolNode(tools=tavily_tools)
graph_builder.add_node("tools", tool_node)

# Set entry point
graph_builder.set_entry_point("agent")

# Add edges
graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    """Streams updates from the chatbot graph and prints the bot's responses."""
    initial_state = {"messages": [("user", user_input)]}

    for event in graph.stream(initial_state, stream_mode="values"):
        last_message = event["messages"][-1]

        # Don't print the user's message
        if isinstance(last_message, HumanMessage):
            continue
        
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            print("Bot --- ", "Calling tools...")
            for tool_call in last_message.tool_calls:
                print(f"  - {tool_call['name']}({tool_call['args']})")
        elif hasattr(last_message, 'content'):
            print("Bot >>>", last_message.content)

while True:
    try:
        user_input = input("You <<< ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        stream_graph_updates(user_input)
    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except EOFError:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break