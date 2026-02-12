# GCC (Git-Context-Controller)

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

GCC is a unified memory and context management system for AI agents. It leverages Git as a version-controlled backend to provide a persistent, structured, and auditable history of an agent's activities. GCC exposes its functionality through both a FastAPI-based HTTP server and an MCP (Model Context Protocol) proxy, making it easy for AI models to maintain context across different sessions and branches of exploration.

### Key Features

- **Git-Backed Memory**: Every change to the agent's context is automatically committed to a local Git repository, ensuring a full audit trail and easy state recovery.
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

#### Local Installation
```bash
pip install -e .
gcc-server  # Start the API server
# OR
gcc-mcp     # Start the MCP proxy (via stdin/stdout)
```

### API Reference

| Endpoint | Method | Description | Key Parameters |
| :--- | :--- | :--- | :--- |
| `/init` | `POST` | Initialize a session | `goal`, `todo`, `session_id` |
| `/branch` | `POST` | Create a branch | `branch`, `purpose`, `session_id` |
| `/commit` | `POST` | Record a checkpoint | `branch`, `contribution`, `log_entries`, `metadata_updates`, `update_main` |
| `/context` | `POST` | Get current memory | `branch`, `commit_id`, `log_tail`, `metadata_segment` |
| `/history` | `POST` | View git history | `limit`, `session_id` |

**Example Commit Request:**
```json
{
  "branch": "feature-x",
  "contribution": "Implemented user authentication logic",
  "log_entries": ["Modified auth.py", "Added tests for JWT"],
  "metadata_updates": {"status": "in-progress", "coverage": 85},
  "session_id": "session-123"
}
```

---

<a name="chinese"></a>
## 中文

GCC (Git-Context-Controller) 是一个为 AI 智能体设计的统一内存与上下文管理系统。它利用 Git 作为版本控制后端，为智能体的活动提供持久化、结构化且可审计的历史记录。GCC 通过基于 FastAPI 的 HTTP 服务器和 MCP (Model Context Protocol) 代理暴露其功能，使 AI 模型能够跨不同的会话和探索分支轻松维护上下文。

### 核心特性

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

#### 本地安装
```bash
pip install -e .
gcc-server  # 启动 API 服务器
# 或者
gcc-mcp     # 启动 MCP 代理（通过 stdin/stdout）
```

### API 参考

| 端点 | 方法 | 描述 | 关键参数 |
| :--- | :--- | :--- | :--- |
| `/init` | `POST` | 初始化会话 | `goal`, `todo`, `session_id` |
| `/branch` | `POST` | 创建分支 | `branch`, `purpose`, `session_id` |
| `/commit` | `POST` | 记录检查点 | `branch`, `contribution`, `log_entries`, `metadata_updates`, `update_main` |
| `/context` | `POST` | 获取当前内存 | `branch`, `commit_id`, `log_tail`, `metadata_segment` |
| `/history` | `POST` | 查看 Git 历史 | `limit`, `session_id` |

**示例 Commit 请求:**
```json
{
  "branch": "feature-x",
  "contribution": "实现了用户身份验证逻辑",
  "log_entries": ["修改了 auth.py", "添加了 JWT 测试"],
  "metadata_updates": {"status": "进行中", "coverage": 85},
  "session_id": "session-123"
}
```
