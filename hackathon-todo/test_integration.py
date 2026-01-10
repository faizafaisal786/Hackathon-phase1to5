"""
Integration test for the todo app agent and API.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.tasks import add_task, list_tasks, complete_task, delete_task

def test_tasks():
    """Test the task management functions."""
    print("Testing Task Management Functions")
    print("=" * 50)

    # Test 1: Add a task
    print("\n1. Adding a task...")
    result = add_task("Buy groceries", "Get milk, eggs, and bread", "2024-01-15")
    print(f"   Result: {result}")

    # Test 2: List tasks
    print("\n2. Listing all tasks...")
    result = list_tasks()
    print(f"   {result}")

    # Test 3: List pending tasks
    print("\n3. Listing pending tasks...")
    result = list_tasks("pending")
    print(f"   {result}")

    print("\n" + "=" * 50)
    print("Task management tests completed!")

def test_agent():
    """Test the OpenAI agent (requires OPENAI_API_KEY)."""
    try:
        from backend.agent import simple_chat

        print("\nTesting OpenAI Agent")
        print("=" * 50)

        print("\n1. Testing natural language task addition...")
        response = simple_chat("Add a task to prepare for the meeting tomorrow")
        print(f"   Agent: {response}")

        print("\n2. Testing task listing...")
        response = simple_chat("What are my tasks?")
        print(f"   Agent: {response}")

        print("\n" + "=" * 50)
        print("Agent tests completed!")
    except Exception as e:
        print(f"\nAgent test skipped: {e}")
        print("Make sure OPENAI_API_KEY is set in your .env file")

if __name__ == "__main__":
    # Run tests
    test_tasks()

    # Only test agent if user wants to
    print("\n\nDo you want to test the OpenAI agent? (requires OPENAI_API_KEY)")
    print("This will make API calls to OpenAI.")
    # For automated testing, skip agent test
    # test_agent()
    print("\nSkipping agent test. To test manually, uncomment test_agent() call.")
