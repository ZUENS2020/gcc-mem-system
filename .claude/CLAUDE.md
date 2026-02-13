# Git Context Controller (GCC) - Claude Code Setup Guide

Based on: "Git Context Controller: Manage the Context of LLM-based Agents like Git" (Wu et al., 2025)

## Overview

**GCC (Git-Context-Controller)** is a unified memory and context management system for AI agents. It leverages Git as a version-controlled backend to provide a **persistent, structured, and auditable** history of an agent's activities.

### Key Innovation

GCC treats **agent context as code**:
- Every context change becomes a Git commit
- Full audit trail with diff capabilities
- Structured memory at multiple granularities
- Branch-based exploration without pollution

### Why This Matters

**Traditional LLM limitations:**
- ❌ Context windows overflow and get truncated
- ❌ No persistent memory across sessions
- ❌ Cannot track what changed over time
- ❌ No structured knowledge representation

**GCC solves these:**
- ✅ Persistent Git-based storage (unlimited size)
- ✅ Session-based isolation and continuity
- ✅ Full commit history with diffs
- ✅ Structured: Roadmap → Branches → Commits → Logs

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

Add to your Claude Desktop config:

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

## System Architecture

### Memory Hierarchy

GCC organizes agent memory in a **hierarchical structure**:

```
Session (Isolated Workspace)
│
├── main.md                 # Global roadmap, goals, TODO
│   └── High-level project direction
│
└── Branches (Exploration Spaces)
    │
    └── Branch Name
        ├── commit.md           # Structured contribution checkpoints
        │   └── "What was accomplished" summaries
        │
        ├── log.md              # Fine-grained execution logs (OTA)
        │   └── "Observation-Thinking-Action" entries
        │
        └── metadata.yaml        # Structured state storage
            └── Key-value pairs for environment info
```

### Context Retrieval Granularities

GCC enables **multi-granularity context retrieval**:

| Granularity | Tool | Use Case |
|:---|:---|:---|
| **Project Overview** | `gcc_context()` | "What's this project about?" |
| **Branch Summary** | `gcc_context(branch="name")` | "What's the status of feature X?" |
| **Commit Detail** | `gcc_context(branch="X", commit_id="abc")` | "What did we do in checkpoint 3?" |
| **Execution Log** | `gcc_context(branch="X", log_tail=10)` | "Show me last 10 observations" |
| **Metadata Segment** | `gcc_context(metadata_segment="status")` | "What's the current progress?" |

### OTA Pattern

GCC uses the **Observation-Thinking-Action (OTA)** pattern for fine-grained logging:

```yaml
# log.md example
- Observed: User authentication is failing with 403 errors
- Thought: Token refresh mechanism might be broken
- Action: Debugging refresh token logic in auth.py
- Observed: Found issue - token expiry not checked
- Action: Adding expiry validation before refresh
```

This creates **traceable reasoning chains** for debugging and analysis.

## Core Concepts

### 1. Sessions (Workspaces)

A **session** is an isolated workspace with its own Git repository. Use sessions for:
- Different projects or clients
- Separate experimentation spaces
- Multi-tenant isolation

**Directory Structure:**
```
/data/sessions/{session_id}/.GCC/
├── main.md              # Session goals and roadmap
├── branches/            # Branch-specific memory
│   └── {branch_name}/
│       ├── commit.md     # Contribution checkpoints
│       ├── log.md       # Detailed logs
│       └── metadata.yaml # Structured metadata
└── .git/               # Version control backend
```

### 2. Branches (Exploration)

Within a session, **branches** enable isolated exploration:
- Try different approaches without polluting main
- Experiment with alternative algorithms
- Parallel development paths
- Easy comparison via `gcc_diff`

**Branch Isolation:**
```
main/          → Stable, production-ready approach
├── oauth-exp/    → Exploring OAuth2 authentication
└── selenim/     → Experimenting with browser automation
```

### 3. Checkpoints (Structured Memory)

