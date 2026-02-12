# GCC (Git-Context-Controller)

**Zero Path Knowledge • Complete Memory Management • MCP Integration • Docker Ready**

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

GCC is a unified memory and context management system for AI agents. It leverages Git as a version-controlled backend to provide a persistent, structured, and auditable history of an agent's activities. GCC exposes its functionality through both a FastAPI-based HTTP server and an MCP (Model Context Protocol) proxy, making it easy for AI models to maintain context across different sessions and branches of exploration.

### Key Features

- **Zero Path Knowledge Required**: AI agents only need to provide a `session_id`. The server automatically manages all file system paths using the structure `/data/sessions/{session_id}/`. No path configuration or file system knowledge required.
- **Git-Backed Memory**: Every change to an agent's context is automatically committed to a local Git repository, ensuring a full audit trail and easy state recovery.
- **Hierarchical Context Management**: Organize work into isolated **Sessions** and **Branches**.
- **Structured Memory Components**:
  - **Roadmap (`main.md`)**: High-level goals and task lists.
  - **Checkpoint Commits (`commit.md`)**: Structured contribution summaries.
  - **Operational Logs (`log.md`)**: Fine-grained, timestamped activity records.
  - **Metadata (`metadata.yaml`)**: Structured state storage for environment and file info.
- **Dual Interface**:
  - **HTTP API**: RESTful endpoints for integration with any system.
  - **MCP Integration**: Seamlessly use GCC as a toolset within MCP-compatible LLM clients (like Claude).
- **Security-First Design**: Includes robust input validation to prevent path traversal and injection attacks.

### Architecture & Concepts

#### Automatic Path Management

GCC completely abstracts file system paths from AI agents. Simply provide a `session_id` and the server handles everything:

```
/data/sessions/{session_id}/.GCC/
├── main.md              # Session goals and roadmap
├── branches/            # Branch-specific memory
│   └── {branch_name}/
│       ├── commit.md     # Contribution checkpoints
│       ├── log.md       # Detailed logs
│       └── metadata.yaml # Structured metadata
└── .git/               # Version control
```

**No path parameters needed** - The server:
- Auto-generates unique session IDs if not provided
- Creates and manages all directories automatically
- Validates paths to prevent security issues
- Handles all Git operations transparently

#### Sessions
A session is an isolated workspace. All data for a session is stored in its own directory with a dedicated Git repository. Path: `/data/sessions/{session_id}/`.

#### Branches
Within a session, you can create multiple branches to explore different approaches. Each branch has its own set of memory files.

#### Memory Files
- **`main.md`**: Global state for the session (Roadmap, Goals, Todo).
- **`commit.md`**: Sequence of contribution checkpoints.
- **`log.md`**: Detailed execution logs.
- **`metadata.yaml`**: Key-value store for structured metadata.

### Installation & Setup

#### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git

#### Quick Start with Docker
```bash
make build
make up
```

The server starts with automatic path management. AI clients only need to provide `session_id`.

#### Local Installation
```bash
pip install -e .
gcc-server  # Start API server
# OR
gcc-mcp     # Start MCP proxy (via stdin/stdout)
```

### Configuration

GCC can be configured through environment variables. Most have sensible defaults and should not need adjustment for typical use.

#### Server Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GCC_DATA_ROOT` | Data root directory for sessions | `/data` |
| `GCC_HOST` | Server bind address | `0.0.0.0` |
| `GCC_PORT` | Server port | `8000` |
| `GCC_WORKERS` | Number of worker processes | Auto-detected |
| `GCC_RELOAD` | Enable auto-reload on code changes | `false` |
| `GCC_ACCESS_LOG` | Enable HTTP access logging | `true` |

#### Git Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GCC_GIT_NAME` | Git user name for commits | `GCC Agent` |
| `GCC_GIT_EMAIL` | Git email for commits | `gcc@example.com` |
| `GCC_GIT_DEFAULT_BRANCH` | Default branch name | `main` |

