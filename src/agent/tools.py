""" 
This file contains the tools for the agent. 

The current tools are: 
Tavily Search

"""
from dotenv import load_dotenv
load_dotenv()

from langchain_tavily import TavilySearch
from langchain_core.tools import tool

@tool
def search_recipes(query: str) -> str:
    """ Search for recipes and meal planning information.

    Args: 
        query: The search query for recipes or meal planning information.

    Returns:
        Search results with recipes and meal planning information.
    """ 

    tavily = TavilySearch(
        max_results=2,
        topic="general"
    )

    results = tavily.invoke({"query": f"recipes and meal planning information for {query}"})

    ### Structure the response

    if results and 'results' in results:
        formatted_results = []
        for result in results['results']:
            title = result.get("title", "No title")
            content = result.get("content", "No content")
            url = result.get("url", "No URL")
            formatted_results.append(f"Title: {title}\nContent: {content}\nURL: {url}")
        return "\n".join(formatted_results)
    else:
        return "No results found"

ALL_TOOLS = [search_recipes]

# Testing function - only runs when script is executed directly
if __name__ == "__main__":
    # Test the search_recipes tool
    test_query = "healthy chicken dinner recipes"
    print(f"Testing search_recipes with query: '{test_query}'")
    print("-" * 50)
    
    result = search_recipes.invoke({"query": test_query})
    print(result)