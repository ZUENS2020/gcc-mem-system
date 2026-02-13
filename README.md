# GCC (Git-Context-Controller)

**AI Memory Management • Git-Backed Context • MCP Integration • Docker Ready**

This project is inspired by ***Git Context Controller: Manage the Context of LLM-based Agents like Git***.

If you find this work helpful, please cite the original GCC paper:

```bibtex
@article{wu2025gcc,
  title={Git Context Controller: Manage the Context of LLM-based Agents like Git},
  author={Wu, Junde},
  journal={arXiv preprint arXiv:2508.00031},
  year={2025}
}
```

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

GCC is a unified memory and context management system for AI agents. It leverages Git as a version-controlled backend to provide a persistent, structured, and auditable history of an agent's activities. GCC exposes its functionality through both a FastAPI-based HTTP server and an MCP (Model Context Protocol) proxy, making it easy for AI models to maintain context across different sessions and branches of exploration.

### Key Features

- **Git-Backed Memory**: Every change to an agent's context is automatically committed to a local Git repository, ensuring a full audit trail and easy state recovery.
- **Session-Based Isolation**: Each session has its own workspace with unique `session_id`. Simply provide the session identifier and the server handles the storage structure automatically.
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

#### Directory Structure

Each session stores its data under the shared data root:

```
/data/.GCC/
├── sessions/
│   └── {session_id}/
│       ├── main.md        # Session goals and roadmap
│       └── branches/      # Branch-specific memory
│           └── {branch_name}/
│               ├── commit.md
│               ├── log.md
│               └── metadata.yaml
└── .git/                 # Version control for GCC memory state
```

Breaking change: legacy duplicated path layouts are no longer used. You should clear old data before upgrading.

#### Sessions
A session is an isolated workspace. All data for a session is stored in its own directory with a dedicated Git repository. Use `session_id` to identify which workspace to operate on.

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
export GCC_DATA_ROOT=/data   # Optional override (default: /data)
gcc-server  # Start API server
# OR
gcc-mcp     # Start MCP proxy (via stdin/stdout)
```

### Configuration

GCC can be configured through environment variables. Most have sensible defaults and should not need adjustment for typical use.

`GCC_DATA_ROOT` is optional for server-side path resolution. If omitted, GCC uses the default path `/data`.

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
| `GCC_SESSION_ID` | Fixed session ID for MCP requests (highest priority) | unset |
| `GCC_SESSION_MODE` | Default session strategy: `auto`, `shared`, `isolated` | `auto` |
| `GCC_SESSION_LOCK_MODE` | Session lock policy: `env`, `strict`, `none` | `env` |
| `GCC_SESSION_NAMESPACE` | Optional prefix for generated session IDs | unset |
| `GCC_SESSION_ID_FILE` | Optional file path to load a default session ID | unset |

**Example - Docker Compose with custom configuration:**
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

#### Session Strategy and Locking

GCC MCP resolves `session_id` with this priority:
1. Tool argument `session_id` (if lock policy allows)
2. `GCC_SESSION_ID` environment variable
3. `GCC_SESSION_ID_FILE` value (if configured and valid)
4. Generated default from `GCC_SESSION_MODE`

`GCC_SESSION_MODE` behavior:
- `auto` (default):
  - Docker: shared per container (`container-<host>`)
  - Non-Docker: shared per workspace (`ws-<hash>`)
- `shared`: deterministic shared default (`container-<host>` or `ws-<hash>`)
- `isolated`: per-process default (`container-<host>-p<pid>` or `mcp-<pid>`)

`GCC_SESSION_LOCK_MODE` behavior:
- `env` (default): lock only when `GCC_SESSION_ID` is explicitly set
- `strict`: lock in both env-fixed mode and Docker mode (legacy behavior)
- `none`: never lock, always allow tool-provided `session_id`

**Examples:**

| Scenario | Config | Behavior |
|:---|:---|:---|
| Fixed shared memory | `GCC_SESSION_ID=team-main` | All tools use `team-main` |
| Docker shared memory (same container) | `GCC_SESSION_MODE=auto` | Uses `container-<host>` |
| Docker concurrent isolated memory | `GCC_SESSION_MODE=isolated` | Each MCP process gets `container-<host>-p<pid>` |
| Docker forced lock (legacy) | `GCC_SESSION_LOCK_MODE=strict` | Ignores tool `session_id` in Docker |
| Workspace shared memory | `GCC_SESSION_MODE=shared` | Uses `ws-<hash>` for same workspace |
| Default from file | `GCC_SESSION_ID_FILE=.claude/session.id` | Uses file value when present |

### API Reference

Request validation is strict (`extra=forbid` on request models). Unknown fields are rejected with HTTP 422.

| Endpoint | Method | Description | Key Parameters |
| :--- | :--- | :--- | :--- |
| `/init` | `POST` | Initialize a session | `goal`, `todo`, `session_id` (auto-generated if omitted) |
| `/branch` | `POST` | Create a branch | `branch`, `purpose`, `session_id` |
| `/commit` | `POST` | Record a checkpoint | `branch`, `contribution`, `log_entries`, `metadata_updates`, `update_main` |
| `/context` | `POST` | Get current memory | `branch`, `commit_id`, `log_tail`, `metadata_segment` |
| `/history` | `POST` | View git history | `limit`, `session_id` |

**Example - Initialize Session:**
```bash
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a web scraper",
    "todo": ["Research libraries", "Implement scraping"]
  }'