#### Validation & Limits

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GCC_MAX_BRANCH_LENGTH` | Maximum branch name length | `100` |
| `GCC_MAX_SESSION_LENGTH` | Maximum session ID length | `100` |
| `GCC_MAX_LIMIT` | Maximum history limit | `1000` |
| `GCC_MIN_LIMIT` | Minimum history limit | `1` |
| `GCC_MAX_STRING_LENGTH` | Maximum string field length | `10000` |
| `GCC_ALLOW_PATH_TRAVERSAL` | Allow path traversal (security risk!) | `false` |
| `GCC_ENABLE_RATE_LIMIT` | Enable rate limiting | `true` |
| `GCC_RATE_LIMIT_REQUESTS` | Rate limit requests per minute | `60` |

#### Logging Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GCC_LOG_LEVEL` | Log level (`debug`, `info`, `warning`, `error`) | `info` |
| `GCC_LOG_DIR` | Directory for log files | `/var/log/gcc` |
| `GCC_LOG_MAX_BYTES` | Max size per log file before rotation | `10485760` (10MB) |
| `GCC_LOG_BACKUP_COUNT` | Number of backup logs to keep | `5` |
| `GCC_ENABLE_AUDIT_LOG` | Enable audit logging for all operations | `true` |
| `GCC_ENABLE_GIT_LOG` | Enable Git operation logging | `true` |

#### MCP Client Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GCC_SERVER_URL` | HTTP API server URL for MCP proxy | `http://localhost:8000` |
| `GCC_SESSION_ID` | Default session ID for MCP requests | Auto-generated |

**Example - Docker Compose with custom configuration:**
```yaml
services:
  gcc-server:
    image: gcc-mem-system
    environment:
      - GCC_DATA_ROOT=/data
      - GCC_PORT=8000
      -GCC_LOG_LEVEL=debug
      - GCC_GIT_NAME=My AI Agent
      - GCC_GIT_EMAIL=agent@example.com
    volumes:
      - ./data:/data
```

### API Reference

| Endpoint | Method | Description | Key Parameters |
| :--- | :--- | :--- | :--- |
| `/init` | `POST` | Initialize a session | `goal`, `todo`, `session_id` (auto-generated if omitted) |
| `/branch` | `POST` | Create a branch | `branch`, `purpose`, `session_id` |
| `/commit` | `POST` | Record a checkpoint | `branch`, `contribution`, `log_entries`, `metadata_updates`, `update_main` |
| `/context` | `POST` | Get current memory | `branch`, `commit_id`, `log_tail`, `metadata_segment` |
| `/history` | `POST` | View git history | `limit`, `session_id` |

**Example - Initialize Session (Zero Configuration):**
```bash
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a web scraper",
    "todo": ["Research libraries", "Implement scraping"]
  }'
```
**Note**: No `session_id` or paths required - everything is auto-managed.

**Example - Record Memory Checkpoint:**
```json
{
  "branch": "feature-x",
  "contribution": "Implemented user authentication logic",
  "log_entries": ["Modified auth.py", "Added tests for JWT"],
  "metadata_updates": {"status": "in-progress", "coverage": 85}
}
```
**Note**: Server automatically resolves paths using configured `session_id`.

### MCP Integration

Configure GCC as an MCP server in your Claude Desktop config:

```json
{
  "mcpServers": {
    "gcc": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8000",
        "GCC_SESSION_ID": "my-session"
      }
    }
  }
}
```

AI agents can now use GCC tools without any path knowledge:
```
- gcc_init: Initialize session (goal, todo, optional session_id)
- gcc_branch: Create exploration branch (branch, purpose)
- gcc_commit: Record checkpoint (branch, contribution, log_entries)
- gcc_context: Retrieve memory (branch, commit_id, log_tail)
- gcc_history: View commit history (limit)
```

---

<a name="chinese"></a>
## 中文

GCC (Git-Context-Controller) 是一个为 AI 智能体设计的统一内存与上下文管理系统。它利用 Git 作为版本控制后端，为智能体的活动提供持久化、结构化且可审计的历史记录。GCC 通过基于 FastAPI 的 HTTP 服务器和 MCP (Model Context Protocol) 代理暴露其功能，使 AI 模型能够跨不同的会话和探索分支轻松维护上下文。