**commit.md** stores **structured contribution summaries**:
```markdown
# Contribution Checkpoints

## [Commit Hash] Implementing User Authentication
**Contribution**: Added JWT-based authentication with refresh token support
**Metadata**: {"status": "in-progress", "coverage": "65%"}

## [Commit Hash] OAuth2 Integration Complete
**Contribution**: Migrated from JWT to OAuth2 for third-party integration
**Metadata**: {"status": "completed", "coverage": "85%"}
```

### 4. Metadata (Structured State)

**metadata.yaml** provides **queryable structured state**:
```yaml
status: "in-progress"
test_coverage: 78
last_reviewed: "2025-02-13"
dependencies:
  - fastapi
  - pydantic
known_issues:
  - Rate limiting not implemented
```

Enables context retrieval like:
- "What's the current status?" → `metadata.status`
- "What's our test coverage?" → `metadata.test_coverage`

## Usage Scenarios

### Scenario 1: Project Initialization

**User Prompt:**
```
Start a GCC session for building a REST API with authentication.
Goals: [Design database schema, Implement JWT auth, Add rate limiting]
```

**What Happens:**
1. Claude calls `gcc_init` with your goal and TODO
2. GCC creates isolated workspace with Git repo
3. Sets up `main.md` with project roadmap
4. Every subsequent action tracked in this session

**Result:**
```json
{
  "gcc_root": "/data/sessions/rest-api-auth/.GCC",
  "session": "rest-api-auth",
  "main": ".../main.md"
}
```

### Scenario 2: Exploratory Development

**User Prompt:**
```
Create a branch "oauth-experiment" to test OAuth2 instead of JWT.
Document purpose: "Testing OAuth2 for better third-party integration"
```

**What Happens:**
1. Claude calls `gcc_branch` to create isolated space
2. Branch has its own `commit.md`, `log.md`, `metadata.yaml`
3. Main branch remains stable and untouched
4. Can compare approaches later with `gcc_diff`

**Benefits:**
- ✅ Experiment freely without breaking main
- ✅ Easy to rollback or discard
- ✅ Clear audit trail of experiments

### Scenario 3: Fine-Grained Progress Tracking

**User Prompt:**
```
As you work on the authentication feature, log your observations and decisions.
```

**What Happens:**
1. Claude uses `gcc_log` for granular OTA entries:
   ```
   - Observed: auth.py returning 403 errors
   - Thought: Token refresh might be broken
   - Action: Debugging refresh logic
   ```

2. Uses `gcc_commit` for meaningful checkpoints:
   ```
   Contribution: "Fixed token refresh validation"
   Log entries: [...]
   Metadata: {"auth_status": "working"}
   ```

**Result:**
- Full audit trail from problem → diagnosis → solution
- Can review "Why did we make this decision?"
- Easy to understand months later

### Scenario 4: Context Retrieval

**User:**
```
What's the current project status?
```

**Claude:**
```
Retrieving overview...
📋 main.md:
  Goal: Build REST API with authentication
  TODO: [✓ Database design, ✓ JWT auth, Rate limiting]

📊 Recent activity:
  Branch: oauth-exp
  Status: Testing Google OAuth integration
  Latest: "Fixed redirect URI mismatch"
```

**User:**
```
Show me the last 5 log entries from the oauth experiment.
```

**Claude:**
```
Retrieving fine-grained logs...
1. Observed: OAuth callback returning 400
2. Thought: Redirect URI might not match
3. Action: Checking Google Console configuration
4. Observed: URI missing /callback suffix
5. Action: Updating redirect URI in code
```

### Scenario 5: Comparing Approaches

**User:**
```
Compare the OAuth experiment on the oauth-exp branch with the current JWT approach on main.
```

**Claude:**
```
Analyzing differences...

🔍 Authentication Approach Comparison:

main (JWT):
  + Simpler setup
  + No external dependencies
  - Limited to first-party apps
  - No social login support

oauth-exp (OAuth2):
  + Supports Google/GitHub social login
  + Industry standard
  - More complex token management
  - Requires external provider setup

Recommendation: Merge oauth-exp with feature flag
```

## Session Locking

### What is Session Locking?

