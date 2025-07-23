"""Unit tests for the search_recipes tool."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from src.agent.tools import search_recipes


def test_search_recipes_basic():
    """Test basic functionality of search_recipes tool."""
    print("🧪 Testing basic search_recipes functionality")
    print("-" * 60)
    
    query = "healthy chicken dinner recipes"
    print(f"Query: {query}")
    
    try:
        result = search_recipes.invoke({"query": query})
        
        # Basic checks
        assert isinstance(result, str), "Result should be a string"
        assert len(result) > 0, "Result should not be empty"
        
        print("✅ Basic test passed")
        print(f"📋 Result preview: {result[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False


def test_search_recipes_different_queries():
    """Test search_recipes with different types of queries."""
    print("\n🧪 Testing search_recipes with various queries")
    print("-" * 60)
    
    test_queries = [
        "quick vegetarian lunch ideas",
        "keto breakfast recipes",
        "healthy snacks for kids",
        "Mediterranean diet dinner",
        "gluten-free desserts"
    ]
    
    passed_tests = 0
    total_tests = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{total_tests}] Testing: '{query}'")
        
        try:
            result = search_recipes.invoke({"query": query})
            
            # Validate result
            if isinstance(result, str) and len(result) > 0:
                print(f"✅ Test passed - Got {len(result)} characters")
                passed_tests += 1
            else:
                print("❌ Test failed - Invalid result format")
                
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print(f"\n📊 Summary: {passed_tests}/{total_tests} tests passed")
    return passed_tests == total_tests


def test_search_recipes_edge_cases():
    """Test search_recipes with edge cases."""
    print("\n🧪 Testing search_recipes edge cases")
    print("-" * 60)
    
    edge_cases = [
        "",  # Empty query
        "a",  # Very short query
        "recipes " * 50,  # Very long query
        "🍕🍔🍟",  # Emoji query
    ]
    
    for i, query in enumerate(edge_cases, 1):
        query_display = query if len(query) < 50 else query[:47] + "..."
        print(f"\n[{i}/{len(edge_cases)}] Testing edge case: '{query_display}'")
        
        try:
            result = search_recipes.invoke({"query": query})
            print(f"✅ Handled edge case - Result length: {len(result)}")
            
        except Exception as e:
            print(f"⚠️  Edge case resulted in error: {e}")


def test_api_key_present():
    """Test that TAVILY_API_KEY is available."""
    print("\n🔑 Testing API key availability")
    print("-" * 60)
    
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if tavily_key:
        print("✅ TAVILY_API_KEY is set")
        print(f"📝 Key preview: {tavily_key[:8]}...{tavily_key[-4:]}")
        return True
    else:
        print("❌ TAVILY_API_KEY is not set")
        print("💡 Make sure you have TAVILY_API_KEY in your .env file")
        return False


def run_all_tests():
    """Run all tests for search_recipes tool."""
    print("🚀 Starting search_recipes tool tests")
    print("=" * 80)
    
    # Check API key first
    if not test_api_key_present():
        print("\n❌ Cannot run tests without TAVILY_API_KEY")
        return False
    
    # Run tests
    tests_passed = []
    
    tests_passed.append(test_search_recipes_basic())
    tests_passed.append(test_search_recipes_different_queries())
    
    # Edge cases (don't count towards pass/fail)
    test_search_recipes_edge_cases()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 80)
    
    passed_count = sum(tests_passed)
    total_count = len(tests_passed)
    
    if passed_count == total_count:
        print(f"🎉 ALL TESTS PASSED! ({passed_count}/{total_count})")
        print("✅ search_recipes tool is working correctly")
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed_count}/{total_count})")
        print("❌ There may be issues with the search_recipes tool")
    
    return passed_count == total_count


if __name__ == "__main__":
    run_all_tests() 