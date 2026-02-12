<div align="center">

# 🧠 GCC Context Controller

**Git-Context-Controller (GCC) - AI Memory System with Git-Backed Version Control**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

*Structured memory management for AI agents with MCP (Model Context Protocol) integration*

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [API Reference](#-api-reference) • [Examples](#-usage-examples)

</div>

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
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

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
| 🔐 **Thread-Safe** | File locking prevents data corruption |
| 🌐 **HTTP API** | Easy integration with any client |

---

## 🏗️ Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         AI Agent / Client                        │
│                    (Claude, Custom Apps, etc.)                   │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     │ MCP Protocol / HTTP API
                     │
┌────────────────────▼───────────────────────────────────────────┐
│                      GCC Context Controller                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ MCP Proxy    │  │  FastAPI     │  │  Commands    │          │
│  │  (stdio)     │──│   Server     │──│   Layer      │          │
│  └──────────────┘  └──────────────┘  └──────┬───────┘          │
│                                             │                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────▼───────┐          │
│  │   Storage    │──│  Git Ops     │──│    Lock      │          │
│  │   Manager    │  │  (libgit2)   │  │   Manager    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────┬───────────────────────────────────────────┘
                     │
                     │ File System
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                      Persistent Storage                         │
│  /data/<session_id>/.GCC/                                       │
│    ├── sessions/<session_id>/                                   │
│    │   ├── main.md                  (Goals & Todos)             │
│    │   └── branches/<branch>/                                   │
│    │       ├── commit.md            (Commit History)            │
│    │       ├── log.md               (Action Logs)               │
│    │       └── metadata.yaml        (Structured Data)           │
│    └── .git/                        (Version Control)           │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow: From Init to Context Retrieval

```
    ┌─────────┐
    │  START  │
    └────┬────┘
         │
         ▼
    ┌────────────────┐
    │  POST /init    │  Initialize project with goal & todos
    │  Creates:      │
    │  • main.md     │
    │  • git repo    │
    └────┬───────────┘
         │
         ▼
    ┌────────────────┐
    │ POST /branch   │  Create feature branch for specific work
    │  Creates:      │
    │  • branch dir  │
    │  • branch docs │
    └────┬───────────┘
         │
         ▼
    ┌────────────────┐
    │ POST /commit   │  Save progress checkpoint
    │  Updates:      │
    │  • commit.md   │
    │  • log.md      │
    │  • metadata    │
    │  • git commit  │
    └────┬───────────┘
         │
         ▼
    ┌────────────────┐
    │ POST /context  │  Retrieve all relevant context
    │  Returns:      │
    │  • goal        │
    │  • todos       │
    │  • commits     │
    │  • logs        │
    │  • metadata    │
    └────┬───────────┘
         │
         ▼
    ┌─────────┐
    │   END   │
    └─────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
- OR **Python 3.9+** (for local development)

### Method 1: Docker Compose (Recommended) ⭐

Perfect for production use and quick setup:

```bash
# Clone the repository
git clone https://github.com/ZUENS2020/gcc-mem-system.git
cd gcc-mem-system

# Start the service
docker compose up -d --build

# Verify it's running
curl http://localhost:8000/docs
```

✅ **Service available at:** `http://localhost:8000`  
📚 **API Documentation:** `http://localhost:8000/docs`

### Method 2: Docker Run

For more control over configuration:

```bash
# Build the image
docker build -t gcc-mcp:latest .

# Create a volume for persistent data
docker volume create gcc_data

# Run the container
docker run -d \
  --name gcc \
  -p 8000:8000 \
  -v gcc_data:/data \
  -e GCC_SESSION_ID=my-session \
  gcc-mcp:latest

# Check logs
docker logs gcc
```

### Method 3: Local Development

For development and testing:

```bash
# Install dependencies
pip install -e .

# Run the server
gcc-server
# OR
uvicorn gcc_mcp.server:app --reload --port 8000
```

---

## 💡 Usage Examples

### Example 1: Basic Project Setup

```bash
# Initialize a new project
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "root": "/workspace/my-project",
    "goal": "Build a user authentication system",
    "todo": [
      "Design database schema",
      "Implement JWT authentication",
      "Create login/signup endpoints",
      "Add password reset functionality"
    ],
    "session_id": "auth-project"
  }'
```

**Response:**
```json
{
  "gcc_root": "/data/auth-project/.GCC",
  "session": "auth-project",
  "main": "/data/auth-project/.GCC/sessions/auth-project/main.md"
}
```

### Example 2: Feature Branch Workflow

```bash
# Create a branch for JWT implementation
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{
    "root": "/workspace/my-project",
    "branch": "jwt-auth",
    "purpose": "Implement JWT token generation and validation",
    "session_id": "auth-project"
  }'

# Make progress and commit
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "root": "/workspace/my-project",
    "branch": "jwt-auth",
    "contribution": "Implemented JWT token generation with refresh tokens",
    "log_entries": [
      "Created JWT utility functions",
      "Added token expiration logic",
      "Implemented refresh token mechanism",
      "Added unit tests for token validation"
    ],
    "metadata_updates": {
      "status": "completed",
      "test_coverage": "95%"
    },
    "session_id": "auth-project"
  }'
```

### Example 3: Retrieve Context

```bash
# Get full context for a branch
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{
    "root": "/workspace/my-project",
    "branch": "jwt-auth",
    "session_id": "auth-project"
  }'
```

**Response:**
```json
{
  "session": "auth-project",
  "goal": "Build a user authentication system",
  "todo": ["Design database schema", "..."],
  "branch": "jwt-auth",
  "purpose": "Implement JWT token generation and validation",
  "commits": [
    {
      "contribution": "Implemented JWT token generation with refresh tokens",
      "timestamp": "2026-02-11T10:30:00Z"
    }
  ],
  "logs": [
    "Created JWT utility functions",
    "Added token expiration logic",
    "..."
  ],
  "metadata": {
    "status": "completed",
    "test_coverage": "95%"
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
| `GET` | `/diff` | View changes between commits |
| `GET` | `/history` | Get commit history |

### POST /init

**Initialize a project session**

```json
{
  "root": "project-path",           // Required: Project root path
  "goal": "Project goal",            // Optional: High-level objective
  "todo": ["task1", "task2"],        // Optional: Task list
  "session_id": "my-session"         // Optional: Session identifier
}
```

### POST /branch

**Create a new work branch**

```json
{
  "root": "project-path",            // Required: Project root path
  "branch": "feature-name",          // Required: Branch name
  "purpose": "Branch description",   // Required: Purpose of branch
  "session_id": "my-session"         // Optional: Session identifier
}
```

### POST /commit

**Save progress checkpoint**

```json
{
  "root": "project-path",                    // Required: Project root path
  "branch": "feature-name",                  // Required: Branch name
  "contribution": "What was achieved",       // Required: Summary of work
  "log_entries": ["action1", "action2"],     // Optional: Detailed logs
  "metadata_updates": {"key": "value"},      // Optional: Structured data
  "session_id": "my-session"                 // Optional: Session identifier
}
```

### POST /context

**Retrieve full context**

```json
{
  "root": "project-path",            // Required: Project root path
  "branch": "feature-name",          // Optional: Specific branch
  "session_id": "my-session"         // Optional: Session identifier
}
```

---

## 🗄️ Data Structure

### File System Layout

```
/data/
└── <session_id>/              # Isolated session directory
    └── .GCC/                  # GCC memory root
        ├── .git/              # Git repository for version control
        └── sessions/
            └── <session_id>/  # Session-specific data
                ├── main.md    # 📝 Project goals and todo list
                └── branches/
                    ├── main/
                    │   ├── commit.md      # 💾 Commit history
                    │   ├── log.md         # 📋 Action logs
                    │   └── metadata.yaml  # 🏷️ Structured metadata
                    └── feature-x/
                        ├── commit.md
                        ├── log.md
                        └── metadata.yaml
```

### File Contents

#### main.md
```markdown
# Goal
Build a user authentication system

# TODO
- [x] Design database schema
- [ ] Implement JWT authentication
- [ ] Create login/signup endpoints
- [ ] Add password reset functionality
```

#### commit.md
```markdown
## 2026-02-11T10:30:00Z
Implemented JWT token generation with refresh tokens

## 2026-02-10T15:20:00Z
Created database schema for users table
```

#### log.md
```markdown
- Created JWT utility functions
- Added token expiration logic
- Implemented refresh token mechanism
- Added unit tests for token validation
```

#### metadata.yaml
```yaml
status: completed
test_coverage: 95%
last_updated: 2026-02-11T10:30:00Z
```

---

## 🔌 MCP Integration

### What is MCP?

Model Context Protocol (MCP) enables seamless communication between AI agents (like Claude) and external tools.

### Setup MCP Proxy

```bash
# Install the MCP proxy
pip install -e .

# Set the server URL
export GCC_SERVER_URL=http://localhost:8000

# Start the MCP proxy
gcc-mcp
```

### Integration Flow

```
┌──────────────┐
│    Claude    │
│  (AI Agent)  │
└──────┬───────┘
       │ MCP Protocol (stdio)
       │
┌──────▼───────┐
│  gcc-mcp     │  ← MCP Proxy (converts stdio ↔ HTTP)
│   Proxy      │
└──────┬───────┘
       │ HTTP API
       │
┌──────▼───────┐
│  GCC Server  │  ← FastAPI Server (port 8000)
│   (Docker)   │
└──────┬───────┘
       │
┌──────▼───────┐
│  Persistent  │
│    Storage   │
└──────────────┘
```

### Add to Claude Desktop

```bash
# Install CLI
npm install -g @anthropic-ai/claude-cli

# Add MCP server
claude mcp add --scope user --transport stdio gcc -- gcc-mcp
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `GCC_DATA_ROOT` | Base path for data storage | `/data` | `/var/gcc-data` |
| `GCC_SESSION_ID` | Custom session ID | Auto-detected | `my-project` |
| `GCC_SERVER_URL` | HTTP server URL | `http://localhost:8000` | `http://gcc:8000` |

### Session ID Resolution

GCC automatically determines the session ID using this priority:

```
1. GCC_SESSION_ID environment variable     (highest priority)
         ↓
2. Container hostname (Docker)             (auto-detected)
         ↓
3. "default"                               (fallback)
```

### Custom Session Example

```bash
docker run -d \
  --name gcc \
  -p 8000:8000 \
  -v gcc_data:/data \
  -e GCC_SESSION_ID=production-session \
  -e GCC_DATA_ROOT=/data \
  gcc-mcp:latest
```

Data will be stored at: `/data/production-session/.GCC/`

---

## 🔧 Troubleshooting

### Common Issues

#### ⚠️ Encoding Errors with Non-English Text

**Problem:** Chinese or non-ASCII characters cause errors.

**Solution:** Use English only for all text values.

```bash
# ❌ Bad
"goal": "实现用户认证"

# ✅ Good
"goal": "Implement user authentication"
```

**Why?** The MCP protocol layer has limitations with non-ASCII characters on Windows.

#### 🔒 Lock Timeout Errors

**Problem:** Operations timeout waiting for locks.

**Solution:** Check if another process is holding the lock.

```bash
# Check lock files
ls /data/<session_id>/.GCC/.lock.*

# Remove stale locks (if safe)
rm /data/<session_id>/.GCC/.lock.*
```

#### 🐳 Docker Container Not Starting

**Problem:** Container exits immediately.

**Solution:** Check logs for errors.

```bash
docker logs gcc

# Common fixes:
# 1. Ensure port 8000 is available
# 2. Check volume permissions
# 3. Verify git is installed in container
```

#### 📡 Cannot Connect to MCP Proxy

**Problem:** MCP proxy cannot reach GCC server.

**Solution:** Verify server URL and network connectivity.

```bash
# Test server connectivity
curl http://localhost:8000/docs

# Set correct URL
export GCC_SERVER_URL=http://localhost:8000

# Restart proxy
gcc-mcp
```

### Getting Help

- 📖 Check API docs: `http://localhost:8000/docs`
- 🐛 Report issues: [GitHub Issues](https://github.com/ZUENS2020/gcc-mem-system/issues)
- 💬 Join discussions: [GitHub Discussions](https://github.com/ZUENS2020/gcc-mem-system/discussions)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for AI Agents**

[⬆ Back to Top](#-gcc-context-controller)

</div>
