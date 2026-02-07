<!-- 语言选择 -->
<div align="center">

**[English](README.md) | [中文](README.zh.md)**

</div>

---

# Minibot - 轻量级 AI 自动化工具

一个超轻量级的 AI 自动化工具，可以在终端中执行各种任务，包括系统命令、文件操作、网页搜索、URL 内容读取等。

## 🌟 项目优势

- **超轻量级** - 代码简洁，依赖少，快速启动
- **24小时工作** - 支持长时间运行，可设置定时任务
- **计划工作直至完成** - AI 会自动规划任务步骤，逐步完成复杂工作流
- **灵活的 API 支持** - 支持 OpenAI、Anthropic 等官方 API，也支持国内 API 服务
- **自然语言交互** - 用自然语言描述任务，无需学习复杂命令
- **完整的工具集** - 文件操作、网页搜索、文档解析等一应俱全

## 功能特性

✨ **核心功能**
- 🤖 自然语言交互 - 用自然语言描述任务
- 🔧 系统命令执行 - 执行 shell 命令
- 📁 文件操作 - 读写、复制、移动、删除文件
- 📄 文档解析 - 支持 PDF、Word、Markdown、JSON 等格式
- 🔍 网页搜索 - 使用 Tavily API 搜索网页
- 🌐 URL 内容读取 - 自动提取网页内容
- ⏰ 定时器 - 设置定时任务
- ✅ 命令审批 - 交互式命令确认

## 安装

### 方式一：从 PyPI 安装（推荐）

```bash
pip install Minibot
```

### 方式二：从源代码安装

```bash
git clone https://github.com/yourusername/Minibot.git
cd Minibot
pip install -e .
```

## 演示截图

![Minibot 运行界面](images/demo.png)

## 快速开始

### 1. 配置环境变量

创建 `.env` 文件：

```bash
# 使用 OpenAI API（推荐）
API_BASE_URL=https://api.openai.com/v1
API_KEY=sk-your_openai_api_key_here
API_MODEL=gpt-5.2

# 或使用其他 API 服务（如 Anthropic、国内服务等）
# API_BASE_URL=https://api.anthropic.com
# API_KEY=your_api_key_here
# API_MODEL=claude-sonnet-4-5-20250929

# 或使用国内 API 服务
# API_BASE_URL=https://yunwu.ai
# API_KEY=your_api_key_here
# API_MODEL=claude-sonnet-4-5-20250929

TAVILY_API_KEY=tvly-your_tavily_api_key_here
MAX_TOKENS=4096
TEMPERATURE=0.7
```

