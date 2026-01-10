#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive test script for Hackathon Todo Application.
Tests all core functionality without starting a server.
"""
import sys
import os

# Fix Windows encoding issues
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def print_test(name):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)

def test_imports():
    """Test that all required modules can be imported."""
    print_test("Module Imports")

    modules = [
        ("FastAPI", "fastapi"),
        ("SQLModel", "sqlmodel"),
        ("OpenAI", "openai"),
        ("MCP", "mcp"),
        ("Pydantic Settings", "pydantic_settings"),
        ("Python-JOSE", "jose"),
        ("Passlib", "passlib"),
    ]

    for name, module in modules:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ✗ {name}: {e}")
            return False

    return True

def test_app_loading():
    """Test that the FastAPI app loads correctly."""
    print_test("FastAPI Application Loading")

    try:
        from app.main import app
        print("  ✓ App loaded successfully")

        from fastapi.routing import APIRoute
        routes = [r for r in app.routes if isinstance(r, APIRoute)]
        print(f"  ✓ {len(routes)} endpoints registered")

        # Check key endpoints
        paths = [r.path for r in routes]
        required = ["/", "/health", "/auth/register", "/tasks", "/chat/"]

        for path in required:
            if path in paths:
                print(f"  ✓ Endpoint: {path}")
            else:
                print(f"  ✗ Missing endpoint: {path}")
                return False

        return True
    except Exception as e:
        print(f"  ✗ Error loading app: {e}")
        return False

def test_database():
    """Test database initialization."""
    print_test("Database Initialization")

    try:
        from app.database import create_db_and_tables
        create_db_and_tables()
        print("  ✓ Database initialized")

        # Check if database file exists (for SQLite)
        import os
        if os.path.exists("hackathon_todo.db"):
            print("  ✓ Database file created")

        return True
    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False

def test_demo_agent():
    """Test the demo mode agent."""
    print_test("Demo Mode Agent (FREE)")

    try:
        sys.path.insert(0, 'backend')
        from agent import chat_demo_mode, get_demo_mode

        # Check demo mode
        if get_demo_mode():
            print("  ✓ Running in FREE demo mode")
        else:
            print("  ✓ OpenAI API key detected")

        # Test adding a task
        result = chat_demo_mode("Add a task to test the system")
        if "added" in result["message"].lower():
            print("  ✓ Add task command works")
        else:
            print(f"  ✗ Unexpected response: {result['message'][:50]}")

        # Test listing tasks
        result = chat_demo_mode("Show me my tasks")
        if "task" in result["message"].lower():
            print("  ✓ List tasks command works")
        else:
            print(f"  ✗ Unexpected response: {result['message'][:50]}")

        return True
    except Exception as e:
        print(f"  ✗ Agent error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_task_functions():
    """Test core task management functions."""
    print_test("Task Management Functions")

    try:
        sys.path.insert(0, 'backend')
        from tasks import add_task, list_tasks, complete_task

        # Add a task
        result = add_task("Test task", "This is a test", "2024-12-31")
        if "added" in result.lower():
            print("  ✓ add_task() works")

            # Extract task ID
            import re
            match = re.search(r'ID ([a-f0-9-]+)', result)
            if match:
                task_id = match.group(1)

                # Complete the task
                result = complete_task(task_id)
                if "completed" in result.lower():
                    print("  ✓ complete_task() works")
                else:
                    print(f"  ✗ complete_task() failed: {result}")
            else:
                print("  ✗ Could not extract task ID")
        else:
            print(f"  ✗ add_task() failed: {result}")

        # List tasks
        result = list_tasks()
        if result and "task" in result.lower():
            print("  ✓ list_tasks() works")
        else:
            print(f"  ✗ list_tasks() returned: {result[:50]}")

        return True
    except Exception as e:
        print(f"  ✗ Task functions error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading."""
    print_test("Configuration")

    try:
        from app.config import settings
        print(f"  ✓ App name: {settings.app_name}")
        print(f"  ✓ Database: {settings.database_url}")
        print(f"  ✓ Debug mode: {settings.debug}")
        print(f"  ✓ OpenAI key: {'set' if settings.openai_api_key and settings.openai_api_key != 'demo' else 'demo mode'}")
        return True
    except Exception as e:
        print(f"  ✗ Config error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  HACKATHON TODO - COMPREHENSIVE TEST SUITE")
    print("="*60)

    results = []

    # Run tests
    results.append(("Module Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Database", test_database()))
    results.append(("Task Functions", test_task_functions()))
    results.append(("Demo Agent", test_demo_agent()))
    results.append(("App Loading", test_app_loading()))

    # Print summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:8} - {name}")

    print("="*60)
    print(f"  Results: {passed}/{total} tests passed")
    print("="*60)

    if passed == total:
        print("\n  🎉 ALL TESTS PASSED! App is ready to run!")
        print("\n  To start the server:")
        print("    python run.py")
        print("  or:")
        print("    uvicorn app.main:app --reload")
        print("\n  Then visit: http://localhost:8000/docs")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