### 核心特性

- **零路径知识要求**: AI 智能体只需提供 `session_id`。服务器自动使用 `/data/sessions/{session_id}/` 结构管理所有文件系统路径。无需路径配置或文件系统知识。
- **Git 驱动的内存**: 智能体上下文的每次更改都会自动提交到本地 Git 仓库，确保完整的审计追踪和轻松的状态恢复。
- **分层上下文管理**: 将工作组织到隔离的 **会话 (Sessions)** 和 **分支 (Branches)** 中。
- **结构化内存组件**:
  - **路线图 (`main.md`)**: 高级目标和任务列表。
  - **检查点提交 (`commit.md`)**: 结构化的贡献摘要。
  - **操作日志 (`log.md`)**: 细粒度的、带时间戳的活动记录。
  - **元数据 (`metadata.yaml`)**: 用于环境和文件信息的结构化状态存储。
- **双重接口**:
  - **HTTP API**: 用于与任何系统集成的 RESTful 端点。
  - **MCP 集成**: 在 MCP 兼容的 LLM 客户端（如 Claude）中无缝使用 GCC 作为工具集。
- **安全优先设计**: 包含鲁棒的输入验证，防止路径遍历和注入攻击。

### 架构与概念

#### 自动路径管理

GCC 完全从 AI 智能体抽象文件系统路径。只需提供 `session_id`，服务器处理一切：

```
/data/sessions/{session_id}/.GCC/
├── main.md              # 会话目标和路线图
├── branches/            # 分支特定内存
│   └── {branch_name}/
│       ├── commit.md     # 贡献检查点
│       ├── log.md       # 详细日志
│       └── metadata.yaml # 结构化元数据
└── .git/               # 版本控制
```

**无需路径参数** - 服务器自动：
- 如果未提供，自动生成唯一会话 ID
- 自动创建和管理所有目录
- 验证路径以防止安全问题
- 透明地处理所有 Git 操作

#### 会话 (Sessions)
会话是一个隔离的工作区。会话的所有数据都存储在拥有独立 Git 仓库的目录中。路径：`/data/sessions/{session_id}/`。

#### 分支 (Branches)
在一个会话内，您可以创建多个分支来探索不同的方法。每个分支都有自己的一套内存文件。

#### 内存文件
- **`main.md`**: 会话的全局状态（路线图、目标、待办事项）。
- **`commit.md`**: 贡献检查点的序列。
- **`log.md`**: 详细的执行日志。
- **`metadata.yaml`**: 结构化元数据的键值存储。

### 安装与设置

#### 准备条件
- Python 3.9+
- Docker & Docker Compose
- Git

#### 使用 Docker 快速启动
```bash
make build
make up
```

服务器以自动路径管理启动。AI 客户端只需提供 `session_id`。

#### 本地安装
```bash
pip install -e .
gcc-server  # 启动 API 服务器
# 或者
gcc-mcp     # 启动 MCP 代理（通过 stdin/stdout）
```

### 配置选项

GCC 可以通过环境变量进行配置。大多数变量都有合理的默认值，通常情况下不需要调整。

#### 服务器配置

| 变量 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `GCC_DATA_ROOT` | 会话数据根目录 | `/data` |
| `GCC_HOST` | 服务器绑定地址 | `0.0.0.0` |
| `GCC_PORT` | 服务器端口 | `8000` |
| `GCC_WORKERS` | 工作进程数 | 自动检测 |
| `GCC_RELOAD` | 代码更改时自动重载 | `false` |
| `GCC_ACCESS_LOG` | 启用 HTTP 访问日志 | `true` |

#### Git 配置

| 变量 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `GCC_GIT_NAME` | Git 提交用户名 | `GCC Agent` |
| `GCC_GIT_EMAIL` | Git 提交邮箱 | `gcc@example.com` |
| `GCC_GIT_DEFAULT_BRANCH` | 默认分支名称 | `main` |

#### 验证与限制