```
**Note**: `session_id` is optional and will be auto-generated if not provided.

**Migration note (strict schema):**
```json
// Old (rejected now: unknown field "root")
{"root": "/tmp/work", "goal": "Build a web scraper"}

// New
{"goal": "Build a web scraper", "session_id": "my-session"}
```

**Example - Record Memory Checkpoint:**
```json
{
  "branch": "feature-x",
  "contribution": "Implemented user authentication logic",
  "log_entries": ["Modified auth.py", "Added tests for JWT"],
  "metadata_updates": {"status": "in-progress", "coverage": 85}
}
```
**Note**: Server uses the configured `session_id` to locate the correct workspace.

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

AI agents can use GCC tools directly:
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

- **Git 驱动的内存**: 智能体上下文的每次更改都会自动提交到本地 Git 仓库，确保完整的审计追踪和轻松的状态恢复。
- **基于会话的隔离**: 每个会话都有独立的工作空间和唯一的 `session_id`。只需提供会话标识符，服务器会自动处理存储结构。
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

#### 目录结构

每个会话都存储在共享数据根目录下：

```
/data/.GCC/
├── sessions/
│   └── {session_id}/
│       ├── main.md        # 会话目标和路线图
│       └── branches/      # 分支特定内存
│           └── {branch_name}/
│               ├── commit.md
│               ├── log.md
│               └── metadata.yaml
└── .git/                 # GCC 内存状态的版本控制
```

不兼容变更：已移除旧的重复路径布局。升级前请清理旧数据。

#### 会话 (Sessions)
会话是一个隔离的工作区。会话的所有数据都存储在拥有独立 Git 仓库的目录中。使用 `session_id` 来标识要操作的工作空间。

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
export GCC_DATA_ROOT=/data   # 可选覆盖（默认值：/data）
gcc-server  # 启动 API 服务器
# 或者
gcc-mcp     # 启动 MCP 代理（通过 stdin/stdout）
```

### 配置选项

GCC 可以通过环境变量进行配置。大多数变量都有合理的默认值，通常情况下不需要调整。

`GCC_DATA_ROOT` 对服务端路径解析是可选项。未设置时，GCC 默认使用 `/data`。

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
| `GCC_SESSION_ID` | MCP 请求的固定会话 ID（最高优先级） | 未设置 |
| `GCC_SESSION_MODE` | 默认会话策略：`auto`、`shared`、`isolated` | `auto` |
| `GCC_SESSION_LOCK_MODE` | 会话锁定策略：`env`、`strict`、`none` | `env` |
| `GCC_SESSION_NAMESPACE` | 生成会话 ID 的可选前缀 | 未设置 |
| `GCC_SESSION_ID_FILE` | 加载默认会话 ID 的可选文件路径 | 未设置 |

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

