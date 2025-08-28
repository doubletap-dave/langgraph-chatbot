# langgraph-chatbot

A simple chatbot built with Langchain, Langgraph, and Ollama.

## Setup

1.  **Install uv:**

    ```bash
    pip install uv
    ```

2.  **Install dependencies:**

    ```bash
    uv add langgraph langsmith typing-extensions
    ```

3.  **Run the chatbot:**

    ```bash
    uv run python main.py
    ```

    Alternatively, you can run it directly with python if your virtual environment is activated:

    ```bash
    python main.py
    ```

## Usage

Type your messages at the `User:` prompt. To exit the chatbot, type `exit`, `quit`, or `q`.

## Configuration

The Ollama model and base URL are configured in `main.py`:

```python
llm = OllamaLLM(
    model="gemma3n:e4b",
    base_url="http://192.168.7.43:11434",
    temperature=0.7,
)
```

Make sure your Ollama server is running and accessible at the specified `base_url`.

