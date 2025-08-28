from langchain_tavily import TavilySearch

import dotenv
import os
dotenv.load_dotenv()

# Ensure TAVILY_MAX_RESULTS is an integer; default to 5 if not set or invalid.
# It must be an integer, otherwise the TavilySearch tool will error out.
max_results_str = os.getenv("TAVILY_MAX_RESULTS")
if max_results_str:
    try:
        max_results = int(max_results_str)
    except ValueError:
        max_results = 5  # Default to 5 if conversion fails
else:
    max_results = 5  # Default to 5 if not set

tavily_search_tool = TavilySearch(max_results=max_results)
tools = [tavily_search_tool]