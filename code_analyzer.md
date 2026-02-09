# Code Analysis: WISE MCP Backbone

> A technical workflow hub system with MCP server integration, REST API, and React dashboard.

---

## Overview

This codebase implements **North AI Workflow Hub**, a project management and intelligent task assignment system. It exposes functionality via two interfaces: an **MCP (Model Context Protocol) server** for AI integration and a **FastAPI REST API** for the frontend. Data persists in SQLite.

---

## Entry Points

| Entry Point | Location | Purpose |
|-------------|----------|---------|
| MCP Server | `app/server.py:17` | `create_server()` initializes NorthMCPServer with 9 tools |
| REST API | `app/api_server.py:15` | FastAPI app with CRUD endpoints |
| Frontend | `frontend/src/App.jsx:6` | React SPA with Dashboard and Onboarding views |
| Seed Data | `seed_data.py:14` | `seed()` populates demo data |

---

## Core Implementation

### 1. MCP Server (`app/server.py:17-139`)

The `create_server()` function initializes the database and creates a `NorthMCPServer` instance with 9 registered tools:

```
Lines 26-28:   Lamar_Afify_v2_health_check
Lines 30-50:   Lamar_Afify_v2_log_event
Lines 52-76:   Lamar_Afify_v2_list_events
Lines 78-91:   Lamar_Afify_v2_create_project
Lines 93-98:   Lamar_Afify_v2_onboard_user
Lines 100-106: Lamar_Afify_v2_add_milestone
Lines 108-112: Lamar_Afify_v2_complete_milestone
Lines 114-116: Lamar_Afify_v2_get_dashboard
Lines 118-121: Lamar_Afify_v2_recommend_assignee
Lines 123-137: Lamar_Afify_v2_log_work
```

**Server Configuration** (`app/config.py:4-9`):
- `APP_NAME`: from env or "WISE MCP Backbone"
- `PORT`: from env or 8000
- `SERVER_SECRET`: from `NORTH_SERVER_SECRET` env
- `DB_PATH`: from env or "data.db"
- `DEBUG`: from env, parsed as boolean

**Transport** (`app/server.py:144`): Defaults to `streamable-http`

---

### 2. REST API Server (`app/api_server.py:1-76`)

FastAPI application with CORS enabled for all origins (`line 17-23`).

| Endpoint | Method | Handler | Line |
|----------|--------|---------|------|
| `/dashboard` | GET | `get_dashboard()` | 25-27 |
| `/users` | POST | `create_user()` | 29-32 |
| `/projects` | POST | `new_project()` | 34-37 |
| `/milestones` | POST | `add_milestone_endpoint()` | 39-42 |
| `/milestones/{id}/complete` | POST | `complete_milestone_endpoint()` | 44-50 |
| `/history` | POST | `add_history()` | 52-55 |
| `/recommend/{project_id}/{task_type}` | GET | `get_recommendation()` | 57-71 |

Runs on `host="0.0.0.0", port=8000` (`line 75`).

---

### 3. Storage Layer (`app/storage.py`)

#### Database Schema (`lines 16-86`)

`init_db()` creates 5 tables:

| Table | Primary Key | Foreign Keys |
|-------|-------------|--------------|
| `events` | `id TEXT` | — |
| `projects` | `id TEXT` | — |
| `users` | `id TEXT` | — |
| `milestones` | `id TEXT` | `project_id → projects` |
| `task_history` | `id TEXT` | `user_id → users` |

#### Core Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `_connect()` | 10-13 | Opens SQLite connection with Row factory |
| `insert_event()` | 93-113 | Inserts event with JSON payload |
| `query_events()` | 116-174 | Filters events by team/type/severity/timestamp/limit |
| `create_project()` | 182-190 | Inserts new project |
| `add_user()` | 192-201 | Upserts user with skills as JSON |
| `create_milestone()` | 203-211 | Inserts milestone |
| `update_milestone_status()` | 213-221 | Updates milestone status/completion |
| `log_task_history()` | 223-231 | Records task performance data |
| `get_project_details()` | 233-249 | Returns all projects, users, milestones |
| `get_user_performance()` | 251-257 | Returns user's task history |

