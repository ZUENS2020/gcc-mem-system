<div align="center">

# 🧠 GCC Context Controller

**Git-Context-Controller (GCC) - AI Memory System with Git-Backed Version Control**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

*Structured memory management for AI agents with MCP (Model Context Protocol) integration*

[Quick Start](#quick-start) • [Features](#-features) • [Architecture](#-architecture) • [API Reference](#-api-reference) • [Examples](#-usage-examples)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [API Reference](#-api-reference)
- [Data Structure](#-data-structure)
- [MCP Integration](#-mcp-integration)
- [Configuration](#-configuration)
- [Development](#-development)

---

## 🌟 Overview

GCC Context Controller is a **memory management system** designed for AI agents that provides:

- 🗂️ **Structured Memory**: Organize context with branches, commits, and logs
- 🔄 **Version Control**: Git-backed history for all memory operations
- 🔌 **MCP Integration**: Native support for Claude and other AI agents
- 🐳 **Docker Ready**: Easy deployment with Docker Compose
- 🔒 **Session Isolation**: Multi-tenant support with isolated sessions
- 📊 **Rich Context**: Metadata, logs, and structured data storage

### Why GCC?

When AI agents work on complex projects, they need to:
- Remember project goals and progress
- Track work across multiple branches/features
- Maintain structured logs of actions
- Retrieve relevant context efficiently

GCC provides a **git-like memory system** that makes this possible!

---

## ✨ Features

### Core Capabilities

```
              GCC Context Controller
  📝 Initialize    →  Set project goals & todos
  🌿 Branch        →  Create isolated work contexts
  💾 Commit        →  Save progress checkpoints
  📖 Context       →  Retrieve structured memory
  🔀 Merge         →  Combine branch contexts
  📊 Log           →  Record detailed action logs
  🔍 Diff          →  Compare memory versions
```

### Key Benefits

| Feature | Benefit |
|---------|---------|
| 🎯 **Goal Tracking** | Keep project objectives clear and accessible |
| 🔄 **Branch System** | Work on multiple features independently |
| 📚 **Version History** | Full audit trail of all memory changes |
| 🏷️ **Metadata Support** | Store structured data alongside context |
| 🔒 **Thread-Safe** | File locking prevents data corruption |
| 🌐 **HTTP API** | Easy integration with any client |

---

## 🏗️ Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    AI Agent / Client                        │
│                (Claude, Custom Apps, etc.)                   │
└────────────────────┬─────────────────────────────────────────────┘
                     │ MCP Protocol / HTTP API
└────────────────────┼─────────────────────────────────────────────┘
                     ▼
              ┌─────────────────────────────┐
              │   GCC Context Controller    │
              └─────────────────────────────┘
       ┌──────────┬──────────────┬─────────┐
       │ MCP Proxy │ FastAPI     │ Commands │
       │  (stdio)  │──│   │   │
       │           │   │   │   │
┌──────┴──┬─────────┴──┬─────┴────────┐
│    │   │   │   │   │            │
│    │   │   │   │   ▼            │
│    │   │   │   │   Storage    │   │
│    │   │   │   │   Git Ops   │   │
│    │   │   │   │   Lock      │   │
│    │   │   │   └─────────────┘   │
└────────┴─────────────────────────────┘
```

### Data Structure

```
/data/<session_id>/                     # Session root
└── .GCC/                             # GCC system root
    ├── sessions/<session_id>/           # Session data
    │   ├── main.md                     # Goals & todos
    │   └── branches/<branch>/          # Feature branches
    │       ├── commit.md              # Commit history
    │       ├── log.md                  # Action logs
    │       └── metadata.yaml           # Structured data
    └── .git/                        # Version control
```

### Workflow: From Init to Context Retrieval

```
┌─────────┐
│ START  │
└────┬───┘
     │
     ▼
┌────────────────────▼───────────────────────────────┐
│ POST /init     │ Initialize project with goal & todos   │
│                 │ Creates: main.md, git repo            │
└─────────────────────────┬───────────────────────────────────┘
                      │
                      ▼
         ┌─────────────────────────────────┐
         │ POST /branch  │ Create feature branch       │
         │                 │ Creates: branch dir, docs   │
         └─────────────────────────┬───────────┘
                             │
                             ▼
                    ┌──────────────────────────────────────┐
                    │ POST /commit  │ Save progress checkpoint    │
                    │                 │ Updates: commit.md, log.md   │
                    │                 │ Creates: git commit          │
                    └─────────────────────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────────────────┐
                              │ POST /context  │ Retrieve full context      │
                              │                 │ Returns: goal, todos,       │
                              │                 │   commits, logs, metadata│
                              └─────────────────────────┬───────────┘
                                                  │
                                              END
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
- OR **Python 3.9+** (for local development)

### Method 1: Docker Compose (Recommended)

Perfect for production use and quick setup:

```bash
# Clone repository
git clone https://github.com/ZUENS2020/gcc-mem-system.git
cd gcc-mem-system

# Start service
docker compose up -d

# Verify it's running
curl http://localhost:8000/health
```

✅ **Service available at:** `http://localhost:8000`
📚 **API Documentation:** `http://localhost:8000/docs`

### Method 2: Local Development

For development and testing:

```bash
# Install dependencies
pip install -e .

# Run server
gcc-server
```

---

## 💡 Usage Examples

### Example 1: Initialize Project

```bash
# Initialize a new project (no root needed!)
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API server",
    "todo": [
      "Design database schema",
      "Implement CRUD endpoints",
      "Add authentication middleware"
    ],
    "session_id": "api-project"
  }'
```

**Response:**
```json
{
  "gcc_root": "/data/sessions/api-project/.GCC",
  "session": "api-project",
  "main": "/data/sessions/api-project/.GCC/sessions/api-project/main.md"
}
```

### Example 2: Feature Branch Workflow

```bash
# Create a branch for feature work
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-auth",
    "purpose": "Implement JWT-based authentication",
    "session_id": "api-project"
  }'

# Make progress and commit
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-auth",
    "contribution": "Implemented JWT token generation with refresh mechanism",
    "log_entries": [
      "Created JWT utility functions",
      "Added token expiration logic",
      "Implemented refresh token mechanism"
    ],
    "session_id": "api-project"
  }'
```

### Example 3: Retrieve Context

```bash
# Get full context for a branch
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-auth",
    "session_id": "api-project"
  }'
```

**Response:**
```json
{
  "session": "api-project",
  "main": "# Goal: Build a REST API server...",
  "goal": "Build a REST API server",
  "todo": ["Design database schema", "..."],
  "branches": ["user-auth"],
  "branch": {
    "name": "user-auth",
    "purpose": "Implement JWT-based authentication",
    "commits": [...]
  }
}
```

---

## 📚 API Reference

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/init` | Initialize a new project session |
| `POST` | `/branch` | Create a new memory branch |
| `POST` | `/commit` | Save a progress checkpoint |
| `POST` | `/context` | Retrieve structured context |
| `POST` | `/merge` | Merge branch into another |
| `POST` | `/log` | Add log entries |
| `GET` | `/history` | Get commit history |
| `POST` | `/diff` | View changes between commits |
| `POST` | `/show` | Show file content at ref |
| `POST` | `/reset` | Reset repository to ref |

### POST /init

**Initialize a new project session**

All paths are automatically managed by the server using `session_id`. No need to specify root paths.

```json
{
  "goal": "string",           // Optional: Project goal
  "todo": ["string"],        // Optional: Task list
  "session_id": "string"       // Optional: Auto-generated if not provided
}
```

**Response:**
```json
{
  "gcc_root": "/data/sessions/{session}/.GCC",
  "session": "{session}",
  "main": "/data/sessions/{session}/.GCC/sessions/{session}/main.md"
}
```

### POST /branch

**Create a new memory branch**

```json
{
  "branch": "string",           // Required: Branch name
  "purpose": "string",          // Required: Branch description
  "session_id": "string"         // Optional: Uses default if not provided
}
```

### POST /commit

**Save a progress checkpoint**

```json
{
  "branch": "string",                     // Required: Branch name
  "contribution": "string",             // Required: What was achieved
  "log_entries": ["string"],            // Optional: Action log items
  "metadata_updates": {"key": "value"},  // Optional: Structured data
  "update_main": "string",              // Optional: Text to append to main.md
  "session_id": "string"                 // Optional: Session identifier
}
```

### POST /context

**Retrieve structured context**

```json
{
  "branch": "string",           // Optional: Specific branch
  "commit_id": "string",      // Optional: Specific commit
  "log_tail": 1,              // Optional: Number of recent log entries
  "metadata_segment": "string", // Optional: Metadata key to retrieve
  "session_id": "string"         // Optional: Session identifier
}
```

**Response:**
```json
{
  "session": "string",
  "main": "# Goal: ...\n## Todo\n- ...",
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

## 🗄️ Data Structure

### File System Layout

```
/data/<session_id>/                     # Auto-managed session root
└── .GCC/                             # GCC system root
    ├── sessions/<session_id>/           # Session-specific data
    │   ├── main.md                     # Project goals and todo list
    │   └── branches/<branch>/          # Feature branches
    │       ├── commit.md              # Commit history and progress
    │       ├── log.md                  # Detailed action logs
    │       └── metadata.yaml           # Structured metadata storage
    └── .git/                        # Git repository for version control
```

### File Contents

#### main.md
```markdown
# Goal

Build a user authentication system

## Todo

- [x] Design database schema
- [ ] Implement JWT authentication
- [ ] Add password reset functionality
```

#### commit.md
```markdown
# Branch: user-auth

=== Commit ===
Commit ID: abc123
Timestamp: 2026-02-12T10:30:00Z

Branch Purpose:
Implement JWT-based authentication

Previous Progress Summary:
(none)

This Commit's Contribution:
Implemented JWT token generation with refresh mechanism
```

#### metadata.yaml
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

Model Context Protocol (MCP) enables seamless communication between AI agents (like Claude) and external tools.

### Setup MCP Proxy

```bash
# Install MCP proxy
pip install -e .

# Set server URL
export GCC_SERVER_URL=http://localhost:8000

# Start MCP proxy
gcc-mcp
```

### MCP Tools

GCC provides 10 tools for AI agents. **No path management required** - all paths are auto-managed via `session_id`:

| Tool | Description | Parameters |
|------|-------------|------------|
| `gcc_init` | Initialize session | `goal`, `todo`, `session_id` |
| `gcc_branch` | Create branch | `branch`, `purpose`, `session_id` |
| `gcc_commit` | Save checkpoint | `branch`, `contribution`, `log_entries`, `session_id` |
| `gcc_merge` | Merge branches | `source_branch`, `target_branch`, `summary`, `session_id` |
| `gcc_context` | Get context | `branch`, `commit_id`, `log_tail`, `session_id` |
| `gcc_log` | Add logs | `branch`, `entries`, `session_id` |
| `gcc_history` | Get history | `limit`, `session_id` |
| `gcc_diff` | View changes | `from_ref`, `to_ref`, `session_id` |
| `gcc_show` | Show file | `ref`, `path`, `session_id` |
| `gcc_reset` | Reset repo | `ref`, `mode`, `confirm`, `session_id` |

### Integration Flow

```
┌──────────────┐
│    Claude    │  (AI Agent)
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│   MCP Protocol (stdio)    │
└──────────┬─────────────────┘
           │
           ▼
    ┌─────────────────────┐
    │  gcc-mcp (Proxy) │
    └──────────┬─────────┘
               │
               ▼
         ┌────────────────┐
         │ HTTP API (8000) │
         │  GCC Server      │
         │  (FastAPI)       │
         └─────────────────┘
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GCC_DATA_ROOT` | Base path for data storage | `/data` |
| `GCC_SESSION_ID` | Session identifier | Auto-detected |
| `GCC_SERVER_URL` | HTTP API server URL | `http://localhost:8000` |
| `GCC_LOG_DIR` | Log directory | `./logs` |
| `GCC_ENABLE_AUDIT_LOG` | Enable audit logging | `true` |

### Session ID Resolution

GCC automatically determines session ID using this priority:

1. **GCC_SESSION_ID** environment variable (highest priority)
2. **Container hostname** (Docker mode)
3. **"default"** (fallback)

### Custom Session Example

```bash
docker run -d \
  -p 8000:8000 \
  -v gcc_data:/data \
  -e GCC_SESSION_ID=production-session \
  gcc-mcp:latest
```

Data will be stored at: `/data/production-session/.GCC/`

---

## 🛠️ Development

### Project Structure

```
gcc-mem-system/
├── src/
│   └── gcc/
│       ├── core/              # Core functionality
│       │   ├── storage.py     # File operations
│       │   ├── git_ops.py     # Git operations
│       │   ├── commands.py    # High-level commands
│       │   ├── validators.py  # Input validation
│       │   ├── exceptions.py   # Custom exceptions
│       │   └── lock.py        # File locking
│       ├── server/            # HTTP API
│       │   ├── app.py         # FastAPI app
│       │   ├── endpoints.py    # API routes
│       │   └── middleware.py  # Request handling
│       ├── mcp/              # MCP proxy
│       │   └── proxy.py      # MCP→HTTP translation
│       └── logging/          # Logging utilities
│           ├── logger.py      # Structured logging
│           └── audit.py        # Audit logging
├── tests/                    # Test suite
│   ├── test_api.py         # API tests
│   ├── security/            # Security tests
│   └── test_logging/        # Logging tests
├── Dockerfile                 # Container image
├── docker-compose.yml          # Multi-service setup
├── pyproject.toml            # Package config
└── Makefile                   # Build automation
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test category
python -m pytest tests/security -v
python -m pytest tests/test_logging -v

# Run tests in Docker
make test-docker
```

---

## 🐳 Docker Deployment

### Docker Compose Services

```yaml
services:
  gcc-mcp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - gcc_data:/data
    environment:
      - GCC_DATA_ROOT=/data
      # Optional: Set a custom session ID
      # - GCC_SESSION_ID=my-custom-session

  gcc-test:
    build: .
    command: ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
    environment:
      - GCC_LOG_DIR=/var/log/gcc
      - GCC_ENABLE_AUDIT_LOG=true
```

### Quick Commands

```bash
# Build and start
make build
make up

# View logs
make logs

# Run tests
make test-docker

# Stop services
make down

# Access container shell
make shell
```

---

## 🔍 Troubleshooting

### Common Issues

#### 🔒 Lock Timeout Errors

**Problem:** Operations timeout waiting for locks.

**Solution:** Check if another process is holding the lock:
```bash
# Check lock files
ls /data/<session_id>/.GCC/.lock.*

# Remove stale locks (if safe)
rm /data/<session_id>/.GCC/.lock.*
```

#### ⚠️ Encoding Errors with Non-English Text

**Problem:** Chinese or non-ASCII characters cause errors.

**Solution:** Use English only for all text values:
```bash
# ❌ Don't
curl -X POST http://localhost:8000/commit -d '{
  "contribution": "实现用户认证"
}'

# ✅ Do
curl -X POST http://localhost:8000/commit -d '{
  "contribution": "Implemented user authentication"
}'
```

#### 🐳 Docker Container Not Starting

**Problem:** Container exits immediately.

**Solution:** Check logs for errors:
```bash
docker logs gcc
```

### Getting Help

- 📖 Check API docs: `http://localhost:8000/docs`
- 🐛 Report issues: [GitHub Issues](https://github.com/ZUENS2020/gcc-mem-system/issues)
- 💬 Join discussions: [GitHub Discussions](https://github.com/ZUENS2020/gcc-mem-system/discussions)

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for AI Agents**

[⬆ Back to Top](#-overview)

</div>
