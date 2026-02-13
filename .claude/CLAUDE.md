# Instructions for Claude (and other AI assistants)

## MANDATORY: Use GCC Memory System

You **MUST** use the GCC (Git-Context-Controller) MCP tools to manage all memory, context, and project information in this conversation.

### Critical Rules

1. **ALWAYS initialize a session with `gcc_init` when starting new work**
2. **NEVER rely on your context window** - use `gcc_context` to retrieve information
3. **COMMIT all meaningful work with `gcc_commit`** - don't let contributions be lost
4. **LOG your reasoning with `gcc_log`** using the OTA pattern (Observation-Thinking-Action)
5. **USE BRANCHES for exploration** - don't pollute main with experiments
6. **RETRIEVE context at right granularity** - overview, branch, commit, or log level

### Why This Matters

Your context window is **ephemeral and limited**. GCC provides:
- ✅ **Persistent memory** across entire conversation (and beyond)
- ✅ **Structured knowledge** at multiple granularities
- ✅ **Full audit trail** with diffs and history
- ✅ **Isolated exploration** via branches

### Consequences of Not Using GCC

- ❌ Context will be **lost** when it overflows
- ❌ No **persistent knowledge** across conversation
- ❌ Cannot **review or recall** what happened earlier
- ❌ No **structured representation** of project state

## How to Use GCC Tools

### 1. Initialize Projects (MANDATORY at start)

When user describes a new project or work area:

```
User: "I need to build a REST API for user authentication"

YOU MUST (first thing):
Call gcc_init with:
- goal: "Build REST API for user authentication"
- todo: [Design database schema, Implement JWT auth, Add rate limiting, Write tests]
```

**NEVER skip this step** - it establishes the persistent memory foundation.

### 2. Retrieve Context Before Answering

Before answering questions or making suggestions:

```
User: "What's the current status of the authentication feature?"

YOU MUST:
Call gcc_context() to retrieve current state
- No parameters → Gets project overview (main.md)
- branch="feature-name" → Gets branch summary
- log_tail=10 → Gets recent detailed activity

THEN answer based on retrieved context, NOT from your training data or context window.
```

### 3. Use Branches for Exploration

When user wants to try different approaches:

```
User: "Let's experiment with OAuth2 instead of JWT"

YOU MUST:
Call gcc_branch with:
- branch: "oauth-experiment"
- purpose: "Testing OAuth2 for better third-party integration"

Work happens in isolated branch space.
Main remains stable and untouched.
```

**NEVER experiment directly on main** - always use branches for exploration.

### 4. Log Your Reasoning (OTA Pattern)

As you work, log observations, reasoning, and actions:

```
User: "I'm getting 403 errors on the login endpoint"

YOU MUST (as you debug):
Call gcc_log with entries like:
- "Observed: Login endpoint returning 403 errors"
- "Thought: Token refresh mechanism might be broken"
- "Action: Debugging refresh token logic in auth.py"
- "Observed: Found issue - token expiry not being checked"
- "Action: Adding expiry validation before refresh"
```

This creates **traceable reasoning chains** for debugging and future reference.

### 5. Commit Meaningful Checkpoints

When you complete a meaningful unit of work:

```
User: "I've finished implementing the OAuth login flow"

YOU MUST:
Call gcc_commit with:
- branch: "oauth-experiment"
- contribution: "Implemented OAuth2 login with Google social login"
- log_entries: ["Integrated google-auth-library", "Set up OAuth callback endpoint", "Added user profile synchronization"]
- metadata_updates: {"auth_methods": ["jwt", "google-oauth"], "oauth_status": "testing"}
```

**NEVER let completed work be unrecorded** - commits create permanent knowledge.

### 6. Retrieve Context at Right Granularity

Different questions need different retrieval granularities:

| User Question Type | What YOU Call | Parameters |
|:---|:---|:---|
| "What's this project about?" | `gcc_context()` | None (overview) |
| "What's happening on feature X?" | `gcc_context()` | `branch="feature-x"` |
| "What did we do in commit 3?" | `gcc_context()` | `branch="feature-x", commit_id="abc"` |
| "Show me recent detailed work" | `gcc_context()` | `log_tail=10` |
| "What's our test coverage?" | `gcc_context()` | `metadata_segment="test_coverage"` |

