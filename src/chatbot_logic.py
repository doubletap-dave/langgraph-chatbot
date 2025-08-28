from typing import List, Dict, Any
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
import httpx
import os

from src.tools.tavily import tools as tavily_tools
from src.graph_state import State

import dotenv
dotenv.load_dotenv()

heavy_model = os.getenv("HEAVY_MODEL")
light_model = os.getenv("LIGHT_MODEL")

llm = ChatOllama(
    model=heavy_model,
    base_url="http://192.168.7.43:11434",
    temperature=0.7,
)

# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(tavily_tools)

def agent(state: State) -> State:
    """
    Represents the agent logic.

    Invokes the LLM with the current state to decide the next action.

    Args:
        state (State): The current state of the conversation.

    Returns:
        State: The updated state with the LLM's response.
    """
    try:
        response = llm_with_tools.invoke(state["messages"])
        # Return a list of messages to append to the state
        return {"messages": [response]}
    except httpx.RequestError as e:
        error_message = f"Connection to Ollama server failed: {e}. Please ensure Ollama is running and accessible."
        return {"messages": [AIMessage(content=error_message)]}
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        return {"messages": [AIMessage(content=error_message)]}
