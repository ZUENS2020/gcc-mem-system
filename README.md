<div align="center">

# 🧠 GCC 上下文控制器 / GCC Context Controller

**Git-Context-Controller (GCC) - 基于 Git 的 AI 智能体内存管理系统**  
**Git-Context-Controller (GCC) - AI Memory System with Git-Backed Version Control**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

*为 AI 智能体提供结构化内存管理，支持 MCP (模型上下文协议) 集成*  
*Structured memory management for AI agents with MCP (Model Context Protocol) integration*

[🚀 快速开始 Quick Start](#-快速开始--quick-start) • [📚 使用示例 Examples](#-使用示例--usage-examples) • [📖 API 参考 API Docs](#-api-参考--api-reference) • [🔌 MCP 集成 MCP Integration](#-mcp-集成--mcp-integration)

---

**[English](#english-documentation) | [中文文档](#中文文档)**

</div>

---

# English Documentation

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [💡 Usage Examples](#-usage-examples)
- [📚 API Reference](#-api-reference)
- [🔌 MCP Integration](#-mcp-integration)
- [⚙️ Configuration](#️-configuration)
- [🛠️ Development](#️-development)
- [🔍 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

---

## 🌟 Overview

**GCC Context Controller** is an advanced **memory management system designed specifically for AI agents**. It provides a git-like version control system for managing AI agent memory, context, and work history across multiple concurrent tasks.

### What Problem Does It Solve?

Modern AI agents face critical challenges when working on complex, long-running projects:

1. **Memory Loss** - Context is lost between sessions
2. **Task Isolation** - Need to work on multiple features independently
3. **Progress Tracking** - Difficult to maintain detailed logs of actions
4. **Context Retrieval** - Hard to efficiently retrieve relevant information
5. **Version Control** - No way to track changes and roll back mistakes

### The GCC Solution

GCC provides a **git-backed memory system** that enables AI agents to:

- 🗂️ **Structured Memory** - Organize context with branches, commits, and logs (like git for memory)
- 🔄 **Version Control** - Full history with git-backed storage for all memory operations
- 🔌 **MCP Integration** - Native support for Claude Desktop and other AI platforms via Model Context Protocol
- 🐳 **Production Ready** - Easy deployment with Docker Compose, thread-safe operations
- 🔒 **Multi-Tenant** - Session isolation allows multiple independent projects
- 📊 **Rich Context** - Store metadata, logs, and structured data alongside commits

### Why Choose GCC?

| Traditional Approach | With GCC |
|---------------------|----------|
| ❌ Context in chat history only | ✅ Persistent, structured memory storage |
| ❌ No version control for memory | ✅ Full git history with diff and rollback |
| ❌ Single linear conversation | ✅ Multiple parallel branches for tasks |
| ❌ Manual context management | ✅ Automatic context retrieval and organization |
| ❌ Lost work on restart | ✅ Survives restarts with full state preservation |

**GCC transforms AI agents from stateless tools into persistent, organized collaborators!**

---

## ✨ Features

### Core Memory Operations

```
             GCC Context Controller Architecture
  
   📝 init     →  Initialize project with goals & todos
   🌿 branch   →  Create isolated memory contexts
   💾 commit   →  Save structured progress checkpoints
   📖 context  →  Retrieve organized memory efficiently
   🔀 merge    →  Combine work from different branches
   📊 log      →  Append detailed action records
   📜 history  →  View full commit timeline
   🔍 diff     →  Compare memory states
   ⏪ reset    →  Revert to previous states
   👁️ show     →  Inspect specific versions
```

### Technical Capabilities

| Category | Features |
|----------|----------|
| **💾 Storage** | • Git-backed file system<br>• YAML metadata support<br>• Markdown documentation<br>• Binary-safe operations |
| **🔒 Concurrency** | • File-based locking<br>• Thread-safe operations<br>• Atomic commits<br>• Deadlock prevention |
| **🌐 APIs** | • RESTful HTTP API (FastAPI)<br>• MCP JSON-RPC protocol<br>• Interactive docs (Swagger/ReDoc)<br>• Health checks |
| **🎯 Organization** | • Multi-session isolation<br>• Branch-based workflows<br>• Hierarchical structure<br>• Auto-generated IDs |
| **📊 Tracking** | • Commit history<br>• Action logs<br>• Metadata tagging<br>• Timestamp tracking |
| **🔄 Git Features** | • Full version control<br>• Branch management<br>• Merge operations<br>• Diff visualization<br>• Reset capabilities |

### Key Benefits

1. **🎯 Persistent Memory** - Your AI agent never forgets. All context, goals, and progress persist across sessions.

2. **🔄 True Version Control** - Every change is tracked. View history, compare versions, and roll back mistakes.

3. **🌿 Parallel Workflows** - Work on multiple features simultaneously with isolated branches, just like in software development.

4. **📚 Structured Storage** - No more unstructured chat logs. Everything is organized: goals, todos, commits, logs, and metadata.

5. **🔌 Seamless Integration** - Works with Claude Desktop via MCP, or integrate with any application via HTTP API.

6. **🐳 Production Ready** - Docker deployment, health checks, proper logging, and error handling included.

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│          AI Agents / Client Applications            │
│   (Claude Desktop, Custom Apps, Python Scripts)     │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   MCP Protocol           HTTP REST API
   (JSON-RPC)            (OpenAPI/Swagger)
        │                         │
        └────────────┬────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│           GCC Context Controller Server             │
├─────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │  MCP Proxy   │  │  FastAPI     │  │ Commands  │ │
│  │  (stdio)     │  │  Server      │  │  Layer    │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
├─────────┴──────────────────┴────────────────┴───────┤
│              Core Business Logic Layer              │
│  ┌────────┐  ┌──────────┐  ┌────────┐  ┌────────┐ │
│  │Storage │  │ Git Ops  │  │ Locking│  │Validate│ │
│  └────────┘  └──────────┘  └────────┘  └────────┘ │
└─────────────────────┬───────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│       File System (Git-backed Storage)              │
│                                                     │
│  /data/<session_id>/.GCC/                          │
│    ├── sessions/<session_id>/                      │
│    │     ├── main.md          (goals & todos)      │
│    │     └── branches/                             │
│    │           ├── main/                           │
│    │           ├── feature-a/                      │
│    │           └── feature-b/                      │
│    └── .git/                 (version control)     │
└─────────────────────────────────────────────────────┘
```

### Data Structure Deep Dive

```
/data/<session_id>/                     # Session workspace
└── .GCC/                               # GCC system directory
    ├── sessions/<session_id>/          # Session-specific data
    │   ├── main.md                     # Project goals & todo list
    │   │                               # Example content:
    │   │                               # # Goal
    │   │                               # Build REST API
    │   │                               # ## Todo
    │   │                               # - [x] Setup database
    │   │                               # - [ ] Create endpoints
    │   │
    │   └── branches/<branch>/          # Feature branches
    │       ├── commit.md               # Commit history
    │       │                           # Format: Multiple commits
    │       │                           # separated by "=== Commit ==="
    │       │
    │       ├── log.md                  # Detailed action logs
    │       │                           # Chronological record of
    │       │                           # all operations
    │       │
    │       └── metadata.yaml           # Structured metadata
    │                                   # Example:
    │                                   # status: in_progress
    │                                   # test_coverage: 95%
    │                                   # dependencies: [PyJWT]
    │
    └── .git/                           # Git repository
        ├── objects/                    # Git objects storage
        ├── refs/                       # Branch references
        └── logs/                       # Git operation logs
```

### Component Breakdown

#### 1. **MCP Proxy** (`src/gcc/mcp/proxy.py`)
- Translates MCP JSON-RPC calls to HTTP API requests
- Handles stdin/stdout communication with Claude Desktop
- Provides 10 MCP tools for AI agents

#### 2. **FastAPI Server** (`src/gcc/server/app.py`)
- RESTful HTTP API with OpenAPI documentation
- Request validation with Pydantic models
- Health checks and error handling
- Session management and routing

#### 3. **Commands Layer** (`src/gcc/core/commands.py`)
- High-level business logic for memory operations
- Orchestrates storage and git operations
- Transaction management with file locking

#### 4. **Storage Layer** (`src/gcc/core/storage.py`)
- File system operations (create, read, update)
- Path management and validation
- YAML and Markdown file handling
- Session and branch isolation

#### 5. **Git Operations** (`src/gcc/core/git_ops.py`)
- Git repository initialization and management
- Branch creation, merging, and switching
- Commit operations with proper authoring
- History, diff, and reset capabilities

#### 6. **Locking Mechanism** (`src/gcc/core/lock.py`)
- File-based locking for concurrency control
- Timeout and retry logic
- Deadlock prevention
- Thread-safe operations

### Workflow Example: Feature Development

```
     START (Initialize Session)
        │
        ▼
┌─────────────────────────────────────┐
│  POST /init                         │
│  • Set goal: "Build REST API"       │
│  • Set todos: ["Schema", "Auth"]    │
│  • Creates: main.md + git repo      │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  POST /branch                       │
│  • Branch: "user-authentication"    │
│  • Purpose: "JWT auth system"       │
│  • Creates: branch dir + git branch │
└─────────────┬───────────────────────┘
              │
              ▼ (Work on feature)
┌─────────────────────────────────────┐
│  POST /commit (Multiple times)      │
│  • Contribution: "Added JWT utils"  │
│  • Logs: ["Created token fn"]       │
│  • Metadata: {test_coverage: 85%}   │
│  • Creates: git commit              │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  POST /context                      │
│  • Retrieves: goal, todos, commits  │
│  • Retrieves: logs, metadata        │
│  • Returns: complete context        │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  POST /merge                        │
│  • Source: "user-authentication"    │
│  • Target: "main"                   │
│  • Performs: git merge + update     │
└─────────────┬───────────────────────┘
              │
              ▼
            END
```

---

## 🚀 Quick Start

### Prerequisites

Choose your installation method:

- **Recommended**: Docker & Docker Compose (easiest, most reliable)
- **Alternative**: Python 3.9+ (for development or direct installation)
- **System**: Git must be installed (required for version control)

### Option 1: Docker Deployment 🐳 (Recommended)

Perfect for production use, testing, or if you want to get started in 30 seconds.

**Quick Start:**

```bash
# Clone the repository
git clone https://github.com/ZUENS2020/gcc-mem-system.git
cd gcc-mem-system

# Start the server (builds image if needed)
docker compose up -d

# View logs
docker compose logs -f gcc-mcp
```

**Verify it's working:**

```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Check API documentation
open http://localhost:8000/docs
```

✅ **API Server:** http://localhost:8000  
📚 **Interactive Docs:** http://localhost:8000/docs  
📖 **ReDoc:** http://localhost:8000/redoc

**Stop the server:**

```bash
docker compose down
```

### Option 2: Local Python Installation 💻

Ideal for development, testing, or integration into existing Python projects.

**Installation:**

```bash
# Clone repository
git clone https://github.com/ZUENS2020/gcc-mem-system.git
cd gcc-mem-system

# Install in development mode
pip install -e .

# Or install from PyPI (when available)
# pip install gcc-context-controller
```

**Run the server:**

```bash
# Start FastAPI server
gcc-server

# Server starts on http://localhost:8000
```

**Run MCP proxy (for Claude Desktop):**

```bash
# Set server URL (if different from default)
export GCC_SERVER_URL=http://localhost:8000

# Start MCP proxy
gcc-mcp
```

### Option 3: Development Setup 🛠️

For contributors or those wanting to modify the code.

```bash
# Clone and install with dev dependencies
git clone https://github.com/ZUENS2020/gcc-mem-system.git
cd gcc-mem-system
pip install -e ".[dev]"

# Run tests
make test
# or
pytest tests/ -v

# Build Docker image
make build

# Start services
make up
```

### Quick Test

Once the server is running, try this simple workflow:

```bash
# 1. Initialize a session
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Test GCC system",
    "todo": ["Create branch", "Make commit"],
    "session_id": "test-session"
  }'

# 2. Create a branch
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "test-branch",
    "purpose": "Testing GCC functionality",
    "session_id": "test-session"
  }'

# 3. Make a commit
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "test-branch",
    "contribution": "First test commit",
    "log_entries": ["Initialized test", "Created branch"],
    "session_id": "test-session"
  }'

# 4. Get context
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "test-branch",
    "session_id": "test-session"
  }'
```

### Next Steps

- 📚 Read the [Usage Examples](#-usage-examples) to learn common workflows
- 🔌 Set up [MCP Integration](#-mcp-integration) for Claude Desktop
- 📖 Explore the [API Reference](#-api-reference) for all endpoints
- ⚙️ Configure [Environment Variables](#️-configuration) for your setup

---

## 💡 Usage Examples

### Real-World Scenario: Building a Web Application

This comprehensive example shows how an AI agent would use GCC to manage memory while building a REST API application.

#### Scenario Overview

You're building a REST API with authentication, database, and API endpoints. GCC helps you:
- Track overall project goal and todos
- Work on features in isolated branches
- Record detailed logs of all actions
- Store metadata about implementation details
- Merge completed features

### Example 1: Complete Project Workflow

**Step 1: Initialize the Project**

```bash
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API server with authentication and database",
    "todo": [
      "Design database schema",
      "Implement CRUD endpoints",
      "Add JWT authentication",
      "Write API documentation",
      "Add rate limiting"
    ],
    "session_id": "rest-api-project"
  }'
```

<details>
<summary>📄 Response</summary>

```json
{
  "gcc_root": "/data/rest-api-project/.GCC",
  "session": "rest-api-project",
  "main": "/data/rest-api-project/.GCC/sessions/rest-api-project/main.md"
}
```

This creates:
- Session directory structure
- `main.md` file with goals and todos
- Git repository for version control
</details>

**Step 2: Create Feature Branch for Authentication**

```bash
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-authentication",
    "purpose": "Implement JWT-based authentication system with login, logout, and token refresh",
    "session_id": "rest-api-project"
  }'
```

<details>
<summary>📄 Response</summary>

```json
{
  "session": "rest-api-project",
  "branch": "user-authentication",
  "branch_dir": "/data/rest-api-project/.GCC/sessions/rest-api-project/branches/user-authentication"
}
```

This creates:
- `branches/user-authentication/` directory
- `commit.md`, `log.md`, `metadata.yaml` files
- Git branch `user-authentication`
</details>

**Step 3: Make Progress - First Commit**

```bash
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-authentication",
    "contribution": "Implemented JWT token generation and validation utilities",
    "log_entries": [
      "Created jwt_utils.py with token generation function",
      "Added token expiration logic (1 hour default)",
      "Implemented refresh token mechanism",
      "Added unit tests for token validation",
      "Configured secret key from environment variable"
    ],
    "metadata_updates": {
      "status": "in_progress",
      "files_modified": ["src/auth/jwt_utils.py", "tests/test_jwt.py"],
      "dependencies_added": ["PyJWT", "python-jose"],
      "test_coverage": "85%",
      "lines_of_code": 250
    },
    "session_id": "rest-api-project"
  }'
```

<details>
<summary>📄 Response</summary>

```json
{
  "session": "rest-api-project",
  "branch": "user-authentication",
  "commit_id": "a1b2c3d",
  "message": "Memory commit on user-authentication"
}
```

This:
- Appends to `commit.md` with structured commit entry
- Adds log entries to `log.md`
- Updates `metadata.yaml` with new data
- Creates git commit with all changes
</details>

**Step 4: Continue Working - Second Commit**

```bash
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-authentication",
    "contribution": "Completed login and logout API endpoints",
    "log_entries": [
      "Created /api/auth/login endpoint with password hashing",
      "Implemented /api/auth/logout with token blacklisting",
      "Added rate limiting (5 attempts per minute)",
      "Created authentication middleware",
      "Updated API documentation with auth examples"
    ],
    "metadata_updates": {
      "status": "testing",
      "test_coverage": "92%",
      "api_endpoints": ["/api/auth/login", "/api/auth/logout", "/api/auth/refresh"],
      "security_features": ["bcrypt_hashing", "rate_limiting", "token_blacklist"]
    },
    "update_main": "✅ Completed: JWT authentication system\n- Login/logout working\n- Token refresh implemented\n- Rate limiting active",
    "session_id": "rest-api-project"
  }'
