# Minibot - 轻量级 AI 自动化工具

一个轻量级的 AI 自动化工具，可以在终端中执行各种任务，包括系统命令、文件操作、网页搜索、URL 内容读取等。

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

## 快速开始

### 1. 配置环境变量

创建 `.env` 文件：

```bash
API_BASE_URL=https://yunwu.ai
API_KEY=your_api_key_here
API_MODEL=claude-haiku-4-5-20251001
TAVILY_API_KEY=your_tavily_api_key_here
MAX_TOKENS=4096
TEMPERATURE=0.7
```

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
├── chat.py                        # 主程序
├── setup.py                       # 安装配置
├── requirements.txt               # 依赖列表
├── .env.example                   # 环境变量示例
└── README.md                      # 本文件
```

## 常见问题

### Q: 如何获取 API 密钥？

A: 访问 https://yunwu.ai 注册账户并获取 API 密钥。

### Q: 如何获取 Tavily API 密钥？

A: 访问 https://tavily.com 注册并获取 API 密钥。

### Q: 支持哪些文件格式？

A: 支持 PDF、Word (.docx/.doc)、Markdown、JSON、纯文本等格式。

### Q: 如何禁用命令审批？

A: 在交互式菜单中选择 "all" 选项，允许所有命令。

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