| 变量 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `GCC_MAX_BRANCH_LENGTH` | 最大分支名称长度 | `100` |
| `GCC_MAX_SESSION_LENGTH` | 最大会话 ID 长度 | `100` |
| `GCC_MAX_LIMIT` | 最大历史记录条数 | `1000` |
| `GCC_MIN_LIMIT` | 最小历史记录条数 | `1` |
| `GCC_MAX_STRING_LENGTH` | 最大字符串字段长度 | `10000` |
| `GCC_ALLOW_PATH_TRAVERSAL` | 允许路径遍历（安全风险！） | `false` |
| `GCC_ENABLE_RATE_LIMIT` | 启用速率限制 | `true` |
| `GCC_RATE_LIMIT_REQUESTS` | 每分钟速率限制请求数 | `60` |

#### 日志配置

| 变量 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `GCC_LOG_LEVEL` | 日志级别（`debug`, `info`, `warning`, `error`） | `info` |
| `GCC_LOG_DIR` | 日志文件目录 | `/var/log/gcc` |
| `GCC_LOG_MAX_BYTES` | 日志文件轮转前的最大大小 | `10485760` (10MB) |
| `GCC_LOG_BACKUP_COUNT` | 保留的备份日志数量 | `5` |
| `GCC_ENABLE_AUDIT_LOG` | 启用所有操作的审计日志 | `true` |
| `GCC_ENABLE_GIT_LOG` | 启用 Git 操作日志 | `true` |

#### MCP 客户端配置

| 变量 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `GCC_SERVER_URL` | MCP 代理的 HTTP API 服务器 URL | `http://localhost:8000` |
| `GCC_SESSION_ID` | MCP 请求的默认会话 ID | 自动生成 |

**示例 - Docker Compose 自定义配置：**
```yaml
services:
  gcc-server:
    image: gcc-mem-system
    environment:
      - GCC_DATA_ROOT=/data
      - GCC_PORT=8000
      - GCC_LOG_LEVEL=debug
      - GCC_GIT_NAME=My AI Agent
      - GCC_GIT_EMAIL=agent@example.com
    volumes:
      - ./data:/data
```

### API 参考

| 端点 | 方法 | 描述 | 关键参数 |
| :--- | :--- | :--- | :--- |
| `/init` | `POST` | 初始化会话 | `goal`, `todo`, `session_id`（如省略则自动生成） |
| `/branch` | `POST` | 创建分支 | `branch`, `purpose`, `session_id` |
| `/commit` | `POST` | 记录检查点 | `branch`, `contribution`, `log_entries`, `metadata_updates`, `update_main` |
| `/context` | `POST` | 获取当前内存 | `branch`, `commit_id`, `log_tail`, `metadata_segment` |
| `/history` | `POST` | 查看 Git 历史 | `limit`, `session_id` |

**示例 - 初始化会话（零配置）：**
```bash
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a web scraper",
    "todo": ["Research libraries", "Implement scraping"]
  }'
```
**注意**: 无需 `session_id` 或路径 - 一切都是自动管理的。

**示例 - 记录内存检查点：**
```json
{
  "branch": "feature-x",
  "contribution": "Implemented user authentication logic",
  "log_entries": ["Modified auth.py", "Added tests for JWT"],
  "metadata_updates": {"status": "in-progress", "coverage": 85}
}
```
**注意**: 服务器使用配置的 `session_id` 自动解析路径。

### MCP 集成

在 Claude Desktop 配置中将 GCC 配置为 MCP 服务器：

```json
{
  "mcpServers": {
    "gcc": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8000",
        "GCC_SESSION_ID": "my-session"
      }
    }
  }
}
```

AI 智能体现在可以使用 GCC 工具而无需任何路径知识：
```
- gcc_init: 初始化会话（goal, todo, 可选 session_id）
- gcc_branch: 创建探索分支（branch, purpose）
- gcc_commit: 记录检查点（branch, contribution, log_entries）
- gcc_context: 检索内存（branch, commit_id, log_tail）
- gcc_history: 查看提交历史（limit）
```
