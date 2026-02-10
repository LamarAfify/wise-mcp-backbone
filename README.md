# wise-mcp-backbone

An **agentic workflow management system** built on the **Model Context Protocol (MCP)** that allows an AI agent to directly create, update, and manage real project operations moving beyond “AI advice” to **AI execution**.

This project demonstrates how an MCP-enabled agent can coordinate teams, assign work intelligently, and maintain project state through direct tool invocation rather than human-driven UI workflows.

---

## Concept: From Chaos to Control

Traditional project management tools are powerful, but coordination is slow:

- Projects require manual setup  
- Task assignment is often guesswork  
- Status updates depend on meetings, messages, and clicks  

This MCP enables an **Agentic Manager** that:

- Creates projects and teams programmatically  
- Assigns tasks based on historical performance and skill signals  
- Updates milestones and project state in real time  
- Synchronizes changes instantly with a live dashboard  

The agent does not simulate actions, it **executes real system changes** through MCP tools.

---

## What This Project Does

- Implements a **Python-based MCP server** with executable operational tools  
- Allows an AI agent to:
  - Create projects
  - Add team members
  - Assign tasks
  - Update milestones and project status
- Uses historical data to **optimize task assignment**
- Provides a **Vite + React frontend** to visualize live system state
- Demonstrates a shift from *chat-based AI* to *collaborative agent systems*

---

## Project Structure

```
wise-mcp-backbone/
├── app/                    # Core MCP application logic
│   ├── api_server.py       # MCP / API server entrypoint
│   ├── server.py           # Server lifecycle and orchestration
│   ├── config.py           # Configuration
│   ├── schemas.py          # Data models and schemas
│   ├── storage.py          # Persistence and state management
│   ├── utils.py            # Shared utilities
│   └── tools/              # Executable MCP tools
│       ├── events.py
│       ├── health.py
│       └── workflow.py
├── tools/                  # Supporting / external resources
├── frontend/               # Vite + React dashboard
│   ├── src/
│   ├── public/
│   └── package.json
├── server.py               # Top-level launcher
├── seed_data.py            # Demo / historical data
├── reset_demo.py           # Reset demo state
└── README.md
```

---

## MCP Tools

The MCP server exposes executable tools under `app/tools/`:

### Health
- System and service health checks

### Events
- Project and task lifecycle events

### Workflow
- Create projects
- Add team members
- Assign tasks
- Update milestones and progress states

Each tool is:
- Explicitly defined  
- Executed by the agent (not simulated)  
- Immediately reflected in system state and UI  

---

## Example Interaction Flow

A typical agent-driven workflow looks like:

1. Agent receives a natural language instruction  
   *“Start a new project, add the team, and set the deadline.”*

2. Agent selects and invokes MCP tools  
3. Project, team, and milestones are created programmatically  
4. Dashboard updates in real time  
5. Agent analyzes historical data to recommend task ownership  
6. Task assignment and status changes are executed instantly  

No manual setup. No UI clicks. No coordination overhead.

---

## Getting Started

### Backend (Python)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

### Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

The frontend is optional and serves as a visualization layer for MCP-driven actions.

---

## Development Notes

- Python cache files and local state are excluded from version control
- The MCP server is designed to be extended with additional tools
- The frontend can be replaced by any MCP-compatible client
- Tool boundaries are intentionally explicit to support safe agent execution

---

## Use Cases

- Agentic project and workflow management
- AI-assisted team coordination
- Demonstrating executable AI systems (not advisory chatbots)
- Research and experimentation with MCP-based agents
