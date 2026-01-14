# Advanced Features Specification

## Overview

This document outlines the specifications for implementing advanced task management features in the hackathon-todo application.

---

## 1. Recurring Tasks

### Description
Allow users to create tasks that automatically regenerate on a schedule (daily, weekly, monthly, custom).

### Data Model Changes

#### Backend (tasks.py)
```python
# Add to task structure
{
    "id": str,
    "title": str,
    "description": str,
    "due_date": str,
    "status": str,
    "created_at": str,
    # NEW FIELDS
    "is_recurring": bool,           # Whether task repeats
    "recurrence_pattern": str,      # "daily" | "weekly" | "monthly" | "yearly" | "custom"
    "recurrence_interval": int,     # e.g., every 2 weeks = interval of 2
    "recurrence_days": list[int],   # For weekly: [0,2,4] = Mon, Wed, Fri (0=Monday)
    "recurrence_end_date": str,     # Optional end date for recurrence
    "parent_task_id": str,          # Links to original recurring task (for instances)
    "is_instance": bool             # True if this is a generated instance
}
```

#### Frontend (api.ts)
```typescript
interface Task {
  // ... existing fields
  is_recurring?: boolean;
  recurrence_pattern?: 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';
  recurrence_interval?: number;
  recurrence_days?: number[];
  recurrence_end_date?: string;
  parent_task_id?: string;
  is_instance?: boolean;
}

interface RecurrenceConfig {
  pattern: 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';
  interval: number;
  days?: number[];        // For weekly pattern
  endDate?: string;       // Optional end date
}
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks` | Extended to accept recurrence fields |
| PUT | `/api/tasks/{id}` | Can update recurrence settings |
| GET | `/api/tasks/recurring` | List only recurring task templates |
| POST | `/api/tasks/{id}/skip` | Skip next occurrence |
| DELETE | `/api/tasks/{id}/series` | Delete all instances in series |

### Backend Logic

```python
def generate_next_occurrence(task: dict) -> dict:
    """Generate the next instance of a recurring task when completed."""
    if not task.get("is_recurring"):
        return None

    next_date = calculate_next_date(
        current_date=task["due_date"],
        pattern=task["recurrence_pattern"],
        interval=task["recurrence_interval"],
        days=task.get("recurrence_days")
    )

    if task.get("recurrence_end_date") and next_date > task["recurrence_end_date"]:
        return None

    return {
        **task,
        "id": generate_uuid(),
        "due_date": next_date,
        "status": "pending",
        "is_instance": True,
        "parent_task_id": task["id"],
        "created_at": datetime.now().isoformat()
    }
```

### UI Components

#### RecurrenceSelector Component
```tsx
interface RecurrenceSelectorProps {
  value: RecurrenceConfig | null;
  onChange: (config: RecurrenceConfig | null) => void;
}

// Features:
// - Toggle for enabling recurrence
// - Dropdown for pattern selection (Daily, Weekly, Monthly, Yearly, Custom)
// - Interval input (every X days/weeks/months)
// - Day picker for weekly pattern (checkboxes for Mon-Sun)
// - Optional end date picker
```

#### Visual Indicators
- Recurring icon (circular arrow) on task cards
- "Repeats: Every Monday, Wednesday" subtitle text
- Series indicator badge

### User Stories

1. **As a user**, I can create a task that repeats daily at the same time
2. **As a user**, I can set a task to repeat on specific days of the week
3. **As a user**, I can complete a recurring task and have the next instance auto-generated
4. **As a user**, I can skip the next occurrence without completing it
5. **As a user**, I can end a recurring series by setting an end date or deleting the series

---

## 2. Due Dates

### Description
Enhanced due date functionality with time support, reminders, and overdue tracking.

### Data Model Changes

#### Backend
```python
{
    # Existing
    "due_date": str,              # ISO 8601 format: "2024-01-15T14:30:00Z"

    # NEW FIELDS
    "due_time": str,              # Optional time component: "14:30"
    "has_time": bool,             # Whether specific time is set
    "reminder_before": int,       # Minutes before due date to remind (0 = no reminder)
    "reminder_sent": bool,        # Track if reminder was sent
    "timezone": str               # User's timezone: "America/New_York"
}
```

