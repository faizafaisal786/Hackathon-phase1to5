"""
Task CRUD CLI Application
A simple menu-based task management system with in-memory storage.
"""

class Task:
    """Represents a single task with id, title, description, and completion status."""

    def __init__(self, task_id, title, description=""):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = False

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"[{self.id}] {status} {self.title}"

    def details(self):
        status = "Completed" if self.completed else "Pending"
        return f"""
Task ID: {self.id}
Title: {self.title}
Description: {self.description}
Status: {status}
"""


class TaskManager:
    """Manages tasks with CRUD operations and in-memory storage."""

    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def add_task(self, title, description=""):
        """Add a new task."""
        task = Task(self.next_id, title, description)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def list_tasks(self):
        """Return all tasks."""
        return list(self.tasks.values())

    def get_task(self, task_id):
        """Get a specific task by ID."""
        return self.tasks.get(task_id)

    def update_task(self, task_id, title=None, description=None):
        """Update an existing task."""
        task = self.tasks.get(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return True
        return False

    def delete_task(self, task_id):
        """Delete a task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id):
        """Mark a task as complete."""
        task = self.tasks.get(task_id)
        if task:
            task.completed = True
            return True
        return False


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("         TASK MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Exit")
    print("="*50)


def add_task_menu(manager):
    """Handle adding a new task."""
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()
    if not title:
        print("Error: Title cannot be empty!")
        return

    description = input("Enter task description (optional): ").strip()
    task = manager.add_task(title, description)
    print(f"✓ Task added successfully with ID: {task.id}")


def list_tasks_menu(manager):
    """Handle listing all tasks."""
    print("\n--- Task List ---")
    tasks = manager.list_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(task)

    print(f"\nTotal tasks: {len(tasks)}")


def update_task_menu(manager):
    """Handle updating a task."""
    print("\n--- Update Task ---")

    try:
        task_id = int(input("Enter task ID to update: ").strip())
    except ValueError:
        print("Error: Invalid task ID!")
        return

    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found!")
        return

    print(f"\nCurrent task details:{task.details()}")

    new_title = input("Enter new title (press Enter to keep current): ").strip()
    new_description = input("Enter new description (press Enter to keep current): ").strip()

    title = new_title if new_title else None
    description = new_description if new_description else None

    if title is None and description is None:
        print("No changes made.")
        return

    if manager.update_task(task_id, title, description):
        print("✓ Task updated successfully!")
    else:
        print("Error: Failed to update task!")


def delete_task_menu(manager):
    """Handle deleting a task."""
    print("\n--- Delete Task ---")

    try:
        task_id = int(input("Enter task ID to delete: ").strip())
    except ValueError:
        print("Error: Invalid task ID!")
        return

    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found!")
        return

    print(f"\nTask to delete:{task.details()}")
    confirm = input("Are you sure you want to delete this task? (y/n): ").strip().lower()

    if confirm == 'y':
        if manager.delete_task(task_id):
            print("✓ Task deleted successfully!")
        else:
            print("Error: Failed to delete task!")
    else:
        print("Delete operation cancelled.")


def mark_complete_menu(manager):
    """Handle marking a task as complete."""
    print("\n--- Mark Task Complete ---")

    try:
        task_id = int(input("Enter task ID to mark complete: ").strip())
    except ValueError:
        print("Error: Invalid task ID!")
        return

    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found!")
        return

    if task.completed:
        print("Task is already marked as complete!")
        return

    if manager.mark_complete(task_id):
        print("✓ Task marked as complete!")
    else:
        print("Error: Failed to mark task as complete!")


def main():
    """Main application loop."""
    manager = TaskManager()

    print("Welcome to Task Management System!")

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            add_task_menu(manager)
        elif choice == '2':
            list_tasks_menu(manager)
        elif choice == '3':
            update_task_menu(manager)
        elif choice == '4':
            delete_task_menu(manager)
        elif choice == '5':
            mark_complete_menu(manager)
        elif choice == '6':
            print("\nThank you for using Task Management System. Goodbye!")
            break
        else:
            print("Error: Invalid choice! Please select 1-6.")


if __name__ == "__main__":
    main()
