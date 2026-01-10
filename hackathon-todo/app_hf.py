"""
Phase 2/3: Gradio Interface for Hackathon Todo App
Hugging Face Spaces Deployment
"""

import gradio as gr
import requests
import json
from typing import Optional

# Base API URL (will be localhost for HF Spaces with FastAPI backend)
API_URL = "http://localhost:8000"

# Global token storage
current_token = None

def register_user(email: str, username: str, password: str, full_name: str):
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password,
                "full_name": full_name
            }
        )

        if response.status_code == 200:
            data = response.json()
            return f"✓ Registration successful!\nUser ID: {data['id']}\nUsername: {data['username']}"
        else:
            return f"❌ Error: {response.json().get('detail', 'Registration failed')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def login_user(username: str, password: str):
    """Login and get token"""
    global current_token
    try:
        response = requests.post(
            f"{API_URL}/auth/token",
            data={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:
            data = response.json()
            current_token = data['access_token']
            return f"✓ Login successful!\nToken: {current_token[:20]}...\nType: {data['token_type']}"
        else:
            return f"❌ Error: {response.json().get('detail', 'Login failed')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def create_task(title: str, description: str):
    """Create a new task"""
    if not current_token:
        return "❌ Please login first!"

    try:
        response = requests.post(
            f"{API_URL}/tasks",
            json={
                "title": title,
                "description": description,
                "completed": False
            },
            headers={"Authorization": f"Bearer {current_token}"}
        )

        if response.status_code == 200:
            data = response.json()
            return f"✓ Task created!\nID: {data['id']}\nTitle: {data['title']}"
        else:
            return f"❌ Error: {response.json().get('detail', 'Task creation failed')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def list_tasks():
    """List all tasks"""
    if not current_token:
        return "❌ Please login first!"

    try:
        response = requests.get(
            f"{API_URL}/tasks",
            headers={"Authorization": f"Bearer {current_token}"}
        )

        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                return "No tasks found."

            output = []
            for task in tasks:
                status = "✓" if task['completed'] else "✗"
                output.append(f"\n[{task['id']}] {status} {task['title']}")
                if task.get('description'):
                    output.append(f"    Description: {task['description']}")
                output.append(f"    Created: {task.get('created_at', 'N/A')}")

            return "\n".join(output)
        else:
            return f"❌ Error: {response.json().get('detail', 'Failed to fetch tasks')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def chat_with_ai(message: str):
    """Chat with AI assistant"""
    if not current_token:
        return "❌ Please login first!"

    try:
        response = requests.post(
            f"{API_URL}/chat/",
            json={"message": message},
            headers={"Authorization": f"Bearer {current_token}"}
        )

        if response.status_code == 200:
            data = response.json()
            return f"🤖 AI: {data['response']}"
        else:
            return f"❌ Error: {response.json().get('detail', 'Chat failed')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Hackathon Todo - Phase 2/3", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 Hackathon Todo App - Full Stack + AI")
    gr.Markdown("Complete task management with authentication and AI chatbot")

    with gr.Tab("🔐 Register"):
        gr.Markdown("### Create New Account")
        with gr.Row():
            with gr.Column():
                reg_email = gr.Textbox(label="Email", placeholder="user@example.com")
                reg_username = gr.Textbox(label="Username", placeholder="username")
                reg_password = gr.Textbox(label="Password", type="password", placeholder="password")
                reg_fullname = gr.Textbox(label="Full Name", placeholder="John Doe")
                reg_btn = gr.Button("Register", variant="primary")
            with gr.Column():
                reg_output = gr.Textbox(label="Registration Status", lines=5)

        reg_btn.click(
            fn=register_user,
            inputs=[reg_email, reg_username, reg_password, reg_fullname],
            outputs=reg_output
        )

    with gr.Tab("🔑 Login"):
        gr.Markdown("### Login to Your Account")
        with gr.Row():
            with gr.Column():
                login_username = gr.Textbox(label="Username", placeholder="username")
                login_password = gr.Textbox(label="Password", type="password", placeholder="password")
                login_btn = gr.Button("Login", variant="primary")
            with gr.Column():
                login_output = gr.Textbox(label="Login Status", lines=5)

        login_btn.click(
            fn=login_user,
            inputs=[login_username, login_password],
            outputs=login_output
        )

    with gr.Tab("➕ Create Task"):
        gr.Markdown("### Add New Task")
        with gr.Row():
            with gr.Column():
                task_title = gr.Textbox(label="Task Title", placeholder="Enter task title...")
                task_desc = gr.Textbox(label="Description", placeholder="Enter description...", lines=3)
                create_btn = gr.Button("Create Task", variant="primary")
            with gr.Column():
                create_output = gr.Textbox(label="Status", lines=5)

        create_btn.click(
            fn=create_task,
            inputs=[task_title, task_desc],
            outputs=create_output
        )

    with gr.Tab("📋 My Tasks"):
        gr.Markdown("### View All Tasks")
        list_btn = gr.Button("Refresh Task List", variant="primary")
        list_output = gr.Textbox(label="My Tasks", lines=15)

        list_btn.click(
            fn=list_tasks,
            inputs=[],
            outputs=list_output
        )

    with gr.Tab("🤖 AI Chat"):
        gr.Markdown("### Chat with AI Assistant")
        gr.Markdown("Try: *'Add a task to buy groceries'* or *'Show my tasks'*")
        with gr.Row():
            with gr.Column():
                chat_input = gr.Textbox(label="Your Message", placeholder="Type your message...", lines=2)
                chat_btn = gr.Button("Send", variant="primary")
            with gr.Column():
                chat_output = gr.Textbox(label="AI Response", lines=10)

        chat_btn.click(
            fn=chat_with_ai,
            inputs=[chat_input],
            outputs=chat_output
        )

    gr.Markdown("---")
    gr.Markdown("### 🎯 Phase 2 & 3: Full Stack + AI Integration")
    gr.Markdown("Built for Hackathon | FastAPI + Next.js + OpenAI")

if __name__ == "__main__":
    demo.launch(server_port=7860)