#### Frontend
```typescript
interface Task {
  // ... existing fields
  due_date?: string;
  due_time?: string;
  has_time?: boolean;
  reminder_before?: number;       // 0, 15, 30, 60, 1440 (1 day), etc.
  timezone?: string;
}

interface DueDateConfig {
  date: Date;
  time?: string;                  // "HH:mm" format
  reminder?: number;              // minutes before
}
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks?overdue=true` | Filter overdue tasks |
| GET | `/api/tasks?due_today=true` | Filter tasks due today |
| GET | `/api/tasks?due_this_week=true` | Filter tasks due this week |
| GET | `/api/tasks/upcoming` | Get tasks due in next 7 days |

### Due Date States

```typescript
enum DueDateStatus {
  NO_DATE = 'no_date',           // No due date set
  UPCOMING = 'upcoming',         // Due date in future (>24h)
  DUE_SOON = 'due_soon',        // Due within 24 hours
  DUE_TODAY = 'due_today',      // Due today
  OVERDUE = 'overdue'           // Past due date
}

function getDueDateStatus(dueDate: string | null): DueDateStatus {
  if (!dueDate) return DueDateStatus.NO_DATE;
  const now = new Date();
  const due = new Date(dueDate);
  const hoursUntil = (due.getTime() - now.getTime()) / (1000 * 60 * 60);

  if (hoursUntil < 0) return DueDateStatus.OVERDUE;
  if (hoursUntil < 24 && isToday(due)) return DueDateStatus.DUE_TODAY;
  if (hoursUntil < 24) return DueDateStatus.DUE_SOON;
  return DueDateStatus.UPCOMING;
}
```

### UI Components

#### DateTimePicker Component
```tsx
interface DateTimePickerProps {
  value: DueDateConfig | null;
  onChange: (config: DueDateConfig | null) => void;
  showReminder?: boolean;
}

// Features:
// - Calendar date picker
// - Optional time input
// - Quick select buttons: "Today", "Tomorrow", "Next Week"
// - Reminder dropdown: None, 15 min, 30 min, 1 hour, 1 day
// - Clear button to remove due date
```

#### Due Date Badge Component
```tsx
interface DueDateBadgeProps {
  dueDate: string;
  status: DueDateStatus;
}

// Visual styling:
// - OVERDUE: Red background, "Overdue" or "X days overdue"
// - DUE_TODAY: Orange/amber background, "Due today"
// - DUE_SOON: Yellow background, "Due in X hours"
// - UPCOMING: Gray/neutral, formatted date
```

### User Stories

1. **As a user**, I can set a due date for any task
2. **As a user**, I can optionally add a specific time to the due date
3. **As a user**, I can see visual indicators for overdue tasks (red highlighting)
4. **As a user**, I can filter to see only overdue tasks
5. **As a user**, I can set reminders for upcoming due dates
6. **As a user**, I can quickly set "Today" or "Tomorrow" as due dates

---

## 3. Priorities

### Description
Allow users to set priority levels for tasks to indicate importance/urgency.

### Data Model Changes

#### Backend
```python
{
    # NEW FIELD
    "priority": int               # 0 = none, 1 = low, 2 = medium, 3 = high, 4 = urgent
}
```

#### Frontend
```typescript
enum Priority {
  NONE = 0,
  LOW = 1,
  MEDIUM = 2,
  HIGH = 3,
  URGENT = 4
}

interface Task {
  // ... existing fields
  priority?: Priority;
}

const PRIORITY_CONFIG = {
  [Priority.NONE]:   { label: 'None',   color: 'gray',   icon: null },
  [Priority.LOW]:    { label: 'Low',    color: 'blue',   icon: 'flag-outline' },
  [Priority.MEDIUM]: { label: 'Medium', color: 'yellow', icon: 'flag-half' },
  [Priority.HIGH]:   { label: 'High',   color: 'orange', icon: 'flag' },
  [Priority.URGENT]: { label: 'Urgent', color: 'red',    icon: 'flag-filled' }
};
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks?priority=3` | Filter by priority level |
| GET | `/api/tasks?min_priority=2` | Filter by minimum priority |
| PATCH | `/api/tasks/{id}/priority` | Quick priority update |