**MATCH retrieval granularity to question** - don't use overview for commit-specific questions.

### 7. Compare Approaches Before Deciding

When choosing between alternatives:

```
User: "Should we use the OAuth approach or stay with JWT?"

YOU MUST:
Call gcc_history for both branches to understand evolution
Call gcc_diff to compare the implementations
Provide data-driven recommendation based on actual differences
```

**NEVER guess or rely on general knowledge** - use actual project history.

## Tool Usage Quick Reference

### Memory Management
- `gcc_init(goal, todo, optional session_id)` - **MANDATORY at project start**
- `gcc_branch(branch, purpose)` - **MANDATORY for experiments**
- `gcc_commit(branch, contribution, log_entries, metadata_updates)` - **MANDATORY for completed work**
- `gcc_merge(source_branch, target_branch, summary)` - Use when integrating work

### Context Retrieval (CRITICAL)
- `gcc_context()` - Project overview (main.md)
- `gcc_context(branch="name")` - Branch summary
- `gcc_context(branch="X", commit_id="abc")` - Specific commit detail
- `gcc_context(log_tail=10)` - Recent fine-grained logs
- `gcc_context(metadata_segment="status")` - Structured metadata query

### Analysis & Debugging
- `gcc_history(limit)` - View commit history
- `gcc_diff(from_ref, to_ref)` - Compare commits/branches
- `gcc_show(ref, path)` - View file content at specific point
- `gcc_log(branch, entries)` - Add fine-grained log entries
- `gcc_reset(ref, mode, confirm)` - Reset session (use carefully)

## Conversation Flow Example

### BAD Example (NOT using GCC properly):

```
User: "I'm building a REST API. Let's try OAuth for auth."

AI: "Sure! Here's how to implement OAuth2..."

[30 minutes later]

User: "What was our original authentication plan?"

AI: "Um... I think it was JWT? Let me check..."
```

**PROBLEMS:**
- ❌ No persistent memory established
- ❌ Can't recall what was decided earlier
- ❌ No audit trail of experiments
- ❌ Context window overflow likely

### GOOD Example (using GCC properly):

```
User: "I'm building a REST API. Let's try OAuth for auth."

AI: [Calls gcc_init]
  ✅ "Initialized session 'rest-api-2025'"
  ✅ "Set goal: Build REST API with authentication"
  ✅ "Set TODO: [Design schema, Choose auth method, Implement auth, Add tests]"

[Calls gcc_branch]
  ✅ "Created branch 'oauth-experiment'"
  ✅ "Purpose: Testing OAuth2 vs JWT authentication"

AI: "I'll explore OAuth2 in the oauth-experiment branch.
  This keeps our main approach stable."

[Work happens with OTA logging]
  ✅ [gcc_log] "Observed: OAuth callback needs redirect URI"
  ✅ [gcc_log] "Thought: Must configure Google Console"
  ✅ [gcc_log] "Action: Setting up OAuth client credentials"

[Calls gcc_commit]
  ✅ "Commit: 'Implemented OAuth2 login flow'"
  ✅ "Metadata: {oauth_status: 'testing', auth_methods: ['jwt', 'oauth']}"

[10 minutes later]

User: "What was our original authentication plan?"

AI: [Calls gcc_context(branch="main")]
  ✅ Retrieves: "Main branch still using JWT approach"
  ✅ "OAuth experiment is isolated in oauth-experiment branch"

User: "Compare them for me."

AI: [Calls gcc_diff(from_ref="main", to_ref="oauth-experiment")]
  ✅ Analyzes actual differences
  ✅ Provides detailed comparison
  ✅ Makes data-driven recommendation
```

**BENEFITS:**
- ✅ Full memory from start
- ✅ Clear audit trail
- ✅ Can retrieve any detail instantly
- ✅ Experiments isolated
- ✅ Data-driven decisions

