"""MCP (Model Context Protocol) proxy for GCC system.

Translates MCP JSON-RPC requests to HTTP API calls.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

import httpx


# Windows encoding fix - important for non-ASCII characters
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")


# Configuration
SERVER_URL_ENV = "GCC_SERVER_URL"
SESSION_ID_ENV = "GCC_SESSION_ID"
DEFAULT_SERVER_URL = "http://localhost:8000"
DEFAULT_SESSION_ID = None

COMMIT_PROMPT_GUIDE = (
    "Commit guidance: every gcc_commit should include a clear contribution summary, "
    "key observations/actions in log_entries, and any file/module changes in metadata_updates. "
    "Update main milestones via update_main when needed."
)


# Tool definitions
TOOLS = [
    {
        "name": "gcc_init",
        "description": "Initialize a session memory store. Creates main.md (goal + todo) and prepares a git-backed workspace for memory commits. IMPORTANT: Use English only for all text values to avoid encoding issues. All paths are automatically managed by the server using session_id.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "goal": {"type": "string", "description": "Session goal or objective"},
                "todo": {"type": "array", "items": {"type": "string"}, "description": "List of todo items"},
                "session_id": {"type": "string", "description": "Unique session identifier (auto-generated if not provided)"},
            },
            "required": [],
        },
    },
    {
        "name": "gcc_branch",
        "description": "Create a memory branch within session. Writes commit.md/log.md/metadata.yaml and creates a git branch for isolated exploration. IMPORTANT: Use English only for 'purpose' to avoid encoding issues.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "branch": {"type": "string", "description": "Branch name"},
                "purpose": {"type": "string", "description": "Branch purpose"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": ["branch", "purpose"],
        },
    },
    {
        "name": "gcc_commit",
        "description": "Record a structured memory checkpoint. Appends to commit.md, optionally adds OTA log entries and metadata updates, updates main.md, and creates a git commit. IMPORTANT: Use English only for all text fields ('contribution', 'log_entries') to avoid encoding issues. " + COMMIT_PROMPT_GUIDE,
        "inputSchema": {
            "type": "object",
            "properties": {
                "branch": {"type": "string", "description": "Branch name"},
                "contribution": {"type": "string", "description": "This commit's contribution"},
                "purpose": {"type": "string", "description": "Branch purpose (optional if branch exists)"},
                "log_entries": {"type": "array", "items": {"type": "string"}, "description": "Log entries to add"},
                "metadata_updates": {"type": "object", "description": "Metadata to update"},
                "update_main": {"type": "string", "description": "Text to append to main.md"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": ["branch", "contribution"],
        },
    },
    {
        "name": "gcc_merge",
        "description": "Merge a source memory branch into a target branch (default main). Performs git merge and updates main.md plus merged commit/log/metadata content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_branch": {"type": "string", "description": "Source branch to merge from"},
                "target_branch": {"type": "string", "description": "Target branch (default: main)"},
                "summary": {"type": "string", "description": "Merge summary"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": ["source_branch"],
        },
    },
    {
        "name": "gcc_context",
        "description": "Retrieve structured context at multiple levels: project overview, branch summaries, commit entry, log tail, or a metadata segment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "branch": {"type": "string", "description": "Branch name to get context for"},
                "commit_id": {"type": "string", "description": "Specific commit ID"},
                "log_tail": {"type": "integer", "description": "Number of recent log entries"},
                "metadata_segment": {"type": "string", "description": "Metadata key to retrieve"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": [],
        },
    },
    {
        "name": "gcc_log",
        "description": "Append fine-grained OTA log entries to branch log.md and record a git commit for traceability.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "branch": {"type": "string", "description": "Branch name"},
                "entries": {"type": "array", "items": {"type": "string"}, "description": "Log entries"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": ["branch", "entries"],
        },
    },
    {
        "name": "gcc_history",
        "description": "List git commit history for session repository. Each entry reflects a memory change checkpoint.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Maximum commits to return"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": [],
        },
    },
    {
        "name": "gcc_diff",
        "description": "Show git diff between two refs to compare memory changes (e.g., HEAD~1..HEAD).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "from_ref": {"type": "string", "description": "Source git reference"},
                "to_ref": {"type": "string", "description": "Target git reference (default: HEAD)"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": ["from_ref"],
        },
    },
    {
        "name": "gcc_show",
        "description": "Show file content at a git ref (e.g., main.md or branches/<branch>/commit.md) to inspect memory before/after changes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ref": {"type": "string", "description": "Git reference (commit hash, branch, tag)"},
                "path": {"type": "string", "description": "File path within git repo"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": ["ref"],
        },
    },
    {
        "name": "gcc_reset",
        "description": "Reset session git repo to a ref. Use mode=soft or hard; hard reset requires confirm=true.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ref": {"type": "string", "description": "Git reference to reset to"},
                "mode": {"type": "string", "description": "Reset mode: soft or hard"},
                "confirm": {"type": "boolean", "description": "Required for hard reset"},
                "session_id": {"type": "string", "description": "Session identifier (uses default if not provided)"},
            },
            "required": ["ref"],
        },
    },
]


def _server_url() -> str:
    """Get server URL from environment.

    Returns:
        Server URL for HTTP API calls
    """
    return os.environ.get(SERVER_URL_ENV, DEFAULT_SERVER_URL).rstrip("/")


def _default_session_id() -> str:
    """Get or generate default session ID.

    Priority:
    1. GCC_SESSION_ID environment variable
    2. Container hostname (Docker)
    3. Process ID

    Returns:
        Session ID string
    """
    global DEFAULT_SESSION_ID

    # Priority 1: Explicit environment variable
    env_value = os.environ.get(SESSION_ID_ENV)
    if env_value:
        return env_value

    # Priority 2: Try container ID from hostname
    try:
        hostname = os.environ.get("HOSTNAME", "")
        if hostname and len(hostname) >= 12:
            if DEFAULT_SESSION_ID is None:
                DEFAULT_SESSION_ID = f"container-{hostname[:12]}"
            return DEFAULT_SESSION_ID
    except Exception:
        pass

    # Priority 3: Fallback to process ID
    if DEFAULT_SESSION_ID is None:
        DEFAULT_SESSION_ID = f"mcp-{os.getpid()}"
    return DEFAULT_SESSION_ID


def _ensure_session_id(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure session_id is set in arguments.

    Args:
        arguments: Tool arguments dictionary

    Returns:
        Arguments with session_id guaranteed to be set
    """
    if "session_id" not in arguments or not arguments.get("session_id"):
        arguments = dict(arguments)
        arguments["session_id"] = _default_session_id()
    return arguments