When `session_id` is configured via environment variable or Docker container ID, GCC **locks** the session to prevent AI from accidentally overriding it.

### Why This Matters

**Problem:** In production environments, you don't want AI to use wrong session:
- Multi-tenant deployments
- Containerized environments
- Fixed project sessions

**Solution:** Lock session to configured value, ignore AI-provided `session_id`

### Locking Conditions

| Configuration | Behavior |
|:---|:---|
| `GCC_SESSION_ID` environment variable set | **Locked** - AI cannot override |
| Docker with valid `HOSTNAME` (≥12 chars) | **Locked** - Uses container ID |
| No configuration | **Unlocked** - AI can specify sessions |

### Configuration Examples

**Production/Fixed Session:**
```json
{
  "mcpServers": {
    "gcc": {
      "command": "gcc-mcp",
      "env": {
        "GCC_SERVER_URL": "http://localhost:8000",
        "GCC_SESSION_ID": "my-production-project"
      }
    }
  }
}
```

**Development/Exploration:**
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

**Docker Deployment:**
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

Container automatically uses `container-<hostname>` as locked session ID.

## Tool Reference

Claude has access to these GCC tools:

### Memory Management
- **gcc_init**: Initialize session (goal, todo, optional session_id)
- **gcc_branch**: Create exploration branch (branch, purpose)
- **gcc_commit**: Record checkpoint (branch, contribution, log_entries, metadata_updates)
- **gcc_merge**: Merge branch to target (source_branch, target_branch, summary)

### Context Retrieval
- **gcc_context**: Retrieve memory at multiple granularities
  - No params: Project overview (main.md)
  - `branch`: Branch summary
  - `branch + commit_id`: Specific checkpoint detail
  - `log_tail`: Last N log entries (OTA pattern)
  - `metadata_segment`: Structured metadata query

### Analysis & Debugging
- **gcc_history**: View commit history (limit)
- **gcc_diff**: Compare commits (from_ref, to_ref)
- **gcc_show**: View file at ref (ref, path)
- **gcc_log**: Append fine-grained log entries (branch, entries)
- **gcc_reset**: Reset to ref (ref, mode, confirm)

## Best Practices

### 1. Initialize Projects Clearly
```
Start a GCC session for "Build web scraper for news sites".
Goals: [Extract article titles, Handle pagination, Store in PostgreSQL].
```

**Why:** Clear initialization provides strong foundation for all subsequent work.

### 2. Use Branches for Exploration
```
Create a branch "selenium-approach" to test browser automation vs simple HTTP requests.
```

**Why:** Keeps main stable. Easy to compare approaches with `gcc_diff`.

### 3. Log Observations, Not Just Actions
```
Use OTA pattern: Log what you observe, your reasoning, and then the action.
```

**Example:**
```yaml
- Observed: Pagination links are JavaScript-generated
- Thought: BeautifulSoup won't work, need browser automation
- Action: Switching to Selenium for this site
```

**Why:** Traceable reasoning chains help debug and understand decisions later.

### 4. Commit Meaningful Checkpoints
```
When you complete a meaningful unit of work, create a checkpoint.
Include: What was done, why it matters, current status.
```

**Example:**
```
Contribution: "Implemented OAuth2 with Google social login"
Metadata: {"auth_methods": ["jwt", "google-oauth"], "status": "in-testing"}
```

**Why:** High-level summaries complement fine-grained logs.

### 5. Retrieve Context at Right Granularity
```
"What's the project status?"           → Overview (main.md)
"What's happening on feature X?"     → Branch summary
"Show me recent detailed work"        → Log tail (OTA)
"What's the current test coverage?" → Metadata query
```

**Why:** Different questions need different granularities.

### 6. Review History Before Changes
```
Before refactoring, show me commit history to understand the evolution.
```

**Why:** Historical context prevents repeating mistakes.

### 7. Use Diff to Compare Approaches
```
Compare the experiment branch with main before deciding which to keep.
```

**Why:** Data-driven decision making.

## Advanced Usage

### Multi-Project Setup
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

Team members can:
- Share context across different AI instances
- Review each other's reasoning chains
- Collaborate on same memory base

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
      Isolated from main branch

