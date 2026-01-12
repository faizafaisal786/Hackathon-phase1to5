"""
Vercel entry point for the FastAPI backend.
This file exposes the FastAPI app for Vercel's serverless functions.
"""
from main import app

# Vercel expects a variable named 'app' or a handler function
# The FastAPI app is already defined in main.py, so we just import it
