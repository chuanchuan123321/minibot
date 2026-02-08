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

### 1. Configure Environment Variables

Create a `.env` file:

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
Minibot
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
| `read_pdf` | Read PDF/Word documents | `path` |
| `read_markdown` | Read Markdown files | `path` |
| `read_json` | Read JSON files | `path` |
| `web_search` | Search the web | `query` |
| `read_url` | Read URL content | `url` |
| `set_timer` | Set timer | `minutes`, `message` |
| `send_file` | Send file to Feishu | `path` (Gateway Mode only) |

## Configuration

### API Configuration

- **API_BASE_URL**: Base URL of the AI API
- **API_KEY**: API key
- **API_MODEL**: Model name to use
- **TAVILY_API_KEY**: Tavily search API key

### Other Configuration

- **MAX_TOKENS**: Maximum number of tokens
- **TEMPERATURE**: Temperature parameter (0-1)

## Command Line Options

```bash
# Show help information
Minibot --help

# Specify configuration file
Minibot --config /path/to/.env

# Run specific task
Minibot "Your task description"

# Clear conversation history
/clear

# Stop current task (Gateway mode only)
/stop
```

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
│   │   ├── ai_engine.py          # AI Engine
│   │   └── extended_tool_executor.py  # Tool Executor
│   ├── tools/
│   │   ├── shell.py              # Shell Tool
│   │   ├── file.py               # File Tool
│   │   ├── time_tool.py          # Time Tool
│   │   └── pdf_tool.py           # PDF Generation Tool
│   ├── channels/
│   │   ├── base.py               # Base Channel
│   │   ├── feishu.py             # Feishu Integration
│   │   └── manager.py            # Channel Manager
│   ├── bus/
│   │   ├── queue.py              # Message Queue
│   │   └── events.py             # Event Definitions
│   ├── config/
│   │   ├── loader.py             # Config Loader
│   │   └── schema.py             # Config Schema
│   └── ui/
│       └── cli.py                # CLI Interface
├── images/                        # Demo screenshots folder
│   └── demo.png                  # Interface screenshot
├── chat.py                        # Main program
├── setup.py                       # Installation configuration
├── requirements.txt               # Dependencies list
├── .env.example                   # Environment variables example
├── .gitignore                     # Git ignore file
├── LICENSE                        # MIT License
└── README.md                      # This file
```

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

## Changelog

### v1.1.0 (2025-02-08)
- ✨ Added file sending to Feishu (Gateway Mode)
- ✨ Added image upload support (JPG, PNG, GIF, WebP, BMP)
- ✨ Real-time task progress updates via Feishu
- ✨ Added `/clear` command to clear conversation history
- 🐛 Improved JSON parsing with better quote handling
- 🐛 Fixed terminal UI scrolling issue in approval menu
- 📝 Updated documentation

### v1.0.0 (2025-02-07)
- Initial release
- Support basic task execution
- Integrated web search and URL reading
- Added timer functionality