**支持的 API 服务：**
- ✅ OpenAI (https://api.openai.com/v1)
- ✅ Anthropic (https://api.anthropic.com)
- ✅ 国内 API 服务 (如 yunwu.ai 等)
- ✅ 其他兼容 OpenAI 格式的 API

### 2. 运行 Minibot

```bash
Minibot
```

或者直接运行：

```bash
python chat.py
```

## 使用示例

### 示例 1：搜索网页信息

```
你: 搜索最新的 AI 技术发展

接下来我要: 使用 web_search 工具搜索最新 AI 技术

===== JSON START =====
{"action": "execute_tool", "tool": "web_search", "params": {"query": "latest AI technology 2024"}}
===== JSON END =====
```

### 示例 2：读取 URL 内容

```
你: 读取这个网页的内容 https://example.com

接下来我要: 使用 read_url 工具读取网页内容

===== JSON START =====
{"action": "execute_tool", "tool": "read_url", "params": {"url": "https://example.com"}}
===== JSON END =====
```

### 示例 3：设置定时器

```
你: 30分钟后提醒我吃饭

接下来我要: 设置 30 分钟的定时器

===== JSON START =====
{"action": "execute_tool", "tool": "set_timer", "params": {"minutes": 30, "message": "该吃饭了！"}}
===== JSON END =====
```

### 示例 4：创建和修改配置文件

```
你: 创建一个 config.json 文件，包含应用配置信息

接下来我要: 创建配置文件

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/config.json", "content": "{\"app_name\": \"MyApp\", \"version\": \"1.0.0\", \"debug\": true}"}}
===== JSON END =====
```

### 示例 5：批量文件操作

```
你: 创建一个项目结构，包括 src、tests、docs 三个目录，并在 src 中创建 main.py 文件

接下来我要: 创建项目目录结构

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/project/src"}}
===== JSON END =====

接下来我要: 创建 tests 目录

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/project/tests"}}
===== JSON END =====

接下来我要: 创建 docs 目录

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/project/docs"}}
===== JSON END =====

接下来我要: 在 src 中创建 main.py 文件

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/project/src/main.py", "content": "#!/usr/bin/env python3\n\ndef main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()"}}
===== JSON END =====
```

### 示例 6：读取和修改现有文件

```
你: 读取 README.md 文件，然后在其中添加一个新的章节

接下来我要: 读取 README.md 文件

===== JSON START =====
{"action": "execute_tool", "tool": "file_read", "params": {"path": "/path/to/README.md"}}
===== JSON END =====

接下来我要: 在文件末尾添加新章节

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/README.md", "content": "[原文件内容]\n\n## 新章节\n\n这是新添加的章节内容。"}}
===== JSON END =====
```

### 示例 7：复杂工作流 - 生成项目文档

```
你: 创建一个完整的项目，包括源代码、测试文件和文档

接下来我要: 创建项目根目录

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/myproject"}}
===== JSON END =====

接下来我要: 创建源代码目录

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/myproject/src"}}
===== JSON END =====

接下来我要: 创建 Python 模块

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/src/__init__.py", "content": "\"\"\"MyProject Package\"\"\"\n__version__ = '1.0.0'"}}
===== JSON END =====

接下来我要: 创建主模块

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/src/core.py", "content": "class Calculator:\n    def add(self, a, b):\n        return a + b\n    \n    def subtract(self, a, b):\n        return a - b"}}
===== JSON END =====

接下来我要: 创建项目 README

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/README.md", "content": "# MyProject\n\n一个示例项目\n\n## 功能\n\n- 加法\n- 减法\n\n## 使用方法\n\n```python\nfrom src.core import Calculator\ncalc = Calculator()\nprint(calc.add(1, 2))\n```"}}
===== JSON END =====

接下来我要: 创建测试目录

===== JSON START =====
{"action": "execute_tool", "tool": "dir_create", "params": {"path": "/path/to/myproject/tests"}}
===== JSON END =====

接下来我要: 创建测试文件

===== JSON START =====
{"action": "execute_tool", "tool": "file_write", "params": {"path": "/path/to/myproject/tests/test_core.py", "content": "import unittest\nfrom src.core import Calculator\n\nclass TestCalculator(unittest.TestCase):\n    def setUp(self):\n        self.calc = Calculator()\n    \n    def test_add(self):\n        self.assertEqual(self.calc.add(1, 2), 3)\n    \n    def test_subtract(self):\n        self.assertEqual(self.calc.subtract(5, 3), 2)"}}
===== JSON END =====
```

## 可用工具

| 工具名 | 描述 | 参数 |
|------|------|------|
| `shell` | 执行系统命令 | `command` |
| `file_read` | 读取文本文件 | `path` |
| `file_write` | 写入文件 | `path`, `content` |
| `file_list` | 列出目录文件 | `path` |
| `file_delete` | 删除文件 | `path` |
| `dir_create` | 创建目录 | `path` |
| `read_pdf` | 读取 PDF/Word 文档 | `path` |
| `read_markdown` | 读取 Markdown 文件 | `path` |
| `read_json` | 读取 JSON 文件 | `path` |
| `web_search` | 搜索网页 | `query` |
| `read_url` | 读取 URL 内容 | `url` |
| `set_timer` | 设置定时器 | `minutes`, `message` |

## 配置说明

### API 配置

- **API_BASE_URL**: AI API 的基础 URL
- **API_KEY**: API 密钥
- **API_MODEL**: 使用的模型名称
- **TAVILY_API_KEY**: Tavily 搜索 API 密钥

### 其他配置

- **MAX_TOKENS**: 最大 token 数
- **TEMPERATURE**: 温度参数（0-1）

## 命令行选项

```bash
# 显示帮助信息
Minibot --help

# 指定配置文件
Minibot --config /path/to/.env

# 运行特定任务
Minibot "你的任务描述"
```

## 项目结构

```
Minibot/
├── agent/
│   ├── core/
│   │   ├── ai_engine.py          # AI 引擎
│   │   └── extended_tool_executor.py  # 工具执行器
│   ├── tools/
│   │   ├── shell.py              # Shell 工具
│   │   └── file.py               # 文件工具
│   └── ui/
│       └── cli.py                # CLI 界面
├── images/                        # 演示截图文件夹
│   └── demo.png                  # 运行界面截图
├── tests/                         # 测试文件
│   └── test_agent.py
├── chat.py                        # 主程序
├── setup.py                       # 安装配置
├── requirements.txt               # 依赖列表
├── .env.example                   # 环境变量示例
├── .gitignore                     # Git 忽略文件
└── README.md                      # 本文件
```

## 常见问题

### Q: 如何获取 API 密钥？

A: 根据你选择的 API 服务获取：
- **OpenAI**: 访问 https://platform.openai.com/api-keys 获取 API 密钥
- **Anthropic**: 访问 https://console.anthropic.com 获取 API 密钥
- **国内服务**: 访问 https://yunwu.ai 或其他国内 API 服务商注册获取

### Q: 如何获取 Tavily API 密钥？

A: 访问 https://tavily.com 注册并获取 API 密钥。

### Q: 支持哪些文件格式？

A: 支持 PDF、Word (.docx/.doc)、Markdown、JSON、纯文本等格式。

### Q: 如何禁用命令审批？

A: 在交互式菜单中选择 "all" 选项，允许所有命令。

### Q: 可以长时间运行吗？

A: 可以。Minibot 支持 24 小时运行，你可以设置定时任务让它在指定时间执行工作。

### Q: 支持哪些 API 服务？

A: 支持任何兼容 OpenAI API 格式的服务，包括：
- OpenAI 官方 API
- Anthropic API
- 国内 API 服务（如 yunwu.ai）
- 其他兼容服务

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 LICENSE 文件

## 作者

chuan (2774421277@qq.com)

## 更新日志

### v1.0.0 (2024-02-07)
- 初始版本发布
- 支持基本的任务执行
- 集成网页搜索和 URL 读取
- 添加定时器功能
