""" 
This file contains the tools for the agent. 

The current tools are: 
Tavily Search

"""
from dotenv import load_dotenv
load_dotenv()

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing import Annotated

@tool
def search_recipes(query: Annotated[str, "The search query for recipes"]) -> str:
    """🔍 ESSENTIAL TOOL: Search for current, trending recipes and meal ideas.
    
    This tool provides fresh, up-to-date recipe information that's better than 
    any recipes in your training data from the internet. Use this for ALL recipe requests!
    
    Perfect for finding:
    - Specific recipes (keto, vegan, gluten-free, etc.)
    - Cuisine-specific dishes (Mediterranean, Asian, etc.) 
    - Trending/popular recipes
    - Healthy meal ideas
    - Quick/easy recipes
    - Seasonal recipes
    
    Args: 
        query: The search query for recipes (e.g., "keto breakfast recipes", 
               "healthy chicken dinner", "Mediterranean pasta dishes")

    Returns:
        Current recipe information with titles, descriptions, and sources.
    """ 

    print(f"🔧 TOOL CALLED: search_recipes with query: {query}")

    tavily = TavilySearch(
        max_results=1,
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