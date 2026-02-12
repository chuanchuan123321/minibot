<!-- Language Selection -->
<div align="center">

**[English](README.md) | [中文](README.zh.md)**

</div>

---

# Minibot - Lightweight AI Automation Tool

An ultra-lightweight AI automation tool that can execute various tasks in the terminal, including system commands, file operations, web search, URL content reading, and more.

## 🌟 Project Advantages

- **Ultra-lightweight** - Clean code, minimal dependencies, fast startup
- **24/7 Operation** - Supports long-running processes with scheduled tasks
- **Plan Work Until Completion** - AI automatically plans task steps and progressively completes complex workflows
- **Unlimited Context** - Intelligent memory compression keeps context manageable while supporting infinite task chaining
- **Flexible API Support** - Supports OpenAI, Anthropic, and other official APIs, as well as domestic API services
- **Natural Language Interaction** - Describe tasks in natural language without learning complex commands
- **Complete Toolset** - File operations, web search, document parsing, and more

## Features

✨ **Core Features**
- 🤖 Natural Language Interaction - Describe tasks in natural language
- 🔧 System Command Execution - Execute shell commands
- 📁 File Operations - Read, write, copy, move, delete files
- 📄 Document Parsing - Support PDF, Word, Markdown, JSON and other formats
- 🔍 Web Search - Search the web using Tavily API
- 🌐 URL Content Reading - Automatically extract web page content
- ⏰ Timer - Set scheduled tasks
- ✅ Command Approval - Interactive command confirmation
- 📤 **File Sending** - Send files to Feishu (Gateway Mode)
- 💬 **Feishu Integration** - Real-time task progress updates via Feishu
- 🎓 **Skill System** - Modular knowledge base with 6+ built-in skills
- 🔄 **Smart Tool Loading** - AI consciously loads skills and tools as needed

## Installation

### Install from Source

```bash
git clone https://github.com/chuanchuan123321/Minibot.git
cd Minibot
pip install -e .
```

## Demo Screenshots

![Minibot Interface](images/demo.png)

## Quick Start

### 1. Configure Environment Variables (Required)

Copy `.env.example` to `.env` and fill in your API credentials:

```bash
cp .env.example .env
```

Edit `.env` file with your API keys:

```bash
# Using OpenAI API (Recommended)
API_BASE_URL=https://api.openai.com/v1
API_KEY=sk-your_openai_api_key_here
API_MODEL=gpt-5.2

# Or use other API services (e.g., Anthropic, domestic services, etc.)
# API_BASE_URL=https://api.anthropic.com
# API_KEY=your_api_key_here
# API_MODEL=claude-sonnet-4-5-20250929

# Or use domestic API services
# API_BASE_URL=https://yunwu.ai
# API_KEY=your_api_key_here
# API_MODEL=claude-sonnet-4-5-20250929

TAVILY_API_KEY=tvly-your_tavily_api_key_here
MAX_TOKENS=4096
TEMPERATURE=0.7
```

