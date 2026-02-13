# Claude Code + GCC Memory System Setup Guide

This guide helps you configure Claude Code to use the GCC (Git-Context-Controller) memory system for persistent, version-controlled AI memory management.

## Quick Start

### 1. Install GCC

```bash
# Using Docker (recommended)
docker-compose up -d

# OR locally
pip install -e .
gcc-server  # Start API server
```

### 2. Configure Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gcc": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8000"
      }
    }
  }
}
```

Restart Claude Desktop.

## Core Concepts

### Sessions
A **session** is an isolated workspace with its own Git repository. All memory (goals, branches, commits, logs) is stored within a session.

### Branches
Within a session, **branches** let you explore different approaches in isolation. Each branch has its own memory files.

### Memory Components
- **main.md**: Global roadmap, goals, and TODO lists
- **commit.md**: Structured contribution checkpoints
- **log.md**: Fine-grained execution logs (OTA pattern)
- **metadata.yaml**: Structured state storage

## Usage Scenarios

### Scenario 1: Start a New Project

**Tell Claude:**
```
Initialize a GCC session for "Build a REST API with authentication".
TODO: Design database schema, Implement JWT auth, Add rate limiting.
```

**Claude will use:**
- `gcc_init` with goal and todo
- Creates session workspace with Git tracking
- Sets up main.md with your project goals

### Scenario 2: Exploratory Development

**Tell Claude:**
```
Create a branch "oauth-experiment" to try OAuth2 instead of JWT.
Document the purpose: "Testing OAuth2 for better third-party integration"
```

**Claude will use:**
- `gcc_branch` to create isolated workspace
- `gcc_commit` to record experiments
- Keep main branch stable while exploring

### Scenario 3: Detailed Progress Tracking

**Tell Claude:**
```
As you work on the user authentication feature, log your observations and decisions.
```

**Claude will use:**
- `gcc_log` for granular entries: "Modified auth.py to add refresh token validation"
- `gcc_commit` for checkpoint summaries: "Implemented OAuth2 login flow"
- Full audit trail in Git history

### Scenario 4: Context Retrieval

**Ask Claude:**
```
What was the last commit on the "oauth-experiment" branch?
Show me the recent activity logs.
```

**Claude will use:**
- `gcc_context` with `branch` and `commit_id` parameters
- `gcc_context` with `log_tail` parameter
- Retrieve exactly what you need, at the right granularity

### Scenario 5: Compare Approaches

**Tell Claude:**
```
Compare the JWT implementation on main branch with the OAuth experiment.
Show me the differences in commit history.
```

**Claude will use:**
- `gcc_diff` to compare commits
- `gcc_history` for each branch
- Data-driven decision making

## Session Locking

### What is Session Locking?

When `session_id` is configured via environment variable or Docker container ID, GCC **locks** the session to prevent AI from accidentally overriding it.

### When Locked

- ✅ AI-provided `session_id` is **ignored**
- ✅ Only configured value is used
- ✅ Ensures production environments maintain isolation

### Locking Conditions

| Configuration | Behavior |
|:---|:---|
| `GCC_SESSION_ID` environment variable set | **Locked** - AI cannot override |
| Docker with valid `HOSTNAME` (≥12 chars) | **Locked** - Uses container ID |
| No configuration | **Unlocked** - AI can specify sessions |

### Recommended Configuration

**For Production/Fixed Projects:**
```json
{
  "mcpServers": {
    "gcc": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8000",
        "GCC_SESSION_ID": "my-project-2024"
      }
    }
  }
}
```

**For Development/Exploration:**
```json
{
  "mcpServers": {
    "gcc": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8000"
      }
    }
  }
}
```

**For Docker Deployment:**
```yaml
# docker-compose.yml
services:
  gcc-server:
    image: gcc-mem-system
    environment:
      - GCC_DATA_ROOT=/data
      - GCC_PORT=8000
    volumes:
      - ./data:/data