def _post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Make HTTP POST request to GCC server.

    Args:
        path: API endpoint path
        payload: Request body

    Returns:
        Response JSON

    Raises:
        httpx.HTTPError: If request fails
    """
    url = f"{_server_url()}{path}"
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        return response.json()


def _handle_tools_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP tool call by translating to HTTP request.

    Args:
        tool_name: Name of the tool being called
        arguments: Tool arguments

    Returns:
        Result from HTTP API

    Raises:
        ValueError: If tool name is unknown
    """
    mapping = {
        "gcc_init": "/init",
        "gcc_branch": "/branch",
        "gcc_commit": "/commit",
        "gcc_merge": "/merge",
        "gcc_context": "/context",
        "gcc_log": "/log",
        "gcc_history": "/history",
        "gcc_diff": "/diff",
        "gcc_show": "/show",
        "gcc_reset": "/reset",
    }
    if tool_name not in mapping:
        raise ValueError(f"Unknown tool: {tool_name}")

    # Server handles path management - just forward arguments
    payload = _ensure_session_id(arguments)
    return _post(mapping[tool_name], payload)


def _write_response(payload: Dict[str, Any]) -> None:
    """Write JSON-RPC response to stdout.

    Args:
        payload: Response dictionary

    Note:
        Uses ensure_ascii=False for proper Unicode handling.
        Falls back to ASCII with escapes if UTF-8 fails.
    """
    try:
        output = json.dumps(payload, ensure_ascii=False)
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Fallback to ASCII with escapes if UTF-8 fails
        output = json.dumps(payload, ensure_ascii=True)
    sys.stdout.write(output + "\n")
    sys.stdout.flush()


def _error_response(request_id: Any, message: str) -> Dict[str, Any]:
    """Create JSON-RPC error response.

    Args:
        request_id: Request ID from client
        message: Error message

    Returns:
        Error response dictionary
    """
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32000, "message": message},
    }


def main() -> None:
    """Main MCP proxy loop.

    Reads JSON-RPC requests from stdin, processes them,
    and writes responses to stdout.
    """
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        request_id = None
        try:
            request = json.loads(line)
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params") or {}

            if method == "initialize":
                protocol = params.get("protocolVersion") if isinstance(params, dict) else None
                protocol = protocol or "2024-11-05"
                _write_response(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "protocolVersion": protocol,
                            "serverInfo": {"name": "gcc-mcp", "version": "1.0.0"},
                            "capabilities": {"tools": {}},
                        },
                    }
                )
                continue

            if method in ("initialized", "notifications/initialized") or (
                    isinstance(method, str) and method.startswith("notifications/")
            ):
                # Notifications do not expect a response
                continue

            if method == "tools/list":
                _write_response(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"tools": TOOLS},
                    }
                )
                continue

            if method == "ping":
                _write_response({"jsonrpc": "2.0", "id": request_id, "result": {}})
                continue

            if method == "resources/list":
                _write_response({"jsonrpc": "2.0", "id": request_id, "result": {"resources": []}})
                continue

            if method == "prompts/list":
                _write_response({"jsonrpc": "2.0", "id": request_id, "result": {"prompts": []}})
                continue

            if method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments") or {}
                result = _handle_tools_call(tool_name, arguments)
                # Serialize result once
                result_text = json.dumps(result, ensure_ascii=False, indent=None)
                _write_response(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"content": [{"type": "text", "text": result_text}]},
                    }
                )
                continue

            if method in ("shutdown", "exit"):
                _write_response({"jsonrpc": "2.0", "id": request_id, "result": {}})
                break

            if request_id is not None:
                _write_response(_error_response(request_id, f"Unsupported method: {method}"))

        except Exception as exc:
            if request_id is not None:
                _write_response(_error_response(request_id, str(exc)))


if __name__ == "__main__":
    main()
