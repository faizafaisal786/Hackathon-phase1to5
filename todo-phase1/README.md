# Task CRUD CLI Application

A simple command-line interface (CLI) task management system with in-memory storage, built for Phase I of the todo project.

## Features

All user stories from the specification are implemented:

- **Add Task**: Create new tasks with title and optional description
- **List Tasks**: View all tasks with their status
- **Update Task**: Modify existing task title and description
- **Delete Task**: Remove tasks with confirmation
- **Mark Task Complete**: Mark tasks as completed

## Task Properties

Each task has the following attributes:
- `id`: Unique identifier (auto-generated)
- `title`: Task title (required)
- `description`: Task description (optional)
- `completed`: Completion status (boolean)

## Installation

No external dependencies required. Python 3.6+ is needed.

## Usage

Run the application:

```bash
python src/main.py
```

## Menu Options

When you run the application, you'll see a menu with the following options:

1. **Add Task**: Create a new task
2. **List Tasks**: Display all tasks
3. **Update Task**: Modify an existing task
4. **Delete Task**: Remove a task
5. **Mark Task Complete**: Mark a task as done
6. **Exit**: Close the application

## Example Workflow

1. Select option `1` to add a task
2. Enter the task title and description
3. Select option `2` to list all tasks
4. Select option `5` to mark a task complete (enter the task ID)
5. Select option `4` to delete a task if needed

## Data Storage

Tasks are stored in memory during the application session. Data will be lost when the application exits (as per Phase I requirements).

## Implementation Details

- **Task Class**: Represents individual tasks
- **TaskManager Class**: Handles all CRUD operations
- **Menu-based Interface**: User-friendly CLI interaction
- **Input Validation**: Prevents errors from invalid input