```

<details>
<summary>📄 What happens</summary>

1. New commit appended to `commit.md`
2. Five log entries added to `log.md`
3. Metadata updated with testing status and new endpoints
4. `main.md` updated with progress note
5. Git commit created
</details>

**Step 5: Retrieve Context**

```bash
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "user-authentication",
    "log_tail": 10,
    "session_id": "rest-api-project"
  }'
```

<details>
<summary>📄 Response (Full Context)</summary>

```json
{
  "session": "rest-api-project",
  "goal": "Build a REST API server with authentication and database",
  "todo": [
    "Design database schema",
    "Implement CRUD endpoints",
    "Add JWT authentication",
    "Write API documentation",
    "Add rate limiting"
  ],
  "branches": ["user-authentication"],
  "branch": {
    "name": "user-authentication",
    "purpose": "Implement JWT-based authentication system with login, logout, and token refresh",
    "latest_commit": "e4f5g6h",
    "commit_count": 2,
    "commits": [
      {
        "id": "a1b2c3d",
        "contribution": "Implemented JWT token generation and validation utilities",
        "timestamp": "2026-02-12T10:30:00Z"
      },
      {
        "id": "e4f5g6h",
        "contribution": "Completed login and logout API endpoints",
        "timestamp": "2026-02-12T11:45:00Z"
      }
    ],
    "recent_logs": [
      "Created jwt_utils.py with token generation function",
      "Added token expiration logic (1 hour default)",
      "Implemented refresh token mechanism",
      "Added unit tests for token validation",
      "Configured secret key from environment variable",
      "Created /api/auth/login endpoint with password hashing",
      "Implemented /api/auth/logout with token blacklisting",
      "Added rate limiting (5 attempts per minute)",
      "Created authentication middleware",
      "Updated API documentation with auth examples"
    ],
    "metadata": {
      "status": "testing",
      "test_coverage": "92%",
      "files_modified": ["src/auth/jwt_utils.py", "tests/test_jwt.py"],
      "dependencies_added": ["PyJWT", "python-jose"],
      "api_endpoints": ["/api/auth/login", "/api/auth/logout", "/api/auth/refresh"],
      "security_features": ["bcrypt_hashing", "rate_limiting", "token_blacklist"]
    }
  }
}
```
</details>

**Step 6: Merge to Main**

```bash
curl -X POST http://localhost:8000/merge \
  -H "Content-Type: application/json" \
  -d '{
    "source_branch": "user-authentication",
    "target_branch": "main",
    "summary": "Authentication system complete: JWT tokens, login/logout, rate limiting, 92% test coverage",
    "session_id": "rest-api-project"
  }'
