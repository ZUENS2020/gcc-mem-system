<div align="center">

# 🧠 GCC Context Controller

**Git-Context-Controller (GCC) - AI Memory System with Git-Backed Version Control**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

*Structured memory management for AI agents with MCP (Model Context Protocol) integration*

[🚀 Quick Start](#-quick-start) • [📚 Examples](#-usage-examples) • [📖 API Docs](#-api-reference) • [🔌 MCP Integration](#-mcp-integration)

</div>

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🚀 Quick Start](#-quick-start)
- [💡 Usage Examples](#-usage-examples)
- [📚 API Reference](#-api-reference)
- [🔌 MCP Integration](#-mcp-integration)
- [⚙️ Configuration](#-configuration)
- [🛠️ Development](#-development)
- [🔍 Troubleshooting](#-troubleshooting)

---

## 🌟 Overview

GCC Context Controller is a **memory management system for AI agents** that provides:

- 🗂️ **Structured Memory** - Organize context with branches, commits, and logs
- 🔄 **Version Control** - Git-backed history for all memory operations
- 🔌 **MCP Integration** - Native support for Claude and other AI agents
- 🐳 **Docker Ready** - Easy deployment with Docker Compose
- 🔒 **Session Isolation** - Multi-tenant support with isolated sessions
- 📊 **Rich Context** - Metadata, logs, and structured data storage

### Why Use GCC?

AI agents working on complex projects need to:
- ✅ Remember project goals and track progress
- ✅ Work on multiple features independently (branches)
- ✅ Maintain detailed logs of all actions
- ✅ Retrieve relevant context efficiently

**GCC provides a git-like memory system that makes this possible!**

---

## ✨ Features

### Core Capabilities

```
            GCC Context Controller
  
  📝 Initialize  →  Set project goals & todos
  🌿 Branch      →  Create isolated work contexts
  💾 Commit      →  Save progress checkpoints
  📖 Context     →  Retrieve structured memory
  🔀 Merge       →  Combine branch contexts
  📊 Log         →  Record detailed action logs
  🔍 Diff        →  Compare memory versions
```

### Key Benefits

| Feature | Benefit |
|---------|---------|
| 🎯 Goal Tracking | Keep project objectives clear and accessible |
| 🔄 Branch System | Work on multiple features independently |
| 📚 Version History | Full audit trail of all memory changes |
| 🏷️ Metadata Support | Store structured data alongside context |
| 🔒 Thread-Safe | File locking prevents data corruption |
| 🌐 HTTP API | Easy integration with any client |

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────┐
│      AI Agent / Client                  │
│   (Claude, Custom Apps, etc.)           │
└──────────────┬──────────────────────────┘
               │ MCP Protocol / HTTP API
               ▼
┌─────────────────────────────────────────┐
│     GCC Context Controller              │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌─────────┐  ┌────────┐ │
│  │   MCP    │  │ FastAPI │  │Commands│ │
│  │  Proxy   │  │   API   │  │ Layer  │ │
│  └────┬─────┘  └────┬────┘  └───┬────┘ │
├───────┴─────────────┴───────────┴──────┤
│  ┌──────────────────────────────────┐  │
│  │  Core Layer                      │  │
│  │  • Storage  • Git Ops  • Lock    │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   File System (Git-backed Storage)      │
│   /data/<session_id>/.GCC/              │
└─────────────────────────────────────────┘
```

### Data Structure

```
/data/<session_id>/                    # Session root
└── .GCC/                              # GCC system root
    ├── sessions/<session_id>/         # Session data
    │   ├── main.md                    # Goals & todos
    │   └── branches/<branch>/         # Feature branches
    │       ├── commit.md              # Commit history
    │       ├── log.md                 # Action logs
    │       └── metadata.yaml          # Structured data
    └── .git/                          # Version control
```

### Workflow: From Init to Context Retrieval

```
     START
       │
       ▼
┌──────────────────────────────────────┐
│  1. POST /init                       │
│     Initialize project               │
│     • Set goal & todos               │
│     • Create main.md & git repo      │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  2. POST /branch                     │
│     Create feature branch            │
│     • Define branch purpose          │
│     • Create branch directory        │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  3. POST /commit                     │
│     Save progress checkpoint         │
│     • Update commit.md & log.md      │
│     • Create git commit              │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  4. POST /context                    │
│     Retrieve full context            │
│     • Get goal, todos, commits       │
│     • Get logs & metadata            │
└──────────────┬───────────────────────┘
               │
               ▼
              END
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (recommended) **OR** Python 3.9+

### Option 1: Docker (Recommended) 🐳

**Start in 3 commands:**

```bash
git clone https://github.com/ZUENS2020/gcc-mem-system.git
cd gcc-mem-system
docker compose up -d
```

**Verify:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

✅ **API Server:** http://localhost:8000  
📚 **Documentation:** http://localhost:8000/docs

### Option 2: Local Development 💻

**For development and testing:**

```bash
# 1. Install
pip install -e .

# 2. Run
gcc-server
```

✅ **Server running on:** http://localhost:8000

---

## 💡 Usage Examples

### Example 1: Basic Workflow

**Step 1: Initialize Project**
```bash
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API server",
    "todo": [
      "Design database schema",
      "Implement CRUD endpoints",
      "Add authentication"
    ],
    "session_id": "my-api-project"
  }'
```

<details>
<summary>📄 Response</summary>

```json
{
  "gcc_root": "/data/sessions/my-api-project/.GCC",
  "session": "my-api-project",
  "main": "/data/sessions/my-api-project/.GCC/sessions/my-api-project/main.md"
}
```
</details>

**Step 2: Create Feature Branch**
```bash
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-auth",
    "purpose": "Implement JWT-based authentication",
    "session_id": "my-api-project"
  }'
```

**Step 3: Commit Progress**
```bash
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-auth",
    "contribution": "Implemented JWT token generation",
    "log_entries": [
      "Created JWT utility functions",
      "Added token expiration logic",
      "Implemented refresh token mechanism"
    ],
    "session_id": "my-api-project"
  }'
```

**Step 4: Retrieve Context**
```bash
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-auth",
    "session_id": "my-api-project"
  }'
```

<details>
<summary>📄 Response</summary>

```json
{
  "session": "my-api-project",
  "goal": "Build a REST API server",
  "todo": ["Design database schema", "Implement CRUD endpoints", "Add authentication"],
  "branches": ["user-auth"],
  "branch": {
    "name": "user-auth",
    "purpose": "Implement JWT-based authentication",
    "commits": [...]
  }
}
```
</details>

### Example 2: Working with Multiple Branches

```bash
# Create database branch
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{"branch": "database", "purpose": "Setup PostgreSQL schema", "session_id": "my-api-project"}'

# Create API branch
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{"branch": "api-endpoints", "purpose": "Implement REST endpoints", "session_id": "my-api-project"}'

# Merge database work into main
curl -X POST http://localhost:8000/merge \
  -H "Content-Type: application/json" \
  -d '{"source_branch": "database", "target_branch": "main", "summary": "Database schema completed", "session_id": "my-api-project"}'
```

### Example 3: Adding Metadata

```bash
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-auth",
    "contribution": "Completed authentication module",
    "metadata_updates": {
      "status": "completed",
      "test_coverage": "95%",
      "dependencies": ["PyJWT", "bcrypt"]
    },
    "session_id": "my-api-project"
  }'
```

---

## 📚 API Reference

> 💡 **Tip:** For interactive API documentation, visit http://localhost:8000/docs

### Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/init` | POST | Initialize a new project session |
| `/branch` | POST | Create a new memory branch |
| `/commit` | POST | Save a progress checkpoint |
| `/context` | POST | Retrieve structured context |
| `/merge` | POST | Merge branch into another |
| `/log` | POST | Add log entries |
| `/history` | GET | Get commit history |
| `/diff` | POST | View changes between commits |
| `/show` | POST | Show file content at ref |
| `/reset` | POST | Reset repository to ref |

### Key Endpoints

#### POST /init - Initialize Session

**Request:**
```json
{
  "goal": "string",              // Optional: Project goal
  "todo": ["string"],            // Optional: Task list
  "session_id": "string"         // Optional: Auto-generated if omitted
}
```

**Response:**
```json
{
  "gcc_root": "string",
  "session": "string",
  "main": "string"
}
```

#### POST /branch - Create Branch

**Request:**
```json
{
  "branch": "string",            // Required: Branch name
  "purpose": "string",           // Required: Branch purpose
  "session_id": "string"         // Optional
}
```

#### POST /commit - Save Progress

**Request:**
```json
{
  "branch": "string",                      // Required
  "contribution": "string",                // Required: What was achieved
  "log_entries": ["string"],               // Optional: Action logs
  "metadata_updates": {"key": "value"},    // Optional: Structured data
  "update_main": "string",                 // Optional: Update main.md
  "session_id": "string"                   // Optional
}
```

#### POST /context - Get Context

**Request:**
```json
{
  "branch": "string",            // Optional: Specific branch
  "commit_id": "string",         // Optional: Specific commit
  "log_tail": 1,                 // Optional: Recent log entries
  "session_id": "string"         // Optional
}
```

**Response:**
```json
{
  "session": "string",
  "goal": "string",
  "todo": ["string"],
  "branches": ["string"],
  "branch": {
    "name": "string",
    "purpose": "string",
    "commits": [...],
    "recent_commits": ["string"]
  }
}
```

---

## 🗄️ Data Structure & Files

### Directory Layout

```
/data/<session_id>/                    # Session root
└── .GCC/                              # GCC system directory
    ├── sessions/<session_id>/         # Session-specific data
    │   ├── main.md                    # Project goals & todo list
    │   └── branches/<branch>/         # Feature branches
    │       ├── commit.md              # Commit history
    │       ├── log.md                 # Action logs
    │       └── metadata.yaml          # Structured data
    └── .git/                          # Git repository
```

### File Examples

**main.md** - Project goals and tasks
```markdown
# Goal

Build a user authentication system

## Todo

- [x] Design database schema
- [ ] Implement JWT authentication
- [ ] Add password reset
```

**commit.md** - Progress tracking
```markdown
# Branch: user-auth

=== Commit ===
Commit ID: abc123
Timestamp: 2026-02-12T10:30:00Z

Branch Purpose:
Implement JWT-based authentication

This Commit's Contribution:
Implemented JWT token generation with refresh mechanism
```

**metadata.yaml** - Structured data
```yaml
status: in_progress
test_coverage: 95%
last_updated: 2026-02-12T10:30:00Z

config:
  auth_method: jwt
  token_expiry: 3600
```

---

## 🔌 MCP Integration

### What is MCP?

**Model Context Protocol (MCP)** enables AI agents (like Claude) to communicate with external tools seamlessly.

### Quick Setup

```bash
# 1. Install with MCP support
pip install -e .

# 2. Set server URL
export GCC_SERVER_URL=http://localhost:8000

# 3. Start MCP proxy
gcc-mcp
```

### Available MCP Tools

GCC provides **10 MCP tools** for AI agents. All paths are auto-managed via `session_id`:

| Tool | Description |
|------|-------------|
| `gcc_init` | Initialize session with goal & todos |
| `gcc_branch` | Create a new feature branch |
| `gcc_commit` | Save progress checkpoint |
| `gcc_context` | Get complete session context |
| `gcc_merge` | Merge branches together |
| `gcc_log` | Add detailed log entries |
| `gcc_history` | View commit history |
| `gcc_diff` | Compare changes between commits |
| `gcc_show` | Show file content at specific commit |
| `gcc_reset` | Reset to previous state |

### Integration Architecture

```
┌──────────────┐
│    Claude    │  AI Agent
└──────┬───────┘
       │ MCP Protocol (stdio)
       ▼
┌──────────────────┐
│   gcc-mcp Proxy  │  Protocol Translation
└──────┬───────────┘
       │ HTTP Requests
       ▼
┌──────────────────┐
│  GCC Server      │  FastAPI (port 8000)
│  gcc-server      │
└──────────────────┘
```

### Usage with Claude

Once configured, Claude can use GCC tools directly:

```
You: "Initialize a project to build a web app"

Claude: [Uses gcc_init tool]
        Project initialized with goal "Build a web app"

You: "Create a branch for user authentication"

Claude: [Uses gcc_branch tool]
        Created branch "user-auth" with purpose "Implement user authentication"
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GCC_DATA_ROOT` | Base storage directory | `/data` |
| `GCC_SESSION_ID` | Session identifier | Auto-detected |
| `GCC_SERVER_URL` | API server URL | `http://localhost:8000` |
| `GCC_LOG_DIR` | Log directory | `./logs` |
| `GCC_ENABLE_AUDIT_LOG` | Enable audit logs | `true` |

### Session ID Resolution

GCC auto-detects session ID in this order:

1. `GCC_SESSION_ID` environment variable (highest priority)
2. Container hostname (when running in Docker)
3. `"default"` (fallback)

### Custom Configuration Example

```bash
# Docker with custom session
docker run -d \
  -p 8000:8000 \
  -v gcc_data:/data \
  -e GCC_SESSION_ID=my-project \
  gcc-mcp:latest

# Data stored at: /data/my-project/.GCC/
```

---

## 🛠️ Development

### Project Structure

```
gcc-mem-system/
├── src/gcc/
│   ├── core/              # Core functionality
│   │   ├── storage.py     # File operations
│   │   ├── git_ops.py     # Git operations
│   │   ├── commands.py    # High-level commands
│   │   └── lock.py        # File locking
│   ├── server/            # HTTP API
│   │   ├── app.py         # FastAPI application
│   │   └── endpoints.py   # API routes
│   ├── mcp/               # MCP proxy
│   │   └── proxy.py       # MCP↔HTTP bridge
│   └── logging/           # Logging utilities
├── tests/                 # Test suite
├── Dockerfile             # Container image
├── docker-compose.yml     # Multi-service setup
└── Makefile              # Build automation
```

### Running Tests

```bash
# All tests
make test

# Specific category
pytest tests/security -v
pytest tests/test_logging -v

# With Docker
make test-docker
```

### Docker Commands

```bash
make build          # Build image
make up             # Start services
make down           # Stop services
make logs           # View logs
make shell          # Access container shell
```

---

## 🔍 Troubleshooting

### Common Issues

**🔒 Lock Timeout Errors**

*Problem:* Operations timeout waiting for locks

*Solution:*
```bash
# Check for stale locks
ls /data/<session_id>/.GCC/.lock.*

# Remove if safe (ensure no other process is running)
rm /data/<session_id>/.GCC/.lock.*
```

**⚠️ Encoding Errors**

*Problem:* Non-English characters cause errors

*Solution:* Use English only for all text values
```bash
# ❌ Incorrect
{"contribution": "实现用户认证"}

# ✅ Correct
{"contribution": "Implemented user authentication"}
```

**🐳 Docker Container Issues**

*Problem:* Container exits immediately

*Solution:*
```bash
# Check container logs
docker logs gcc-mcp

# Check if port is already in use
lsof -i :8000
```

**❓ Need More Help?**

- 📖 API docs: http://localhost:8000/docs
- 🐛 Report issues: [GitHub Issues](https://github.com/ZUENS2020/gcc-mem-system/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ZUENS2020/gcc-mem-system/discussions)

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for AI Agents**

[⬆ Back to Top](#-overview)

</div>