---

### 4. Data Schemas (`app/schemas.py`)

Pydantic models define data structures:

| Model | Lines | Key Fields |
|-------|-------|------------|
| `Event` | 8-14 | id, type, team, severity, timestamp, payload |
| `Decision` | 17-27 | id, title, made_by, owners, rationale, outcomes |
| `ResourceUpdate` | 29-37 | id, resource, team, metric, value, unit |
| `Project` | 40-45 | id, name, deadline, status, created_at |
| `User` | 48-52 | id, name, role, skills (Dict[str, float]) |
| `Milestone` | 55-62 | id, project_id, title, status, assigned_to, due_date |
| `TaskHistory` | 65-71 | id, user_id, task_type, duration_minutes, success_rating |

---

### 5. Workflow Recommendation (`app/tools/workflow.py:6-34`)

`recommend_task_assignee()` implements intelligent task assignment:

**Algorithm** (`lines 11-34`):
1. Iterates each candidate user
2. Fetches user's task history via `get_user_performance()`
3. Filters history for matching `task_type`
4. Calculates score: `avg_rating / avg_duration`
5. Returns user with highest score (or first candidate if all zero)

**Score Formula** (`line 28`):
```
score = average_success_rating / average_duration_minutes
```
Higher ratings and shorter durations yield higher scores.

---

### 6. Event Management (`app/tools/events.py`)

| Function | Lines | Action |
|----------|-------|--------|
| `log_event()` | 10-27 | Creates Event with auto-generated ID, inserts to DB |
| `list_events()` | 30-48 | Queries events with optional filters |

Uses `new_id("evt")` from `app/utils.py:12` for ID generation.

---

### 7. Utility Functions (`app/utils.py:8-13`)

| Function | Line | Return |
|----------|------|--------|
| `utc_now_iso()` | 8-9 | Current UTC time as ISO string |
| `new_id(prefix)` | 12-13 | `{prefix}_{uuid4_hex}` |

---

## Frontend Implementation

### Application Shell (`frontend/src/App.jsx:6-32`)

React component managing view state (`dashboard` | `onboarding`):
- Navigation toggles between views (`lines 14-25`)
- Conditionally renders `<Dashboard />` or `<Onboarding />` (`line 29`)

### Dashboard Component (`frontend/src/components/Dashboard.jsx`)

**State Management** (`lines 16-18`):
```javascript
const [data, setData] = useState({ projects: [], users: [], milestones: [] });
const [recommendation, setRecommendation] = useState(null);
const [selectedTaskType, setSelectedTaskType] = useState('analytics');
```

**Data Loading** (`lines 20-25`):
- Fetches from `http://localhost:8001/dashboard` on mount
- Populates projects, users, milestones

**Key Functions**:
| Function | Lines | Action |
|----------|-------|--------|
| `getRecommendation()` | 27-32 | Calls `/recommend/{projectId}/{taskType}` API |
| `toggleMilestone()` | 34-46 | POSTs to `/milestones/{id}/complete`, updates local state |

**UI Sections**:
1. **Header** (`lines 61-77`): Project name, deadline, user avatars
2. **Milestones** (`lines 79-124`): Progress bars with status badges, complete button
3. **Task Assignment** (`lines 126-169`): Task type selector, recommendation display

### Onboarding Component (`frontend/src/components/Onboarding.jsx`)

**Multi-step Form** (`line 9`): `step` state controls wizard flow

**Form Data** (`lines 10-14`):
```javascript
{ projectName: '', deadline: '', users: [{ name: '', role: 'member' }] }
```

**Step 1** (`lines 75-106`): Project name and deadline inputs
**Step 2** (`lines 108-157`): Dynamic team member list with add/remove

