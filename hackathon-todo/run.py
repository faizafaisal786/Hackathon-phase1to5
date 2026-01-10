#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Professional startup script for Hackathon Todo Application
Handles all initialization, checks, and startup tasks.
"""
import os
import sys
import subprocess
from pathlib import Path

# Fix Windows encoding issues
if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # Already wrapped or running in IDE

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"Python version: {sys.version.split()[0]} ✓")

def check_environment():
    """Check if .env file exists."""
    env_file = Path(".env")
    if not env_file.exists():
        print("\nWARNING: .env file not found!")
        print("Creating .env file from .env.example...")
        example_file = Path(".env.example")
        if example_file.exists():
            import shutil
            shutil.copy(example_file, env_file)
            print(".env file created! ✓")
        else:
            print("ERROR: .env.example not found!")
            sys.exit(1)
    else:
        print(".env file found ✓")

def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    required = [
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "python-jose",
        "passlib",
        "openai"
    ]

    missing = []
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print(f"  {package} ✓")
        except ImportError:
            missing.append(package)
            print(f"  {package} ✗ (missing)")

    if missing:
        print(f"\nInstalling missing packages: {', '.join(missing)}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-q"
        ] + missing)
        print("Dependencies installed ✓")
    else:
        print("All dependencies installed ✓")

def initialize_database():
    """Initialize the database."""
    print("\nInitializing database...")
    try:
        from app.database import create_db_and_tables
        create_db_and_tables()
        print("Database initialized ✓")
    except Exception as e:
        print(f"Database initialization warning: {e}")
        print("Will auto-initialize on first request...")

def check_demo_mode():
    """Check if running in demo mode."""
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key == "demo" or not api_key or api_key.startswith("demo-"):
        print("\n" + "⚡" * 30)
        print("  RUNNING IN FREE DEMO MODE")
        print("  No OpenAI API costs!")
        print("  Using built-in pattern matching for task management")
        print("⚡" * 30)
        return True
    else:
        print("\n✓ OpenAI API key detected - Using advanced AI mode")
        return False

def start_server():
    """Start the FastAPI server."""
    print_header("Starting Hackathon Todo API Server")
    print("\nServer will start at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("\nPress CTRL+C to stop the server\n")

    try:
        subprocess.run([
            "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except FileNotFoundError:
        print("\nERROR: uvicorn not found!")
        print("Installing uvicorn...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn[standard]"])
        print("\nPlease run this script again.")

def main():
    """Main entry point."""
    print_header("Hackathon Todo - Professional Startup")

    # Run checks
    check_python_version()
    check_environment()
    check_dependencies()
    check_demo_mode()
    initialize_database()

    # Start server
    start_server()

if __name__ == "__main__":
    main()
