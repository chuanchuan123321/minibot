# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Minibot** is a lightweight AI automation tool that executes tasks through natural language interaction. It acts as an AI agent that can execute system commands, file operations, web searches, document parsing, and more. The tool uses an iterative step-based approach where the AI engine decides what action to take next until the task is complete.

## Architecture

### Core Components

1. **AIEngine** (`agent/core/ai_engine.py`)
   - Handles API communication with OpenAI-compatible services (OpenAI, Anthropic, domestic services)
   - Manages conversation history and message formatting
   - Supports configurable models, tokens, and temperature via environment variables
   - Sends prompts to the API and receives responses

2. **ExtendedToolExecutor** (`agent/core/extended_tool_executor.py`)
   - Central tool dispatcher that executes all available tools
   - Manages 19+ tools including shell commands, file operations, document reading, web search, timers, and file sending
   - Returns structured results from tool execution

3. **NaturalTaskExecutor** (`chat.py`)
   - Main orchestrator that coordinates the AI engine and tool executor
   - Implements iterative step-based task execution (up to 100 steps max)
   - Builds context from execution history
   - Handles command approval workflow and timer management

4. **Tool Implementations**
   - `agent/tools/shell.py`: Shell command execution with safety checks (blocks dangerous patterns)
   - `agent/tools/file.py`: File operations (read, write, delete, copy, move, list, search)
   - `agent/tools/time_tool.py`: Timer and time-related utilities

5. **CLI Interface** (`agent/ui/cli.py`)
   - User interaction layer for command approval and task input

### Execution Flow

1. User provides a task description
2. NaturalTaskExecutor builds context from previous steps
3. AIEngine receives a prompt describing available tools and current step
4. AI responds with natural language description + JSON action
5. ExtendedToolExecutor executes the specified tool
6. Result is added to execution history
7. Process repeats until task is complete or max steps reached

## Common Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python chat.py

# Run tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_agent.py::TestAIEngine::test_add_message

# Install in development mode
pip install -e .

# Run as command-line tool (after installation)
minibot "Your task description"
```

## Environment Configuration

Create a `.env` file with:

```
API_BASE_URL=https://api.openai.com/v1
API_KEY=your_api_key_here
API_MODEL=gpt-4
TAVILY_API_KEY=your_tavily_key_here
MAX_TOKENS=4096
TEMPERATURE=0.7

# Feishu Configuration (Optional)
FEISHU_ENABLED=false
FEISHU_APP_ID=your_feishu_app_id
FEISHU_APP_SECRET=your_feishu_app_secret
```

Supported API services:
- OpenAI (https://api.openai.com/v1)
- Anthropic (https://api.anthropic.com)
- Domestic services (e.g., yunwu.ai)
- Any OpenAI-compatible API

## Key Implementation Details

### Tool System

Tools are registered in `ExtendedToolExecutor.tools` dictionary and must:
- Accept parameters as a dictionary
- Return a tuple of (success: bool, result: str)
- Be listed in `get_available_tools()` for AI visibility

### Step-Based Execution

The system uses a step counter (`self.step_count`) to track progress and prevent infinite loops. Each step:
1. Builds a prompt with current context and available tools
2. Calls the AI engine to decide next action
3. Executes the tool and captures results
4. Increments step counter
5. Repeats until task completion or max steps (100) reached

### Command Approval

The `allow_all_commands` flag controls whether commands require user approval. When False, users are prompted to approve shell commands before execution.

### File Sending (Gateway Mode)

The `send_file` tool allows the AI to send files to users through Feishu in gateway mode:
- **Availability**: Only works in gateway mode (when running with `python chat.py gateway`)
- **Usage**: AI can use `send_file` tool with a file path parameter
- **Implementation**:
  - `_send_file_to_channel()` in `chat.py` handles file sending
  - Feishu channel (`agent/channels/feishu.py`) automatically detects file paths and uploads them
  - Files are uploaded to Feishu's file storage and sent as file messages
- **Example**: When AI needs to send a report or generated file, it calls:
  ```json
  {"action": "execute_tool", "tool": "send_file", "params": {"path": "/path/to/file.txt"}}
  ```

### Document Reading

The `read_pdf` tool handles multiple document formats (.pdf, .docx, .doc) using document parsing libraries. It's prioritized in prompts for document-related tasks.

## Testing

Tests are located in `tests/test_agent.py` and cover:
- AIEngine message handling and history
- ShellTool command execution
- FileTool file operations

Run tests with: `python -m pytest tests/ -v`

## Important Notes

- The system has built-in safety checks in ShellTool that block dangerous commands (rm -rf /, fork bombs, etc.)
- Path expansion supports Chinese aliases (桌面 → Desktop, 文档 → Documents, etc.)
- Web search requires a Tavily API key
- The tool executor has a 30-second timeout for shell commands
- Maximum output length for shell commands is 5000 characters