```

Container will automatically use `container-<hostname>` as session ID.

## Best Practices

### 1. Initialize Projects Clearly
```
Start a GCC session for "Build web scraper for news sites".
Goals: [Extract article titles, Handle pagination, Store in database].
```

### 2. Use Branches for Exploration
```
Create a branch "selenium-approach" to test browser automation vs simple HTTP requests.
```

### 3. Commit Meaningful Checkpoints
Claude will automatically structure commits with:
- **contribution**: High-level summary
- **log_entries**: Detailed technical observations
- **metadata_updates**: State changes (status, coverage, etc.)

### 4. Retrieve Context at Right Granularity
```
What's the current project status?         → gcc_context() (overview)
What happened on "feature-x" branch?      → gcc_context(branch="feature-x")
Show last 10 log entries                 → gcc_context(log_tail=10)
```

### 5. Review History Before Major Changes
```
Show me the commit history for the "auth-refactor" branch to understand the evolution.
```

## Tool Reference

Claude has access to these tools:

- **gcc_init**: Initialize session (goal, todo, optional session_id)
- **gcc_branch**: Create exploration branch (branch, purpose)
- **gcc_commit**: Record checkpoint (branch, contribution, log_entries, metadata_updates)
- **gcc_context**: Retrieve memory (branch, commit_id, log_tail, metadata_segment)
- **gcc_history**: View commit history (limit)
- **gcc_log**: Append fine-grained logs (branch, entries)
- **gcc_merge**: Merge branch to target (source_branch, target_branch, summary)
- **gcc_diff**: Compare commits (from_ref, to_ref)
- **gcc_show**: View file at ref (ref, path)
- **gcc_reset**: Reset to ref (ref, mode, confirm)

## Troubleshooting

### "Failed to connect to GCC server"
Ensure the server is running:
```bash
docker-compose ps  # Check if running
docker-compose up -d  # Start if not
```

### "Session not found"
Check your session configuration:
- If locked: Verify `GCC_SESSION_ID` matches your intended session
- If unlocked: Check if AI is using correct session_id parameter

### Need to reset session?
```bash
# Delete specific session data
rm -rf /data/sessions/your-session-id

# OR reset to blank state via API
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"ref": "HEAD", "mode": "hard", "confirm": true}'
```

## Example Conversation Flow

```
You: Initialize a GCC session for "Build a CLI tool for file management".
     TODO: [Implement file search, Add batch operations, Create progress UI].

Claude: ✅ Created session "mcp-12345"
      Set main.md with goal and TODO items.

---

You: Create a branch "fuzzy-search" to experiment with fuzzy matching algorithms.

Claude: ✅ Created branch "fuzzy-search"
      Purpose: "Testing fuzzy matching for better file search"

---

You: Log your progress as you implement the fuzzy search feature.

Claude: ✅ Added log entry: "Researching fuzzy matching libraries"
      ✅ Added log entry: "Integrated fuzzywuzzy for path matching"
      ✅ Commit: "Implemented fuzzy search with fuzzywuzzy library"

---

You: What have we accomplished so far?

Claude: 📋 Retrieved context:
      Session: mcp-12345
      Goal: Build a CLI tool for file management
      TODO: [✓ Implement file search, ✓ Add batch operations, Create progress UI]
      Branch: fuzzy-search
      Recent commits: [Implemented fuzzy search, Added unit tests]

---

You: Compare the fuzzy search implementation with the main branch approach.

Claude: 🔍 Comparing branches...
      fuzzy-search uses fuzzywuzzy (85% match threshold)
      main uses exact string matching
      Trade-off: Accuracy vs performance
      Recommendation: Merge fuzzy-search with configurable threshold
```

## Advanced Usage

### Multi-Project Setup
Configure multiple GCC servers for different projects:
```json
{
  "mcpServers": {
    "gcc-web-app": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8000",
        "GCC_SESSION_ID": "web-app-prod"
      }
    },
    "gcc-data-pipeline": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8001",
        "GCC_SESSION_ID": "data-pipeline-prod"
      }
    }
  }
}
```

### Team Collaboration
Store session data in shared volume:
```yaml
# docker-compose.yml
services:
  gcc-server:
    volumes:
      - nfs-share:/data

volumes:
  nfs-share:
    driver: local
    driver_opts:
      type: nfs
      device: ":/path/to/shared"
```

## Resources

- [GCC Documentation](../../README.md)
- [API Reference](../../README.md#api-reference)
- [Session Locking Details](../../README.md#session-locking)

---

**Need help?** Check server logs:
```bash
docker-compose logs -f gcc-server
```