```

### Example 2: Working with Multiple Branches

Simulate working on multiple features simultaneously:

```bash
# Create database schema branch
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "database-schema",
    "purpose": "Design and implement PostgreSQL database schema",
    "session_id": "rest-api-project"
  }'

# Create API endpoints branch
curl -X POST http://localhost:8000/branch \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "api-endpoints",
    "purpose": "Implement REST API CRUD endpoints",
    "session_id": "rest-api-project"
  }'

# Work on database branch
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "database-schema",
    "contribution": "Created users and sessions tables with proper indexes",
    "session_id": "rest-api-project"
  }'

# Switch to API branch and work there
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "api-endpoints",
    "contribution": "Implemented GET and POST endpoints for users resource",
    "session_id": "rest-api-project"
  }'

# Get overview of all branches
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "rest-api-project"
  }'
```

### Example 3: Version Control Features

**View commit history:**

```bash
curl http://localhost:8000/history?session_id=rest-api-project&limit=20
```

**Compare versions (diff):**

```bash
curl -X POST http://localhost:8000/diff \
  -H "Content-Type: application/json" \
  -d '{
    "from_ref": "HEAD~5",
    "to_ref": "HEAD",
    "session_id": "rest-api-project"
  }'
```

**View specific version:**

```bash
curl -X POST http://localhost:8000/show \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "a1b2c3d",
    "path": "sessions/rest-api-project/branches/user-authentication/commit.md",
    "session_id": "rest-api-project"
  }'