#### Session 策略与锁定机制

GCC MCP 按以下优先级解析 `session_id`：
1. 工具调用参数中的 `session_id`（前提是锁定策略允许）
2. 环境变量 `GCC_SESSION_ID`
3. `GCC_SESSION_ID_FILE` 文件中的值（已配置且合法时）
4. 基于 `GCC_SESSION_MODE` 生成的默认值

`GCC_SESSION_MODE` 行为：
- `auto`（默认）：
  - Docker：容器内共享（`container-<host>`）
  - 非 Docker：按工作区共享（`ws-<hash>`）
- `shared`：确定性的共享默认值（`container-<host>` 或 `ws-<hash>`）
- `isolated`：按进程默认值（`container-<host>-p<pid>` 或 `mcp-<pid>`）

`GCC_SESSION_LOCK_MODE` 行为：
- `env`（默认）：仅当显式设置 `GCC_SESSION_ID` 时锁定
- `strict`：在固定环境变量和 Docker 场景都锁定（兼容旧行为）
- `none`：从不锁定，总是允许工具调用传入 `session_id`

**示例：**

| 场景 | 配置 | 行为 |
|:---|:---|:---|
| 固定共享记忆 | `GCC_SESSION_ID=team-main` | 所有工具都使用 `team-main` |
| Docker 容器内共享记忆 | `GCC_SESSION_MODE=auto` | 使用 `container-<host>` |
| Docker 并发隔离记忆 | `GCC_SESSION_MODE=isolated` | 每个 MCP 进程使用 `container-<host>-p<pid>` |
| Docker 强制锁定（旧行为） | `GCC_SESSION_LOCK_MODE=strict` | 在 Docker 中忽略工具传入的 `session_id` |
| 工作区共享记忆 | `GCC_SESSION_MODE=shared` | 同一工作区使用 `ws-<hash>` |
| 从文件读取默认会话 | `GCC_SESSION_ID_FILE=.claude/session.id` | 文件存在时优先使用其值 |

### API 参考

请求体采用严格校验（`extra=forbid`）。未知字段会被拒绝并返回 HTTP 422。

| 端点 | 方法 | 描述 | 关键参数 |
| :--- | :--- | :--- | :--- |
| `/init` | `POST` | 初始化会话 | `goal`, `todo`, `session_id`（如省略则自动生成） |
| `/branch` | `POST` | 创建分支 | `branch`, `purpose`, `session_id` |
| `/commit` | `POST` | 记录检查点 | `branch`, `contribution`, `log_entries`, `metadata_updates`, `update_main` |
| `/context` | `POST` | 获取当前内存 | `branch`, `commit_id`, `log_tail`, `metadata_segment` |
| `/history` | `POST` | 查看 Git 历史 | `limit`, `session_id` |

**示例 - 初始化会话：**
```bash
curl -X POST http://localhost:8000/init \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a web scraper",
    "todo": ["Research libraries", "Implement scraping"]
  }'
```
**注意**: `session_id` 是可选的，如果未提供将自动生成。

**迁移说明（严格 schema）：**
```json
// 旧写法（现在会被拒绝：未知字段 "root"）
{"root": "/tmp/work", "goal": "Build a web scraper"}

// 新写法
{"goal": "Build a web scraper", "session_id": "my-session"}
```

**示例 - 记录内存检查点：**
```json
{
  "branch": "feature-x",
  "contribution": "Implemented user authentication logic",
  "log_entries": ["Modified auth.py", "Added tests for JWT"],
  "metadata_updates": {"status": "in-progress", "coverage": 85}
}
```
**注意**: 服务器使用配置的 `session_id` 来定位正确的工作空间。

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

AI 智能体现在可以直接使用 GCC 工具：
```
- gcc_init: 初始化会话（goal, todo, 可选 session_id）
- gcc_branch: 创建探索分支（branch, purpose）
- gcc_commit: 记录检查点（branch, contribution, log_entries）
- gcc_context: 检索内存（branch, commit_id, log_tail）
- gcc_history: 查看提交历史（limit）
```


