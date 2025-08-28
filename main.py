from typing import Annotated, List, Dict, Any, Optional

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage

class State(TypedDict):
    """Represents the state of the chatbot conversation.

    Attributes:
        messages: A list of message dictionaries. The `add_messages` function ensures
                  new messages are appended to this list rather than overwriting it.
    """
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list; doesn't overwrite them)
    messages: Annotated[List[Dict[str, Any]], add_messages]

graph_builder = StateGraph(State)

from langchain_ollama.llms import OllamaLLM

llm = OllamaLLM(
    model="gemma3n:e4b",
    base_url="http://192.168.7.43:11434",
    temperature=0.7,
)


def bot(state: State) -> State:
    """Represents the main chatbot logic.

    This function processes the latest user message, invokes the Ollama LLM with a system message
    to guide its behavior, and then formats the LLM's response as an assistant message.

    Args:
        state (State): The current state of the conversation, including the message history.

    Returns:
        State: The updated state with the LLM's response appended to the message history.
    """
    # Get the last user message content
    user_message = state["messages"][-1]
    if isinstance(user_message, dict):
        user_content = user_message.get("content", str(user_message))
    else:
        user_content = str(user_message)

    messages_to_send = [
        SystemMessage(content="You are a helpful AI assistant. Keep your responses concise and conversational. Do not include metadata, explanations, or formatting notes in your responses."),
        user_content
    ]

    # Invoke LLM with the user content
    response = llm.invoke(messages_to_send)

    # Format the response as a message object
    bot_message = {"role": "assistant", "content": response}
    return {"messages": [bot_message]}


graph_builder.add_node("bot", bot)
graph_builder.add_edge(START, "bot")
graph_builder.add_edge("bot", END)

graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    """Streams updates from the chatbot graph and prints the bot's responses.

    This function takes user input, sends it to the compiled chatbot graph, and then
    iterates through the events to extract and print the bot's messages.

    Args:
        user_input (str): The message provided by the user.
    """
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Bot: ", value["messages"][-1]["content"])

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        stream_graph_updates(user_input)
    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except EOFError:
        # Handle Ctrl-D or end of input
        print("\nExiting...")
        break
    except Exception:
        # fallback if input() is not available
        user_input = "`Fallback prompt, something broke."
        print("User: ", user_input)
        stream_graph_updates(user_input)
        break