```

**Rollback to previous state:**

```bash
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "HEAD~3",
    "mode": "soft",
    "session_id": "rest-api-project"
  }'
```

### Example 4: Advanced Metadata Usage

Store complex structured data:

```bash
curl -X POST http://localhost:8000/commit \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "api-endpoints",
    "contribution": "Completed full CRUD operations with validation",
    "metadata_updates": {
      "api_version": "v1",
      "endpoints": {
        "users": {
          "GET": "/api/v1/users",
          "POST": "/api/v1/users",
          "GET_by_id": "/api/v1/users/{id}",
          "PUT": "/api/v1/users/{id}",
          "DELETE": "/api/v1/users/{id}"
        }
      },
      "validation": {
        "email": "regex + DNS check",
        "password": "min 8 chars, complexity rules"
      },
      "performance": {
        "avg_response_time": "45ms",
        "queries_optimized": true,
        "caching": "Redis"
      },
      "deployment": {
        "environment": "staging",
        "last_deployed": "2026-02-12T12:00:00Z",
        "health_check_url": "/health"
      }
    },
    "session_id": "rest-api-project"
  }'
```

### Example 5: Logging Best Practices

Detailed logging for complex operations:

```bash
curl -X POST http://localhost:8000/log \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "database-schema",
    "entries": [
      "=== Database Migration Started ===",
      "Step 1: Backing up existing data",
      "  - Created backup at /backups/db_2026-02-12.sql",
      "  - Verified backup integrity",
      "Step 2: Creating new tables",
      "  - Created users table with UUID primary key",
      "  - Added email unique constraint",
      "  - Created indexes on email and created_at",
      "Step 3: Data migration",
      "  - Migrated 10,000 user records",
      "  - Validated data integrity (100% success)",
      "Step 4: Updating foreign keys",
      "  - Updated sessions table references",
      "=== Migration Completed Successfully ===="
    ],
    "session_id": "rest-api-project"
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

