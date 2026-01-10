"""
Phase 1: Gradio Web Interface for Hugging Face Spaces
"""

import gradio as gr
import sys
import os

# Import the TaskManager from the original CLI app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from main import TaskManager

# Initialize task manager
task_manager = TaskManager()

def add_task(title, description):
    """Add a new task"""
    if not title.strip():
        return "Error: Title cannot be empty!", get_task_list()

    task = task_manager.add_task(title, description)
    return f"✓ Task added successfully with ID: {task.id}", get_task_list()

def list_tasks():
    """List all tasks"""
    return get_task_list()

def get_task_list():
    """Get formatted task list"""
    tasks = task_manager.list_tasks()
    if not tasks:
        return "No tasks found."

    output = []
    for task in tasks:
        status = "✓" if task.completed else "✗"
        output.append(f"[{task.id}] {status} {task.title}")
        if task.description:
            output.append(f"    Description: {task.description}")

    return "\n".join(output)

def delete_task(task_id):
    """Delete a task"""
    try:
        task_id = int(task_id)
    except:
        return "Error: Invalid task ID!", get_task_list()

    task = task_manager.get_task(task_id)
    if not task:
        return f"Error: Task with ID {task_id} not found!", get_task_list()

    success = task_manager.delete_task(task_id)
    if success:
        return f"✓ Task {task_id} deleted successfully!", get_task_list()
    else:
        return f"Error: Failed to delete task {task_id}!", get_task_list()

def mark_complete_task(task_id):
    """Mark task as complete"""
    try:
        task_id = int(task_id)
    except:
        return "Error: Invalid task ID!", get_task_list()

    task = task_manager.get_task(task_id)
    if not task:
        return f"Error: Task with ID {task_id} not found!", get_task_list()

    if task.completed:
        return f"Task {task_id} is already completed!", get_task_list()

    success = task_manager.mark_complete(task_id)
    if success:
        return f"✓ Task {task_id} marked as complete!", get_task_list()
    else:
        return f"Error: Failed to mark task {task_id} as complete!", get_task_list()

def update_task(task_id, new_title, new_description):
    """Update a task"""
    try:
        task_id = int(task_id)
    except:
        return "Error: Invalid task ID!", get_task_list()

    task = task_manager.get_task(task_id)
    if not task:
        return f"Error: Task with ID {task_id} not found!", get_task_list()

    title = new_title if new_title.strip() else None
    description = new_description if new_description.strip() else None

    if title is None and description is None:
        return "No changes made.", get_task_list()

    success = task_manager.update_task(task_id, title, description)
    if success:
        return f"✓ Task {task_id} updated successfully!", get_task_list()
    else:
        return f"Error: Failed to update task {task_id}!", get_task_list()

# Create Gradio interface
with gr.Blocks(title="Task Manager - Phase 1", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📝 Task Management System - Phase 1")
    gr.Markdown("Simple and efficient task manager with CRUD operations")

    with gr.Tab("➕ Add Task"):
        with gr.Row():
            with gr.Column():
                add_title = gr.Textbox(label="Task Title", placeholder="Enter task title...")
                add_desc = gr.Textbox(label="Description (optional)", placeholder="Enter description...", lines=3)
                add_btn = gr.Button("Add Task", variant="primary")
            with gr.Column():
                add_output = gr.Textbox(label="Status", lines=2)
                add_list = gr.Textbox(label="Current Tasks", lines=10)

        add_btn.click(
            fn=add_task,
            inputs=[add_title, add_desc],
            outputs=[add_output, add_list]
        )

    with gr.Tab("📋 View Tasks"):
        view_btn = gr.Button("Refresh Task List", variant="primary")
        view_output = gr.Textbox(label="All Tasks", lines=15)

        view_btn.click(
            fn=list_tasks,
            inputs=[],
            outputs=view_output
        )

    with gr.Tab("✏️ Update Task"):
        with gr.Row():
            with gr.Column():
                update_id = gr.Textbox(label="Task ID", placeholder="Enter task ID...")
                update_title = gr.Textbox(label="New Title (optional)", placeholder="Enter new title...")
                update_desc = gr.Textbox(label="New Description (optional)", placeholder="Enter new description...", lines=3)
                update_btn = gr.Button("Update Task", variant="primary")
            with gr.Column():
                update_output = gr.Textbox(label="Status", lines=2)
                update_list = gr.Textbox(label="Current Tasks", lines=10)

        update_btn.click(
            fn=update_task,
            inputs=[update_id, update_title, update_desc],
            outputs=[update_output, update_list]
        )

    with gr.Tab("✅ Mark Complete"):
        with gr.Row():
            with gr.Column():
                complete_id = gr.Textbox(label="Task ID", placeholder="Enter task ID to mark complete...")
                complete_btn = gr.Button("Mark Complete", variant="primary")
            with gr.Column():
                complete_output = gr.Textbox(label="Status", lines=2)
                complete_list = gr.Textbox(label="Current Tasks", lines=10)

        complete_btn.click(
            fn=mark_complete_task,
            inputs=[complete_id],
            outputs=[complete_output, complete_list]
        )

    with gr.Tab("🗑️ Delete Task"):
        with gr.Row():
            with gr.Column():
                delete_id = gr.Textbox(label="Task ID", placeholder="Enter task ID to delete...")
                delete_btn = gr.Button("Delete Task", variant="stop")
            with gr.Column():
                delete_output = gr.Textbox(label="Status", lines=2)
                delete_list = gr.Textbox(label="Current Tasks", lines=10)

        delete_btn.click(
            fn=delete_task,
            inputs=[delete_id],
            outputs=[delete_output, delete_list]
        )

    gr.Markdown("---")
    gr.Markdown("### 🚀 Phase 1: CLI to Web Conversion")
    gr.Markdown("Built for Hackathon | In-Memory Storage")

if __name__ == "__main__":
    demo.launch()
