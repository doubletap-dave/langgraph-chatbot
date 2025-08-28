# langgraph-chatbot

A simple, agentic chatbot built with Langchain, Langgraph, and Ollama. It can use tools like Tavily Search to answer questions that require up-to-date information.

## Setup

1.  **Install uv:**

    **Option 1: Standalone Installer (Recommended for Windows)**

    Open PowerShell and run:

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    **Option 2: Using pipx (Recommended for global installation)**

    First, ensure you have `pipx` installed:

    ```bash
    pip install pipx
    pipx ensurepath
    ```

    Then, install `uv`:

    ```bash
    pipx install uv
    ```

2.  **Install dependencies (using uv):**

    ```bash
    uv add dotenv ipykernel langchain langchain-community langchain-ollama langchain-tavily langgraph langsmith typing-extensions
    ```

3.  **Configure Environment Variables:**

    Create a `.env` file in the project root and add the following variables:

    ```env
    TAVILY_API_KEY="your_tavily_api_key"
    TAVILY_MAX_RESULTS=3
    HEAVY_MODEL="gpt-oss:20b"
    LIGHT_MODEL="your_optional_light_model"
    ```

    - `TAVILY_API_KEY`: Your API key for the Tavily Search Engine.
    - `TAVILY_MAX_RESULTS`: The maximum number of search results to return.
    - `HEAVY_MODEL`: The primary Ollama model to use (must support tool calling).
    - `LIGHT_MODEL`: An optional, lighter model for simpler tasks (not yet implemented).

4.  **Run the chatbot:**

    ```bash
    uv run python main.py
    ```

## Usage

Type your messages at the `You >>>` prompt. The bot will respond, and if it needs to perform a web search, it will indicate that it's calling the Tavily search tool.

To exit the chatbot, type `exit`, `quit`, or `q`.

## How It Works

The chatbot is built on a `langgraph` state machine with two main nodes:

-   **Agent**: This node uses an Ollama model to decide whether to respond directly or to use a tool.
-   **Tools**: This node executes the tool requested by the agent (currently, Tavily Search).

A conditional edge routes the conversation between the agent and the tools based on the agent's decision. This allows the chatbot to dynamically choose the best way to answer your questions.