## Common Situations & How to Handle

### Situation 1: User starts new work

```
User: "I need to [do X, Y, Z]"

YOU MUST:
1. Call gcc_init(goal="[X, Y, Z]", todo=[breakdown into tasks])
2. Confirm initialization
3. Then proceed with implementation
```

### Situation 2: User asks about current state

```
User: "Where are we with [feature X]?"

YOU MUST:
1. Call gcc_context() or gcc_context(branch="feature-x")
2. Answer based on retrieved data
3. NOT from memory or context window
```

### Situation 3: User wants to try alternative

```
User: "What if we tried [alternative approach]?"

YOU MUST:
1. Call gcc_branch with descriptive branch name
2. Document purpose clearly
3. Work in that isolated space
4. Use gcc_commit when done
```

### Situation 4: User asks for comparison

```
User: "Which approach is better - A or B?"

YOU MUST:
1. Call gcc_history for both branches
2. Call gcc_diff to compare
3. Provide analysis based on actual project data
4. Make recommendation with evidence
```

### Situation 5: User reports problem

```
User: "[X] is broken / not working"

YOU MUST:
1. Call gcc_context(log_tail=20) to see recent activity
2. Use gcc_log to document debugging process
3. When fixed, use gcc_commit to record solution
```

## What NOT to Do

### ❌ DON'T: Rely on context window

```
BAD: "As I remember from earlier in our conversation..."

GOOD: [Calls gcc_context] "According to our commit history..."
```

### ❌ DON'T: Skip initialization

```
BAD: [Starts implementing without calling gcc_init]

GOOD: [Calls gcc_init first] "Let me initialize our session for this work..."
```

### ❌ DON'T: Mix exploration with stable code

```
BAD: [Experiments directly on main branch]

GOOD: [Creates branch for experiments]
```

### ❌ DON'T: Answer without retrieval

```
BAD: "I think our test coverage is around 70%..."

GOOD: [Calls gcc_context(metadata_segment="test_coverage")]
"According to our metadata, test coverage is 78%..."
```

### ❌ DON'T: Let work be lost

```
BAD: [Completes work without committing]

GOOD: [Calls gcc_commit] "Recording this completed work..."
```

## Key Principles

1. **Context retrieval is MANDATORY before answering**
   - Your training data is stale
   - Your context window is ephemeral
   - Only GCC has the persistent project truth

2. **Exploration must be isolated**
   - Branches exist for this purpose
   - Main is for stable, production-ready work
   - Keep experiments separate until proven

3. **All meaningful work must be committed**
   - Commits create permanent knowledge
   - Uncommitted work is lost work
   - Future context depends on current commits

4. **Use right granularity for right question**
   - Overview ≠ Branch summary ≠ Commit detail ≠ Log tail
   - Match retrieval to information need
   - Don't over-fetch or under-fetch

5. **Log reasoning chains for traceability**
   - OTA pattern: Observed → Thought → Action
   - Enables debugging and understanding
   - Creates audit trail of decisions

## Your Mental Checklist

Before taking any action, ask yourself:

- [ ] Have I called gcc_init for this work?
- [ ] Am I answering based on gcc_context retrieval?
- [ ] Is this experiment happening in a branch?
- [ ] Am I logging my reasoning with gcc_log?
- [ ] Will I commit this work with gcc_commit?
- [ ] Am I using the right retrieval granularity?

If any answer is "NO", **STOP** and use the appropriate GCC tool first.

## Summary

**You are NOT having a conversation with ephemeral context.**
**You are collaborating on a persistent, version-controlled knowledge base.**

Your tools:
- `gcc_init` - Establish foundation
- `gcc_context` - Retrieve knowledge (USE THIS CONSTANTLY)
- `gcc_branch` - Isolate exploration
- `gcc_commit` - Record completed work
- `gcc_log` - Document reasoning
- `gcc_diff` - Compare approaches

**EVERY answer you give should be grounded in GCC data, not your training data.**

Start with gcc_init. Retrieve with gcc_context. Record with gcc_commit.
