from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """Represents the state of the chatbot conversation.

    Attributes:
        messages: A list of message dictionaries. The `add_messages` function ensures
                  new messages are appended to this list rather than overwriting it.
    """
    messages: Annotated[List[Dict[str, Any]], add_messages]