---

You: Log your progress as you implement the fuzzy search feature.

Claude: 📝 [OTA Entry 1]
      - Observed: Current exact matching fails on typos
      - Thought: Users often mistype file names
      - Action: Researching fuzzywuzzy library

      📝 [OTA Entry 2]
      - Observed: fuzzywuzzy provides ratio-based matching
      - Thought: Need to test threshold for best UX
      - Action: Implementing with 85% ratio threshold

      ✅ Checkpoint
      Contribution: "Implemented fuzzy search with fuzzywuzzy"
      Metadata: {"status": "testing", "threshold": 0.85}

---

You: What have we accomplished so far?

Claude: 📋 Project Overview
      Session: mcp-12345
      Goal: Build a CLI tool for file management

      📋 TODO Progress
      - [✓] Implement file search (with fuzzy matching!)
      - [ ] Add batch operations
      - [ ] Create progress UI

      📊 Recent Activity
      Branch: fuzzy-search
      Latest: "Implemented fuzzy search with 85% threshold"
      Test Results: 92% user satisfaction in testing

---

You: Compare the fuzzy search implementation with the main branch approach.

Claude: 🔍 Comparing Approaches...

      main (exact matching):
        Pros: Faster (O(n)), simpler
        Cons: Fails on typos, poor UX

      fuzzy-search (fuzzy matching):
        Pros: Handles typos, better UX (92% satisfaction)
        Cons: Slower (O(n*m)), more complex

      📊 Recommendation: Merge fuzzy-search with configurable threshold
      Add FUZZY_THRESHOLD env variable to let users tune

---

You: Good analysis! Merge the fuzzy-search branch into main.

Claude: ✅ Merging fuzzy-search → main
      Merge Summary: "Added fuzzy file search with 85% match threshold"

      Updated main.md TODO:
      - [✓] Implement file search
      - [ ] Add batch operations
      - [ ] Create progress UI
```

## Troubleshooting

### "Failed to connect to GCC server"
```
Ensure the server is running:
docker-compose ps

If not running:
docker-compose up -d

Check server logs:
docker-compose logs -f gcc-server
```

### "Session not found"
```
Check your session configuration:
1. If locked (GCC_SESSION_ID set): Verify it matches intended session
2. If unlocked: Check if AI is using correct session_id parameter
3. List existing sessions: ls /data/sessions/
```

### "Branch not found"
```
List available branches:
curl -X POST http://localhost:8000/context \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session"}' | jq '.branches'
```

### Need to reset session?
```
Delete specific session:
rm -rf /data/sessions/your-session-id

OR reset via API (with confirmation):
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"ref": "HEAD", "mode": "hard", "confirm": true}'
```

## Theoretical Foundation

### Why Git-Backed Memory?

Traditional LLM context management:
- **Ephemeral**: Lost when conversation ends
- **Unstructured**: Flat context window
- **Opaque**: Can't see evolution

GCC provides:
- **Persistent**: Git ensures nothing is lost
- **Structured**: Hierarchy (Roadmap → Branch → Commit → Log)
- **Transparent**: Full history with diffs

### Context as Version Control

GCC treats agent context like **software code**:
- Each change is a commit
- Branches enable parallel exploration
- Diffs show what changed and why
- History provides evolution trace

### Multi-Granularity Memory

Humans think at different levels:
- **High level**: "What are we building?" (main.md)
- **Mid level**: "What did we accomplish?" (commit.md)
- **Low level**: "What just happened?" (log.md - OTA)

GCC supports all levels, enabling **right-granularity retrieval** for the question.

## Resources

- [Paper: "Git Context Controller: Manage the Context of LLM-based Agents like Git"](https://arxiv.org/abs/2501.13245)
- [GCC Documentation](../../README.md)
- [API Reference](../../README.md#api-reference)
- [Session Locking Details](../../README.md#session-locking)

---

**Need help?**
```bash
# Check server status
docker-compose ps

# View real-time logs
docker-compose logs -f gcc-server

# Test connection
curl http://localhost:8000/health
```