### Common Issues & Solutions

**🔒 Lock Timeout Errors**

*Problem:* Operations timeout waiting for locks

*Root Cause:* Another process is holding the lock, or a previous operation crashed without releasing the lock

*Solution:*
```bash
# 1. Check for stale locks
ls /data/<session_id>/.GCC/.lock.*

# 2. Verify no other process is using the session
ps aux | grep gcc

# 3. If safe to proceed, remove stale locks
rm /data/<session_id>/.GCC/.lock.*

# 4. Restart the operation
```

**⚠️ Encoding Errors**

*Problem:* Non-English characters cause errors or garbled text

*Root Cause:* File encoding issues with non-ASCII characters

*Solution:* Use English only for all text values
```bash
# ❌ Incorrect (may cause encoding issues)
{"contribution": "实现用户认证"}

# ✅ Correct (always works)
{"contribution": "Implemented user authentication"}
```

**🐳 Docker Container Issues**

*Problem:* Container exits immediately after start

*Solution:*
```bash
# 1. Check container logs
docker logs gcc-mcp

# 2. Check if port 8000 is already in use
lsof -i :8000
# or
netstat -tulpn | grep 8000

# 3. If port is in use, stop the conflicting process or change the port
docker compose up -d -p 8001:8000
```

**🔄 Git Merge Conflicts**