**Supported API Services:**
- ✅ OpenAI (https://api.openai.com/v1)
- ✅ Anthropic (https://api.anthropic.com)
- ✅ Domestic API Services (e.g., yunwu.ai)
- ✅ Other OpenAI-compatible APIs

### 2. Run Minibot

```bash
python chat.py
```

Or run directly:

```bash
python chat.py
```

### 3. Gateway Mode (Feishu Integration)

Run in gateway mode to receive tasks from Feishu and send real-time updates:

```bash
python chat.py gateway
```

**Gateway Mode Features:**
- 📨 Receive tasks from Feishu
- 🤖 Real-time progress updates
- 📤 Send files directly to Feishu
- ✅ Interactive command approval via Feishu

**Setup:**
1. Configure Feishu credentials in `.env` file:
   ```bash
   FEISHU_ENABLED=true
   FEISHU_APP_ID=your_app_id
   FEISHU_APP_SECRET=your_app_secret
   ```
2. Enable Bot capability in Feishu Open Platform
3. Subscribe to `im.message.receive_v1` event
4. Run: `python chat.py gateway`

## Usage Examples

### Example 1: Search Web Information

```
You: Search for the latest AI technology developments

Next I will: Use web_search tool to search for latest AI technology

===== JSON START =====
{"action": "execute_tool", "tool": "web_search", "params": {"query": "latest AI technology 2025"}}
===== JSON END =====
```

### Example 2: Read URL Content

```
You: Read the content of this webpage https://example.com

Next I will: Use read_url tool to read web page content

===== JSON START =====
{"action": "execute_tool", "tool": "read_url", "params": {"url": "https://example.com"}}
===== JSON END =====
```

### Example 3: Set Timer

```
You: Remind me to eat in 30 minutes

Next I will: Set a 30-minute timer

===== JSON START =====
{"action": "execute_tool", "tool": "set_timer", "params": {"minutes": 30, "message": "Time to eat!"}}
===== JSON END =====
```

### Example 4: Create and Modify Configuration File

```
You: Create a config.json file with application configuration information

Next I will: Create configuration file

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/config.json", "content": "{\"app_name\": \"MyApp\", \"version\": \"1.0.0\", \"debug\": true}"}}
===== JSON END =====
```

### Example 5: Batch File Operations

```
You: Create a project structure with src, tests, docs directories, and create main.py in src

Next I will: Create project directory structure

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/project/src"}}
===== JSON END =====

Next I will: Create tests directory

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/project/tests"}}
===== JSON END =====

Next I will: Create docs directory

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/project/docs"}}
===== JSON END =====

Next I will: Create main.py file in src

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/project/src/main.py", "content": "#!/usr/bin/env python3\n\ndef main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()"}}
===== JSON END =====
```

### Example 6: Read and Modify Existing Files

```
You: Read the README.md file and add a new section to it

Next I will: Read README.md file

===== JSON START =====
{"action": "execute_tool", "tool": "file_read", "params": {"path": "/path/to/README.md"}}
===== JSON END =====

Next I will: Add new section at the end of the file

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/README.md", "content": "[Original file content]\n\n## New Section\n\nThis is the newly added section content."}}
===== JSON END =====
```

### Example 7: Complex Workflow - Generate Project Documentation

```
You: Create a complete project with source code, test files, and documentation

Next I will: Create project root directory

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/myproject"}}
===== JSON END =====

Next I will: Create source code directory

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/myproject/src"}}
===== JSON END =====

Next I will: Create Python module

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/src/__init__.py", "content": "\"\"\"MyProject Package\"\"\"\n__version__ = '1.0.0'"}}
===== JSON END =====

Next I will: Create main module

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/src/core.py", "content": "class Calculator:\n    def add(self, a, b):\n        return a + b\n    \n    def subtract(self, a, b):\n        return a - b"}}
===== JSON END =====

Next I will: Create project README

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/README.md", "content": "# MyProject\n\nA sample project\n\n## Features\n\n- Addition\n- Subtraction\n\n## Usage\n\n```python\nfrom src.core import Calculator\ncalc = Calculator()\nprint(calc.add(1, 2))\n```"}}
===== JSON END =====

Next I will: Create tests directory

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/myproject/tests"}}
===== JSON END =====

Next I will: Create test file

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/tests/test_core.py", "content": "import unittest\nfrom src.core import Calculator\n\nclass TestCalculator(unittest.TestCase):\n    def setUp(self):\n        self.calc = Calculator()\n    \n    def test_add(self):\n        self.assertEqual(self.calc.add(1, 2), 3)\n    \n    def test_subtract(self):\n        self.assertEqual(self.calc.subtract(5, 3), 2)"}}
===== JSON END =====
```

## Available Tools

| Tool Name | Description | Parameters |
|-----------|-------------|-----------|
| `shell` | Execute system commands | `command` |
| `file_read` | Read text files | `path` |
| `file_write` | Write files | `path`, `content` |
| `file_list` | List directory files | `path` |
| `file_delete` | Delete files | `path` |
| `dir_create` | Create directories | `path` |
| `dir_change` | Change working directory | `path` |
| `read_pdf` | Read PDF/Word documents | `path` |
| `read_markdown` | Read Markdown files | `path` |
| `read_json` | Read JSON files | `path` |
| `search_files` | Search for files by pattern | `pattern`, `path` |
| `get_file_info` | Get file information | `path` |
| `copy_file` | Copy files | `source`, `destination` |
| `move_file` | Move/rename files | `source`, `destination` |
| `create_file` | Create new files | `path`, `content` |
| `web_search` | Search the web | `query` |
| `read_url` | Read URL content | `url` |
| `set_timer` | Set timer | `minutes`, `message` |
| `send_file` | Send file to Feishu | `path` (Gateway Mode only) |
| `generate_pdf` | Generate PDF from documents | `input_path`, `output_path`, `format` |
| `load_skill` | Load skill's complete content | `skill_name` |

## Configuration

### API Configuration

- **API_BASE_URL**: Base URL of the AI API
- **API_KEY**: API key
- **API_MODEL**: Model name to use
- **TAVILY_API_KEY**: Tavily search API key

### Other Configuration

- **MAX_TOKENS**: Maximum number of tokens
- **TEMPERATURE**: Temperature parameter (0-1)

### Command Reference

| Command | Mode | Function |
|---------|------|----------|
| `/clear` | CLI & Gateway | Clear conversation and execution history |
| `/stop` | Gateway Mode | Stop the currently executing task |
| `Ctrl+C` | CLI | Interrupt current task |
| `exit` / `quit` | CLI | Exit the program |

## Project Structure

```
Minibot/
├── agent/
│   ├── core/
│   │   ├── ai_engine.py              # AI Engine
│   │   ├── extended_tool_executor.py # Tool Executor
│   │   ├── skills.py                 # Skills Loader
│   │   └── memory_manager.py         # Memory Manager
│   ├── tools/
│   │   ├── shell.py                  # Shell Command Tool
│   │   ├── file.py                   # File Operations Tool
│   │   ├── time_tool.py              # Timer Tool
│   │   ├── pdf_tool.py               # PDF Generation Tool
│   │   └── skill_tool.py             # Skill Loading Tool
│   ├── channels/
│   │   ├── base.py                   # Base Channel Class
│   │   ├── feishu.py                 # Feishu Integration
│   │   └── manager.py                # Channel Manager
│   ├── bus/
│   │   ├── queue.py                  # Message Queue
│   │   └── events.py                 # Event Definitions
│   ├── config/
│   │   ├── loader.py                 # Config Loader
│   │   └── schema.py                 # Config Schema
│   ├── skills/                       # Built-in Skills
│   │   ├── github/
│   │   ├── web/
│   │   ├── python/
│   │   ├── project-setup/
│   │   └── skill-creator/
│   └── ui/
│       └── cli.py                    # CLI Interface
├── Memory/
│   ├── execution_history.md          # Current task execution history
│   ├── accumulated_compression.md    # Compressed summaries of previous tasks
│   ├── index.json                    # Compression record index
│   └── YYYY-MM-DD/                   # Date-based archive folders
│       └── YYYY-MM-DD_HH-MM-SS_历史.md # Timestamped archives
├── workspace/
│   ├── output/                       # Final output files (preserved)
│   ├── temp/                         # Temporary files (auto-cleaned)
│   ├── cache/                        # Cache data
│   └── skills/                       # Custom user skills
├── images/                           # Demo screenshots
│   └── demo.png                      # Interface screenshot
├── chat.py                           # Main program
├── setup.py                          # Installation configuration
├── requirements.txt                  # Dependencies list
├── .env.example                      # Environment variables example
├── .gitignore                        # Git ignore file
├── CLAUDE.md                         # Claude Code guidance
├── LICENSE                           # MIT License
└── README.md                         # This file
```

## Memory System Architecture

Minibot features an intelligent multi-level memory system designed for efficient context management across long-running tasks:

### Memory Structure

**Three-tier storage strategy:**

1. **Current Task History** (`execution_history.md`)
   - Stores real-time execution steps of the current task
   - Records: user requests, AI responses, tool execution results
   - Appended incrementally during task execution
   - Cleared after compression

2. **Accumulated Compression** (`accumulated_compression.md`)
   - Maintains compressed summaries of all previous tasks
   - Enables AI to understand historical context
   - Grows progressively as more tasks are compressed
   - Available to all subsequent tasks

3. **Timestamped Archives** (`Memory/YYYY-MM-DD/`)
   - Permanently stores complete execution history
   - Organized by date with minute-level precision
   - Enables task history lookup and audit trails

### Memory Flow

```
Task Execution:
  1. Load accumulated_compression (previous task summaries)
  2. Append steps to execution_history as they execute
  3. AI references both for decision-making

Task Completion:
  1. Compress execution_history to summary (table format)
  2. Archive complete history with timestamp
  3. Append summary to accumulated_compression
  4. Clear execution_history for next task

Next Task:
  1. Load accumulated_compression (now includes latest summary)
  2. Start fresh execution_history
  3. Continue cycle...
```

### Key Features

- **Persistent Context** - Previous task summaries inform current decisions
- **Automatic Cleanup** - Execution history cleared after compression
- **Temporal Organization** - Archives timestamped for historical reference
- **Token Efficiency** - System prompts not stored, only user context and results
- **Scalable Design** - Supports unlimited task chaining without context loss

### Unlimited Context with Smart Compression

Minibot achieves **unlimited context capacity** through an intelligent compression mechanism:

**How It Works:**

1. **Automatic Compression** (Manual via `/compact` command)
   - When task execution history exceeds 30,000 tokens, automatic compression is triggered
   - Or manually trigger with `/compact` command at any time
   - Execution history is intelligently compressed into a concise summary table
   - Complete history is archived with timestamp for future reference

2. **Context Preservation**
   - Compressed task summaries are accumulated and maintained
   - Each new task can reference ALL previous task summaries
   - AI makes decisions informed by entire project history
   - No information loss, only reorganization for efficiency

3. **Benefits**

   | Scenario | Without Compression | With Compression |
   |----------|-------------------|------------------|
   | 10 task chain | Context overloaded | ✅ All tasks remembered |
   | 100 task chain | Impossible | ✅ Unlimited tasks supported |
   | Context per task | ~3000-4000 tokens | ✅ ~1000-1500 tokens (compressed) |
   | Historical recall | Lost after few tasks | ✅ Full project memory maintained |

**Using the `/compact` Command:**

```bash
# Manual compression (CLI mode)
> /compact
📊 近期记忆: 28,500 tokens，正在压缩...
✅ 历史记录已压缩并保存到记忆文件

# Or in Gateway Mode
> /compact
✅ 历史记录已压缩，可继续提问
```

**Result:**
- Task execution history is cleared
- Compressed summary is archived
- Previous task context is accumulated for next task
- System can handle unlimited task sequences

## Skill System

Minibot includes a powerful skill system for modular knowledge management:

### What are Skills?

Skills are reusable knowledge modules that teach AI about specific domains, tools, or best practices. Each skill contains:
- **SKILL.md** - Comprehensive guide with instructions and examples
- **scripts/** - Python/shell scripts for automation
- **data/** - CSV databases for searching and recommendations

### Built-in Skills

- **web** - Web search techniques and best practices
- **github** - GitHub CLI usage guide
- **python** - Python programming best practices
- **pdf** - PDF processing and manipulation
- **docx** - Word document creation and editing
- **ui-ux-pro-max** - UI/UX design intelligence with 50+ styles and 97 color palettes

### Using Skills

1. **View Available Skills** - AI sees all skills in the system information
2. **Load Skill** - AI calls `load_skill("skill-name")` to get detailed guidance
3. **Get Recommendations** - AI uses skill data for intelligent suggestions

### Creating Custom Skills

Create a new skill in `workspace/skills/`:

```bash
mkdir -p workspace/skills/my-skill
cat > workspace/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: "My custom skill description"
requires_bins: python
requires_env:
---

# My Skill

Detailed content and instructions...
EOF
```

### File Management

Minibot automatically manages files in organized directories:

```
workspace/
├── output/     # Final output files (preserved)
├── temp/       # Temporary files (auto-cleaned)
├── cache/      # Cache data (optional cleanup)
└── skills/     # Skill modules
```

**Rules:**
- Final output → `workspace/output/`
- Temporary files → `workspace/temp/` (auto-cleaned after task)
- Cache data → `workspace/cache/`
- System info includes all paths for AI guidance

## FAQ

### Q: How do I get an API key?

A: Depending on the API service you choose:
- **OpenAI**: Visit https://platform.openai.com/api-keys to get your API key
- **Anthropic**: Visit https://console.anthropic.com to get your API key
- **Domestic Services**: Visit https://yunwu.ai or other domestic API service providers to register

### Q: How do I get a Tavily API key?

A: Visit https://tavily.com to register and get your API key.

### Q: What file formats are supported?

A: Supports multiple file formats:
- **Documents**: PDF, Word (.docx/.doc), Excel (.xls/.xlsx), Markdown, JSON, plain text
- **Images**: JPG, JPEG, PNG, GIF, WebP, BMP (up to 10 MB, max resolution 12000x12000)
- **Media**: MP4 video, OPUS audio
- **Other**: Any binary file format (up to 30 MB)

### Q: How do I disable command approval?

A: Select the "all" option in the interactive menu to allow all commands.

### Q: Can it run 24/7?

A: Yes. Minibot supports 24-hour operation, and you can set scheduled tasks to execute work at specified times.

### Q: What API services are supported?

A: Supports any OpenAI-compatible API service, including:
- OpenAI Official API
- Anthropic API
- Domestic API Services (e.g., yunwu.ai)
- Other compatible services

## Contributing

Welcome to submit Issues and Pull Requests!

## License

MIT License - See LICENSE file for details

## Contact

Email: 2774421277@qq.com