### UI Components

#### PrioritySelector Component
```tsx
interface PrioritySelectorProps {
  value: Priority;
  onChange: (priority: Priority) => void;
  size?: 'sm' | 'md' | 'lg';
}

// Features:
// - Flag icons with color coding
// - Dropdown or segmented control
// - Keyboard shortcut support (1-4 keys)
// - Tooltip showing priority name
```

#### Priority Indicator
```tsx
// Inline indicator for task list items
// - Colored flag icon
// - Optional text label
// - Left border accent color on task card
```

### Visual Design

| Priority | Color | Left Border | Icon |
|----------|-------|-------------|------|
| None | - | None | - |
| Low | `#3B82F6` (blue) | 3px blue | Outline flag |
| Medium | `#EAB308` (yellow) | 3px yellow | Half flag |
| High | `#F97316` (orange) | 3px orange | Solid flag |
| Urgent | `#EF4444` (red) | 3px red + pulse | Filled flag |

### Default Sorting

When priority is set, default task list order becomes:
1. Urgent (4) - top
2. High (3)
3. Medium (2)
4. Low (1)
5. None (0) - bottom

Within same priority, sort by due date (earliest first), then by creation date.

### User Stories

1. **As a user**, I can set a priority level when creating a task
2. **As a user**, I can change the priority of an existing task
3. **As a user**, I can see priority indicated by color and icon
4. **As a user**, I can sort tasks by priority
5. **As a user**, I can filter to show only high/urgent priority tasks

---

## 4. Tags

### Description
Allow users to categorize tasks with custom tags/labels for organization and filtering.

### Data Model Changes

#### Backend
```python
# Task structure addition
{
    "tags": list[str]             # List of tag names: ["work", "urgent", "meeting"]
}

# New Tag entity (optional, for tag management)
{
    "id": str,
    "name": str,                  # "work"
    "color": str,                 # "#3B82F6" (hex color)
    "created_at": str
}
```

#### Frontend
```typescript
interface Tag {
  id: string;
  name: string;
  color: string;
}

interface Task {
  // ... existing fields
  tags?: string[];                // List of tag names
}

// Predefined color palette for tags
const TAG_COLORS = [
  '#EF4444', // red
  '#F97316', // orange
  '#EAB308', // yellow
  '#22C55E', // green
  '#3B82F6', // blue
  '#8B5CF6', // purple
  '#EC4899', // pink
  '#6B7280', // gray
];
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tags` | List all tags (with task counts) |
| POST | `/api/tags` | Create new tag |
| PUT | `/api/tags/{id}` | Update tag (name, color) |
| DELETE | `/api/tags/{id}` | Delete tag (removes from all tasks) |
| GET | `/api/tasks?tags=work,urgent` | Filter tasks by tags (AND) |
| GET | `/api/tasks?any_tags=work,urgent` | Filter tasks by tags (OR) |
| POST | `/api/tasks/{id}/tags` | Add tags to task |
| DELETE | `/api/tasks/{id}/tags/{tag}` | Remove tag from task |

### UI Components

#### TagInput Component
```tsx
interface TagInputProps {
  selectedTags: string[];
  onChange: (tags: string[]) => void;
  availableTags: Tag[];
  allowCreate?: boolean;
}

// Features:
// - Autocomplete dropdown with existing tags
// - Create new tag inline (type + enter)
// - Remove tag with X button or backspace
// - Color dots/pills for each tag
// - Keyboard navigation
```

#### TagBadge Component
```tsx
interface TagBadgeProps {
  tag: Tag;
  size?: 'sm' | 'md';
  onRemove?: () => void;
}

// Visual:
// - Rounded pill shape
// - Background color with 20% opacity
// - Text in tag color
// - Optional X button for removal
```