*Problem:* Merge operation fails with conflicts

*Solution:*
```bash
# 1. Check the current branch state
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session"}'

# 2. Use git directly to resolve (advanced)
cd /data/<session_id>/.GCC
git status
git merge --abort  # Cancel the merge

# 3. Manually merge content or retry with different branch
```

**📊 Large File Performance**

*Problem:* Slow operations with large metadata or logs

*Solution:*
```bash
# Keep metadata focused and structured
# Use log rotation for very long-running projects

# Good practice: Periodic cleanup
curl -X POST http://localhost:8000/log \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "main",
    "entries": ["=== Archive: Previous logs moved to archive branch ==="],
    "session_id": "your-session"
  }'
```

**🔐 Permission Denied Errors**

*Problem:* Cannot write to /data directory

*Solution:*
```bash
# For Docker
docker compose down
sudo chown -R $(id -u):$(id -g) ./gcc_data
docker compose up -d

# For local installation
mkdir -p /tmp/gcc-data
export GCC_DATA_ROOT=/tmp/gcc-data
gcc-server
```

**❓ Need More Help?**

- 📖 **API Documentation**: http://localhost:8000/docs (interactive)
- 🐛 **Report Bugs**: [GitHub Issues](https://github.com/ZUENS2020/gcc-mem-system/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/ZUENS2020/gcc-mem-system/discussions)
- 📧 **Email Support**: Check repository for maintainer contact

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **🐛 Report Bugs** - Found an issue? Open a GitHub issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, Docker version)