**Submission** (`lines 26-61`):
1. POSTs to `/projects` with generated ID (`proj-{Date.now()}`)
2. Iterates users, POSTs each to `/users` with ID `user-{Date.now()}-{Math.random()}`
3. Calls `onComplete()` callback to return to dashboard

---

## Data Flow

### 1. Project Creation via Frontend
```
Onboarding.jsx:handleSubmit (line 26)
    → POST /projects
    → api_server.py:new_project (line 35)
    → storage.py:create_project (line 182)
    → INSERT INTO projects
```

### 2. Task Assignment Recommendation
```
Dashboard.jsx:getRecommendation (line 27)
    → GET /recommend/{project_id}/{task_type}
    → api_server.py:get_recommendation (line 57)
    → workflow.py:recommend_task_assignee (line 6)
    → storage.py:get_user_performance (line 251)
    → Calculate scores, return best match
```

### 3. Milestone Completion
```
Dashboard.jsx:toggleMilestone (line 34)
    → POST /milestones/{id}/complete
    → api_server.py:complete_milestone_endpoint (line 44)
    → storage.py:update_milestone_status (line 213)
    → UPDATE milestones SET status='completed'
```

### 4. MCP Tool Invocation
```
External AI Agent
    → MCP Server (port 8000)
    → app/server.py:Lamar_Afify_v2_* functions
    → storage.py functions
    → SQLite operations
```

---

## Key Patterns

| Pattern | Location | Description |
|---------|----------|-------------|
| **MCP Decorator** | `app/server.py:26` | `@mcp.tool()` registers functions as callable tools |
| **Pydantic Validation** | `app/schemas.py` | Models enforce type safety for all data structures |
| **Repository Pattern** | `app/storage.py` | All database access abstracted through functions |
| **REST + MCP Dual Interface** | `app/` | Same storage layer serves both API and MCP |
| **Component Composition** | `frontend/src/` | App shell composes Dashboard/Onboarding |

---

## Configuration

| Variable | Source | Default | Used In |
|----------|--------|---------|---------|
| `APP_NAME` | `APP_NAME` env | "WISE MCP Backbone" | `config.py:4` |
| `PORT` | `PORT` env | 8000 | `config.py:5` |
| `SERVER_SECRET` | `NORTH_SERVER_SECRET` env | "" | `config.py:7` |
| `DB_PATH` | `DB_PATH` env | "data.db" | `config.py:8` |
| `DEBUG` | `DEBUG` env | false | `config.py:9` |
| `API_URL` | Hardcoded | "http://localhost:8001" | `Dashboard.jsx:13`, `Onboarding.jsx:6` |

---

## Error Handling

| Location | Handling |
|----------|----------|
| `seed_data.py:26,39,51,59,67,80` | `try/except sqlite3.IntegrityError` for duplicate prevention |
| `Dashboard.jsx:24,31,45` | `.catch(console.error)` for API failures |
| `Onboarding.jsx:58-60` | `try/catch` with console error logging |
| `workflow.py:24` | Division by zero guard (`if avg_duration == 0`) |

---

## File Structure

```
wise-mcp-backbone/
├── app/
│   ├── server.py          # MCP server with 9 tools
│   ├── api_server.py      # FastAPI REST endpoints
│   ├── storage.py         # SQLite data access layer
│   ├── schemas.py         # Pydantic models
│   ├── config.py          # Environment configuration
│   ├── utils.py           # ID generation, timestamps
│   └── tools/
│       ├── health.py      # Health check tool
│       ├── events.py      # Event logging/querying
│       └── workflow.py    # Task recommendation algorithm
├── frontend/
│   └── src/
│       ├── App.jsx        # Root component, view routing
│       ├── index.css      # Global styles
│       └── components/
│           ├── Dashboard.jsx   # Project/milestone/recommend UI
│           └── Onboarding.jsx  # Multi-step project setup wizard
├── tools/
│   └── resources.py       # Resource state management (standalone)
├── seed_data.py           # Demo data seeder
├── reset_demo.py          # Demo reset utility
└── data.db                # SQLite database
```