#### TagFilter Component
```tsx
interface TagFilterProps {
  tags: Tag[];
  selectedTags: string[];
  onChange: (tags: string[]) => void;
  mode: 'and' | 'or';
}

// Features:
// - Checkbox list of all tags
// - Task count per tag
// - Toggle between AND/OR filtering
// - "Clear all" button
```

#### TagManager Component
```tsx
// Full page/modal for managing tags
// Features:
// - List all tags with task counts
// - Edit tag name
// - Change tag color (color picker)
// - Delete tag (with confirmation)
// - Merge tags functionality
```

### User Stories

1. **As a user**, I can add multiple tags to a task
2. **As a user**, I can create new tags on the fly while adding them
3. **As a user**, I can filter tasks by one or more tags
4. **As a user**, I can see all my tags and how many tasks each has
5. **As a user**, I can edit tag names and colors
6. **As a user**, I can delete tags (removes from all associated tasks)
7. **As a user**, I can quickly add common tags using suggestions

---

## 5. Search & Sort

### Description
Enable users to search through tasks and sort them by various criteria.

### Search Functionality

#### Backend Search Implementation
```python
def search_tasks(
    query: str,
    fields: list[str] = ["title", "description", "tags"],
    case_sensitive: bool = False
) -> list[dict]:
    """
    Search tasks by query string.
    Searches across specified fields.
    Returns tasks ordered by relevance.
    """
    results = []
    query_lower = query.lower() if not case_sensitive else query

    for task in tasks:
        score = 0

        # Title match (highest weight)
        if query_lower in (task["title"].lower() if not case_sensitive else task["title"]):
            score += 10
            if task["title"].lower().startswith(query_lower):
                score += 5  # Prefix match bonus

        # Description match
        desc = task.get("description", "")
        if query_lower in (desc.lower() if not case_sensitive else desc):
            score += 5

        # Tag match
        for tag in task.get("tags", []):
            if query_lower in (tag.lower() if not case_sensitive else tag):
                score += 3

        if score > 0:
            results.append((task, score))

    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    return [task for task, score in results]
```

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks?q=meeting` | Search tasks |
| GET | `/api/tasks?q=meeting&in=title` | Search in specific field |
| GET | `/api/tasks/search` | Advanced search with POST body |

#### Search Request Body (Advanced)
```python
class SearchRequest(BaseModel):
    query: str
    fields: list[str] = ["title", "description", "tags"]
    filters: dict = {}  # Additional filters to apply
    highlight: bool = False  # Return highlighted matches
```

### Sort Functionality

#### Sort Options
```typescript
enum SortField {
  CREATED_AT = 'created_at',
  UPDATED_AT = 'updated_at',
  DUE_DATE = 'due_date',
  PRIORITY = 'priority',
  TITLE = 'title',
  STATUS = 'status'
}

enum SortOrder {
  ASC = 'asc',
  DESC = 'desc'
}

interface SortConfig {
  field: SortField;
  order: SortOrder;
}
```

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks?sort=due_date&order=asc` | Sort by field |
| GET | `/api/tasks?sort=priority,due_date` | Multi-field sort |

#### Sort Priority Logic
```typescript
// Default sort order (can be customized)
const DEFAULT_SORT: SortConfig[] = [
  { field: SortField.STATUS, order: SortOrder.ASC },      // Pending first
  { field: SortField.PRIORITY, order: SortOrder.DESC },   // Highest priority
  { field: SortField.DUE_DATE, order: SortOrder.ASC },    // Earliest due
  { field: SortField.CREATED_AT, order: SortOrder.DESC }  // Newest
];
```

### UI Components

#### SearchBar Component
```tsx
interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSearch: (value: string) => void;
  placeholder?: string;
  showClear?: boolean;
}

// Features:
// - Search icon
// - Input field with placeholder
// - Clear button (X) when has value
// - Debounced search (300ms delay)
// - Keyboard shortcuts (Cmd/Ctrl + K to focus)
// - Search suggestions dropdown (recent searches)
```