2. **💡 Suggest Features** - Have an idea? Open a discussion or issue describing:
   - The problem it solves
   - Proposed solution
   - Alternative approaches considered

3. **📝 Improve Documentation** - Help others by:
   - Fixing typos or unclear sections
   - Adding examples
   - Translating documentation
   - Creating tutorials or blog posts

4. **🔧 Submit Code** - Contribute features or fixes:
   - Fork the repository
   - Create a feature branch
   - Make your changes with tests
   - Submit a pull request

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR-USERNAME/gcc-mem-system.git
cd gcc-mem-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/gcc --cov-report=html
```

### Code Guidelines

- **Style**: Follow PEP 8 for Python code
- **Type Hints**: Use type annotations for all functions
- **Docstrings**: Document all public APIs with Google-style docstrings
- **Tests**: Add tests for new features and bug fixes
- **Commits**: Use clear, descriptive commit messages

### Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass (`make test`)
4. Update CHANGELOG.md with your changes
5. Submit PR with clear description
6. Respond to review feedback

### Testing Guidelines

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=src/gcc --cov-report=term-missing

# Test security features
pytest tests/security -v
```

---

## 🎯 Best Practices

### For AI Agents

1. **Initialize Once**: Create a session at the start of a project
2. **Branch Per Feature**: Use separate branches for different tasks
3. **Commit Often**: Make frequent, small commits with clear contributions
4. **Detailed Logs**: Include step-by-step actions in log_entries
5. **Rich Metadata**: Store structured data for easy retrieval

### For Developers Integrating GCC

1. **Session Management**: Use meaningful session IDs
2. **Error Handling**: Always check response status codes
3. **Concurrency**: GCC handles locking, but avoid excessive parallel requests to same session
4. **Cleanup**: Archive or delete old sessions periodically
5. **Monitoring**: Use health checks and logging for production deployments

### Security Considerations

1. **Access Control**: Secure the HTTP API with authentication if exposing publicly
2. **Input Validation**: GCC validates input, but sanitize data in your application
3. **Data Privacy**: Session data is not encrypted at rest - use appropriate file system permissions
4. **Audit Logs**: Enable audit logging for production systems
5. **Rate Limiting**: Implement rate limiting if exposing to untrusted clients

### Performance Tips

1. **Branch Count**: Keep branch count reasonable (< 100 per session)
2. **Commit Size**: Avoid extremely large metadata objects
3. **Log Rotation**: Archive old logs for long-running projects
4. **Docker Volumes**: Use Docker volumes for better I/O performance
5. **Context Queries**: Use `log_tail` parameter to limit log retrieval

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**Copyright (c) 2026 ZUENS2020**

---

<div align="center">

**Made with ❤️ for AI Agents**

[⬆ Back to Top](#-overview)

</div>