#### SortDropdown Component
```tsx
interface SortDropdownProps {
  value: SortConfig;
  onChange: (config: SortConfig) => void;
  options: SortField[];
}

// Features:
// - Dropdown with sort options
// - Toggle asc/desc with click or icon
// - Current sort indicator
// - "Reset to default" option
```

#### FilterBar Component (Combined)
```tsx
interface FilterBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  sort: SortConfig;
  onSortChange: (config: SortConfig) => void;
  filters: FilterConfig;
  onFiltersChange: (filters: FilterConfig) => void;
}

interface FilterConfig {
  status?: 'all' | 'pending' | 'completed';
  priority?: Priority[];
  tags?: string[];
  dueDateRange?: { start: string; end: string };
  hasRecurrence?: boolean;
}
```

### Search Results Display

```tsx
interface SearchResultsProps {
  results: Task[];
  query: string;
  isLoading: boolean;
  totalCount: number;
}

// Features:
// - Highlight matching text in results
// - Show "X results found" count
// - Empty state when no results
// - Loading skeleton during search
// - Clear search to show all tasks
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + K` | Focus search bar |
| `Escape` | Clear search / close dropdown |
| `Cmd/Ctrl + Shift + S` | Open sort menu |
| `/` | Quick search (when not in input) |

### User Stories

1. **As a user**, I can search tasks by typing in a search box
2. **As a user**, I can see matching results highlighted
3. **As a user**, I can sort tasks by due date, priority, creation date, or title
4. **As a user**, I can toggle between ascending and descending order
5. **As a user**, I can combine search with filters (e.g., search "meeting" in high priority tasks)
6. **As a user**, I can clear search to return to the full task list
7. **As a user**, I can use keyboard shortcuts for quick search access

---

## Implementation Order (Recommended)

### Phase 1: Foundation
1. **Due Dates** - Enhances existing field, adds filtering
2. **Priorities** - Simple addition, high visual impact

### Phase 2: Organization
3. **Tags** - Adds categorization layer
4. **Search & Sort** - Enables finding tasks quickly

### Phase 3: Automation
5. **Recurring Tasks** - Most complex, builds on due dates

---

## Database Schema (Future Migration)

When migrating from in-memory to persistent storage:

```sql
-- Tasks table with all new fields
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',

    -- Due dates
    due_date TIMESTAMP WITH TIME ZONE,
    has_time BOOLEAN DEFAULT FALSE,
    reminder_before INTEGER DEFAULT 0,
    reminder_sent BOOLEAN DEFAULT FALSE,
    timezone VARCHAR(50),

    -- Priority
    priority INTEGER DEFAULT 0,

    -- Recurrence
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(20),
    recurrence_interval INTEGER DEFAULT 1,
    recurrence_days INTEGER[],
    recurrence_end_date DATE,
    parent_task_id UUID REFERENCES tasks(id),
    is_instance BOOLEAN DEFAULT FALSE,

    -- Metadata
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tags table
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#6B7280',
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, owner_id)
);

-- Task-Tag junction table
CREATE TABLE task_tags (
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- Indexes for common queries
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_owner ON tasks(owner_id);
CREATE INDEX idx_tasks_search ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));
```

---

## API Response Format

All endpoints should follow consistent response format:

```typescript
// Success response
interface ApiResponse<T> {
  success: true;
  data: T;
  meta?: {
    total: number;
    page: number;
    limit: number;
    sort?: SortConfig;
    filters?: FilterConfig;
  };
}

// Error response
interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
  };
}
```

---

## Testing Requirements

### Unit Tests
- Priority sorting logic
- Due date status calculation
- Recurrence date calculation
- Search relevance scoring
- Tag filtering (AND/OR logic)

### Integration Tests
- CRUD operations with new fields
- Filter combinations
- Sort + search + filter together
- Recurring task generation on completion

### E2E Tests
- Create task with all features enabled
- Search and find task
- Complete recurring task and verify next instance
- Filter by multiple criteria
