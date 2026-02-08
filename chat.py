#!/usr/bin/env python3
"""Minibot - 轻量级 AI 自动化工具"""
import sys
sys.path.insert(0, '/Users/a1-6/Desktop/AI智能体')

# 修复macOS终端UTF-8输入问题
import os
import locale
os.environ['PYTHONIOENCODING'] = 'utf-8'
locale.setlocale(locale.LC_ALL, '')

from agent.core.ai_engine import AIEngine
from agent.core.extended_tool_executor import ExtendedToolExecutor
from agent.bus.queue import MessageBus
from agent.bus.events import OutboundMessage
from agent.channels.manager import ChannelManager
from agent.config.loader import load_config
import json
import asyncio


class NaturalTaskExecutor:
    """Execute tasks with natural conversational flow"""

    def __init__(self, bus: MessageBus | None = None):
        self.ai_engine = AIEngine()
        self.tool_executor = ExtendedToolExecutor()
        self.available_tools = self.tool_executor.get_available_tools()
        self.execution_history = []
        self.step_count = 0
        self.max_steps = 100
        self.allow_all_commands = False  # 是否允许所有命令
        self.timer_triggered = False  # 定时器是否被触发
        self.waiting_for_timer = False  # 是否在等待定时器
        self.bus = bus  # 消息总线（用于网关模式）
        self.current_sender_id = None  # 当前消息发送者
        self.current_chat_id = None  # 当前聊天 ID
        self.current_channel = None  # 当前通道
        self.is_gateway_mode = bus is not None  # 是否在网关模式
        self.waiting_for_approval = False  # 是否在等待用户确认
        self.approval_response = None  # 用户的确认响应
        self.pending_decision = None  # 待执行的决策
        self.pending_user_request = None  # 待执行的用户请求
        self.pending_context = None  # 待执行的上下文
        self.should_stop = False  # 是否应该停止当前任务

    def execute_task(self, user_request: str):
        """Execute task dynamically with natural flow"""
        # Check for clear command
        if user_request.lower().strip() == "/clear":
            self._clear_history()
            return

        # Build context from execution history
        context = self._build_context()

        # First step: Decide what to do
        self.step_count = 1
        self._execute_step(user_request, context)

    def _execute_step(self, user_request: str, context: str):
        """Execute a single step with natural description"""
        # 检查是否应该停止任务
        if self.should_stop:
            print(f"\n⏹️  任务已停止。\n")
            self.should_stop = False
            return

        if self.step_count > self.max_steps:
            print(f"\n⚠️  已达到最大步数限制({self.max_steps})，任务停止。\n")
            return

        # Get current time
        from agent.tools.time_tool import TimeTool
        current_time = TimeTool.get_current_time()

        # Build the prompt for this step
        step_prompt = f"""【系统信息】
当前时间: {current_time}
步骤: {self.step_count}/{self.max_steps}

任务: {user_request}

{context}

可用工具:
- shell: 执行系统命令
- file_read: 读取文本文件
- file_write: 写入文件
- file_list: 列出目录文件
- file_delete: 删除文件
- dir_create: 创建目录
- dir_change: 切换目录
- read_pdf: 读取PDF文件内容（支持.pdf, .docx等文档格式）
- read_markdown: 读取Markdown文件
- read_json: 读取JSON文件
- search_files: 搜索文件
- get_file_info: 获取文件信息
- copy_file: 复制文件
- move_file: 移动文件
- create_file: 创建文件
- web_search: 搜索网页信息
- read_url: 读取URL内容
- set_timer: 设置定时器（在指定分钟后触发）
- send_file: 发送文件到飞书（仅在网关模式下可用）
- generate_pdf: 将 Markdown/文本/HTML/Word 文档转换为 PDF

重要提示:
- 如果任务涉及阅读文档（.pdf, .docx, .doc等），优先使用 read_pdf 工具
- read_pdf 工具可以处理多种文档格式，包括Word文档
- 如果任务涉及生成 PDF，使用 generate_pdf 工具（支持 markdown/text/html/docx 格式）
- 如果任务还未完成，必须继续执行下一步
- 只有当任务真正完成时才给出最终回应
- 如果找到了任务所需的信息，使用它来进行下一步
- 如果需要发送文件给用户，使用 send_file 工具（仅在网关模式下可用）

你需要用自然语言描述接下来要做什么，然后给出JSON对象。

格式如下:
接下来我要: [自然语言描述你要做什么]

===== JSON START =====
{{"action": "execute_tool", "tool": "tool_name", "params": {{"param1": "value1"}}}}
===== JSON END =====

或者:
接下来我要: [自然语言描述]

===== JSON START =====
{{"action": "respond", "response": "最终答案"}}
===== JSON END =====

例如:
接下来我要: 读取Word文档的内容

===== JSON START =====
{{"action": "execute_tool", "tool": "read_pdf", "params": {{"path": "/Users/a1-6/Desktop/SuperAgent总纲(2).docx"}}}}
===== JSON END =====

重要: 必须使用 ===== JSON START ===== 和 ===== JSON END ===== 来包围JSON对象！

现在开始，先用自然语言描述接下来要做什么，然后给出JSON对象。"""

        response = self.ai_engine.call_api(step_prompt)

        # 显示AI的回答
        print(response)

        # 提取自然语言部分并发送到飞书
        natural_language = self._extract_natural_language(response)
        if natural_language and self.is_gateway_mode:
            # 使用 ensure_future 而不是 create_task 来避免 context 冲突
            asyncio.ensure_future(self._send_to_channel(f"🤖 {natural_language}"))

        # 尝试解析JSON，如果失败则重试
        decision = self._parse_json_response(response, max_retries=2)

        if decision is None:
            # 如果多次重试都失败，继续下一步而不是停止
            print(f"\n⚠️  无法解析响应，继续下一步...\n")
            self.step_count += 1
            context = self._build_context()
            self._execute_step(user_request, context)
            return

        action = decision.get("action")

        # Handle different actions
        if action == "execute_tool":
            # 如果不是允许所有命令，则询问用户
            if not self.allow_all_commands:
                if self.is_gateway_mode:
                    # 网关模式：发送确认请求到飞书，并等待用户回复
                    tool_name = decision.get("tool", "unknown")
                    params = decision.get("params", {})
                    action_desc = self._get_action_description(tool_name, params)

                    approval_msg = f"""
⚠️ 【需要确认】

AI 想要执行以下操作：
{action_desc}

请在飞书中回复：
- "yes" 或 "y" - 执行此命令
- "all" 或 "a" - 允许本任务所有命令
- "no" 或 "n" - 取消此命令
"""
                    # 发送到飞书
                    if self.bus and self.current_channel and self.current_chat_id:
                        msg = OutboundMessage(
                            channel=self.current_channel,
                            chat_id=self.current_chat_id,
                            content=approval_msg,
                        )
                        asyncio.ensure_future(self.bus.publish_outbound(msg))

                    # 保存待执行的决策和上下文
                    self.pending_decision = decision
                    self.pending_user_request = user_request
                    self.pending_context = context

                    # 设置等待标志，暂停执行
                    print(f"⏳ 等待用户在飞书中确认...\n")
                    self.waiting_for_approval = True
                    self.approval_response = None
                    return
                else:
                    # CLI 模式：使用箭头键选择
                    approval = self._ask_for_approval()

                    if approval == "no":
                        print(f"❌ 已取消此命令\n")
                        self.step_count += 1
                        context = self._build_context()
                        self._execute_step(user_request, context)
                        return
                    elif approval == "all":
                        self.allow_all_commands = True
                        print(f"✅ 已允许本任务所有命令\n")

            self._handle_tool_execution(decision)
            # Continue to next step
            self.step_count += 1
            context = self._build_context()
            self._execute_step(user_request, context)

        elif action == "respond":
            response_text = decision.get("response", "")
            print(f"\n{response_text}\n")
            self.execution_history.append(f"最终回应: {response_text}")

            # 清理大型搜索结果以节省上下文
            self._cleanup_large_results()

            # 如果在网关模式下，发送回复到消息总线
            if self.bus and self.current_channel and self.current_chat_id:
                asyncio.ensure_future(self._send_to_channel(response_text))

        else:
            print(f"\n⚠️  未知操作: {action}，继续下一步...\n")
            self.step_count += 1
            context = self._build_context()
            self._execute_step(user_request, context)

    async def _execute_step_async(self, user_request: str, context: str):
        """Async wrapper for _execute_step to avoid nested asyncio issues"""
        self._execute_step(user_request, context)

    def _truncate_response(self, response: str, max_length: int = 50) -> str:
        """截断长响应，超过max_length的部分用省略号表示"""
        if len(response) <= max_length:
            return response

        # 找到第max_length个字符的位置
        truncated = response[:max_length]

        # 如果截断位置在JSON标记中间，需要特殊处理
        if "===== JSON START =====" in response:
            # 分别处理自然语言部分和JSON部分
            parts = response.split("===== JSON START =====")
            if len(parts) == 2:
                natural_part = parts[0]
                json_part = "===== JSON START =====" + parts[1]

                # 截断自然语言部分
                if len(natural_part) > max_length:
                    natural_part = natural_part[:max_length] + "...\n"

                # JSON部分保持原样（因为需要解析）
                return natural_part + json_part

        return truncated + "..."

    def _extract_natural_language(self, response: str) -> str:
        """从AI响应中提取自然语言部分"""
        try:
            # 查找 JSON 标记
            start_marker = "===== JSON START ====="
            start_idx = response.find(start_marker)

            if start_idx > 0:
                # 提取 JSON 标记之前的内容
                natural_part = response[:start_idx].strip()
                # 移除 "接下来我要: " 前缀
                if natural_part.startswith("接下来我要:"):
                    natural_part = natural_part[len("接下来我要:"):].strip()
                return natural_part
            else:
                # 如果没有 JSON 标记，返回整个响应
                return response.strip()
        except Exception:
            return ""

    def _parse_json_response(self, response: str, max_retries: int = 2) -> dict:
        """尝试解析JSON响应，失败时重试"""
        import re

        for attempt in range(max_retries):
            try:
                # 首先尝试使用分隔符提取JSON
                start_marker = "===== JSON START ====="
                end_marker = "===== JSON END ====="

                start_idx = response.find(start_marker)
                end_idx = response.find(end_marker)

                if start_idx >= 0 and end_idx > start_idx:
                    # 使用分隔符提取JSON
                    json_str = response[start_idx + len(start_marker):end_idx].strip()
                else:
                    # 备选方案：查找 { 和 }
                    start_idx = response.find('{')
                    end_idx = response.rfind('}') + 1

                    if start_idx < 0 or end_idx <= start_idx:
                        if attempt == max_retries - 1:
                            print(f"⚠️  无法找到JSON对象")
                        continue

                    json_str = response[start_idx:end_idx]

                # 尝试修复常见的JSON问题
                json_str = json_str.replace('\n', ' ')  # 移除换行符
                json_str = json_str.replace('\r', '')   # 移除回车符

                # 移除可能的代码块标记
                if json_str.startswith('```'):
                    json_str = json_str[3:]
                if json_str.endswith('```'):
                    json_str = json_str[:-3]
                json_str = json_str.strip()

                # 首先尝试直接解析
                try:
                    decision = json.loads(json_str)
                    return decision
                except json.JSONDecodeError as e:
                    # 如果失败，尝试修复常见问题
                    error_pos = e.pos if hasattr(e, 'pos') else 0

                    # 修复策略1：处理未转义的引号（在字符串值中）
                    # 查找 "response": " 后面的内容，转义其中的引号
                    json_str = re.sub(
                        r'("response"\s*:\s*")((?:[^"\\]|\\.)*?)(")',
                        lambda m: m.group(1) + m.group(2).replace('"', '\\"') + m.group(3),
                        json_str
                    )

                    try:
                        decision = json.loads(json_str)
                        return decision
                    except json.JSONDecodeError:
                        # 修复策略2：处理 HTML 内容中的引号
                        json_str = re.sub(r'(?<=[a-zA-Z0-9])"(?=[a-zA-Z0-9=])', '\\"', json_str)

                        decision = json.loads(json_str)
                        return decision

            except json.JSONDecodeError as e:
                if attempt == max_retries - 1:
                    print(f"⚠️  JSON解析错误: {str(e)}")
                    print(f"原始响应: {response[:300]}...")
                continue
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"⚠️  错误: {e}")
                continue

        return None

    def _handle_tool_execution(self, decision: dict):
        """Execute a tool"""
        tool_name = decision.get("tool")
        params = decision.get("params", {})

        # 如果是设置定时器，传入执行器引用
        if tool_name == "set_timer":
            params["executor"] = self
            self.waiting_for_timer = True
            self.timer_triggered = False

        # 如果是发送文件，在网关模式下处理
        if tool_name == "send_file":
            if self.is_gateway_mode and self.bus and self.current_channel and self.current_chat_id:
                file_path = params.get("path", "")
                result = self._send_file_to_channel(file_path)
            else:
                result = "❌ send_file 工具仅在网关模式下可用"
            print(f"\n执行结果:\n{result}\n")
            self.execution_history.append(f"执行 {tool_name}: {result}")
            return

        # Execute the tool
        tool_call = {"tool": tool_name, "params": params}
        result = self.tool_executor.execute(tool_call)

        # 显示执行结果
        print(f"\n执行结果:\n{result}\n")

        # Record in history - 保存完整结果
        self.execution_history.append(f"执行 {tool_name}: {result}")

        # 如果设置了定时器，等待其触发
        if tool_name == "set_timer" and self.waiting_for_timer:
            print("⏳ 等待定时器触发...\n")
            import time
            while self.waiting_for_timer and not self.timer_triggered:
                time.sleep(0.5)
            print("✅ 定时器已触发，继续执行任务\n")

    def _ask_for_approval(self) -> str:
        """Ask user for approval to execute command with arrow keys"""
        options = ['yes', 'all', 'no']
        selected = 0  # 默认选中第一个选项
        first_display = True

        while True:
            try:
                # 显示选项
                display = "[yes/all/no] 允许执行? "
                for i, opt in enumerate(options):
                    if i == selected:
                        display += f"[{opt}] "  # 当前选中的选项用方括号
                    else:
                        display += f" {opt}  "

                if first_display:
                    print(display, end="", flush=True)
                    first_display = False
                else:
                    # 使用 ANSI 转义序列清除当前行并重新打印
                    sys.stdout.write("\r\033[K" + display)
                    sys.stdout.flush()

                # 获取用户输入
                import sys
                import tty
                import termios

                # 保存终端设置
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)

                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)

                    if ch == '\x1b':  # ESC序列
                        next1 = sys.stdin.read(1)
                        if next1 == '[':
                            next2 = sys.stdin.read(1)
                            if next2 == 'C':  # 右箭头
                                selected = (selected + 1) % len(options)
                            elif next2 == 'D':  # 左箭头
                                selected = (selected - 1) % len(options)
                            elif next2 == 'A':  # 上箭头
                                selected = (selected - 1) % len(options)
                            elif next2 == 'B':  # 下箭头
                                selected = (selected + 1) % len(options)
                    elif ch == '\r' or ch == '\n':  # 回车
                        print()  # 换行
                        return options[selected]
                    elif ch.lower() == 'y':  # 快捷键 y
                        print()
                        return 'yes'
                    elif ch.lower() == 'a':  # 快捷键 a
                        print()
                        return 'all'
                    elif ch.lower() == 'n':  # 快捷键 n
                        print()
                        return 'no'
                    elif ch == 'q' or ch == '\x03':  # q 或 Ctrl+C
                        print()
                        return 'no'

                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            except KeyboardInterrupt:
                print("\n⚠️  已取消\n")
                return "no"
            except Exception as e:
                print(f"\n错误: {e}")
                return "no"

    def _get_action_description(self, tool_name: str, params: dict) -> str:
        """Get natural description of the action"""
        descriptions = {
            "file_list": f"列出 {params.get('path', '当前目录')} 中的文件",
            "file_read": f"读取文件 {params.get('path')}",
            "file_write": f"写入文件 {params.get('path')}",
            "file_delete": f"删除文件 {params.get('path')}",
            "dir_create": f"创建目录 {params.get('path')}",
            "dir_change": f"切换到目录 {params.get('path')}",
            "shell": f"执行命令: {params.get('command', '')[:50]}",
            "read_pdf": f"读取PDF文件 {params.get('path')}",
            "read_markdown": f"读取Markdown文件 {params.get('path')}",
            "read_json": f"读取JSON文件 {params.get('path')}",
            "search_files": f"搜索文件 {params.get('pattern')}",
            "get_file_info": f"获取文件信息 {params.get('path')}",
            "copy_file": f"复制文件 {params.get('source')} 到 {params.get('destination')}",
            "move_file": f"移动文件 {params.get('source')} 到 {params.get('destination')}",
            "create_file": f"创建文件 {params.get('path')}",
            "send_file": f"发送文件到飞书 {params.get('path')}",
        }
        return descriptions.get(tool_name, f"执行 {tool_name}")

    def _get_result_description(self, tool_name: str, result: str) -> str:
        """Get natural description of the result"""
        # Truncate long results
        if len(result) > 500:
            result_preview = result[:500] + "..."
        else:
            result_preview = result

        if "Error" in result or "错误" in result:
            return f"出现错误: {result_preview}"
        elif "Success" in result or "成功" in result or "created" in result or "已创建" in result:
            return f"成功完成。{result_preview}"
        else:
            return f"得到结果: {result_preview}"

    def _build_context(self) -> str:
        """Build context from execution history"""
        if not self.execution_history:
            return "还没有执行任何步骤。"

        context = "之前的执行过程:\n"
        # 保留完整的执行历史，不截断
        for entry in self.execution_history[-10:]:  # Keep last 10 steps
            context += f"- {entry}\n"

        return context

    def _cleanup_large_results(self) -> None:
        """Clean up large results from web_search and read_url to reduce context size"""
        cleaned_history = []
        for entry in self.execution_history:
            # Check if this is a web_search or read_url result
            if "执行 web_search:" in entry or "执行 read_url:" in entry:
                # Extract tool name and result
                if "执行 web_search:" in entry:
                    tool_name = "web_search"
                    prefix = "执行 web_search:"
                else:
                    tool_name = "read_url"
                    prefix = "执行 read_url:"

                result = entry[len(prefix):].strip()

                # If result is very long (> 500 chars), truncate it
                if len(result) > 500:
                    # Keep only first 200 chars as summary
                    summary = result[:200] + "... [内容已截断以节省上下文]"
                    cleaned_history.append(f"{prefix} {summary}")
                else:
                    cleaned_history.append(entry)
            else:
                cleaned_history.append(entry)

        self.execution_history = cleaned_history

    def _clear_history(self) -> None:
        """Clear conversation history and execution history"""
        # Clear AI engine history
        self.ai_engine.clear_history()

        # Clear execution history
        self.execution_history = []

        # Reset step counter
        self.step_count = 0

        # Reset command approval state
        self.allow_all_commands = False

        print("✅ 历史会话已清除\n")

    def _send_file_to_channel(self, file_path: str) -> str:
        """Send file to channel via message bus."""
        if not self.bus or not self.current_channel or not self.current_chat_id:
            return "❌ 无法发送文件：消息总线未初始化"

        try:
            import os
            from pathlib import Path

            # Expand path
            expanded_path = os.path.expanduser(file_path)
            if not expanded_path.startswith("/"):
                expanded_path = os.path.expanduser("~") + "/" + expanded_path

            if not os.path.isfile(expanded_path):
                return f"❌ 文件不存在: {file_path}"

            file_size = os.path.getsize(expanded_path)
            file_name = os.path.basename(expanded_path)

            # Create OutboundMessage with file path
            # The Feishu channel will detect it's a file and handle it
            msg = OutboundMessage(
                channel=self.current_channel,
                chat_id=self.current_chat_id,
                content=expanded_path,  # Pass the full file path
            )

            # Send asynchronously
            asyncio.ensure_future(self.bus.publish_outbound(msg))

            return f"✅ 文件已发送: {file_name} ({file_size} bytes)"
        except Exception as e:
            return f"❌ 发送文件出错: {str(e)}"

    async def _send_to_channel(self, content: str) -> None:
        """Send response to channel via message bus."""
        if not self.bus or not self.current_channel or not self.current_chat_id:
            return

        try:
            msg = OutboundMessage(
                channel=self.current_channel,
                chat_id=self.current_chat_id,
                content=content,
            )
            await self.bus.publish_outbound(msg)
        except Exception as e:
            print(f"❌ Error sending message to channel: {e}")


def get_user_input(prompt: str = "你: ") -> str:
    """Get user input with proper UTF-8 handling for macOS"""
    try:
        # 对于macOS，使用更简单的方法
        import sys
        sys.stdout.write(prompt)
        sys.stdout.flush()

        # 直接读取，不使用readline
        line = sys.stdin.readline()
        if line:
            return line.rstrip('\n\r')
        return ""
    except KeyboardInterrupt:
        return "exit"
    except EOFError:
        return "exit"


async def gateway_mode():
    """Run Minibot in gateway mode with multiple channels."""
    # Fix event loop issue for lark-oapi WebSocket client
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        print("⚠️  nest_asyncio not installed, some asyncio warnings may appear")
        pass

    # Suppress asyncio warnings
    import warnings
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    warnings.filterwarnings('ignore', message='.*cannot enter context.*')

    print("\n🚀 启动 Minibot 网关模式...\n")

    # Load configuration
    config = load_config()

    # Check if any channels are enabled
    if not config.channels.feishu.enabled:
        print("❌ 没有启用任何通道。请在配置文件中启用至少一个通道。")
        print(f"📝 配置文件位置: ~/.minibot/config.json")
        return

    # Create message bus
    bus = MessageBus()

    # Create channel manager
    channel_manager = ChannelManager(config, bus)

    # Create executor with bus
    executor = NaturalTaskExecutor(bus=bus)

    # Start channels and message processing
    async def process_messages():
        """Process inbound messages from channels."""
        while True:
            try:
                # Wait for inbound message with timeout
                msg = await asyncio.wait_for(bus.consume_inbound(), timeout=1.0)

                print(f"\n{'='*60}")
                print(f"📨 【收到飞书消息】")
                print(f"发送者: {msg.sender_id}")
                print(f"内容: {msg.content}")
                print(f"{'='*60}\n")

                # 检查是否在等待用户确认
                if executor.waiting_for_approval:
                    print(f"✅ 【收到用户确认】\n")
                    response = msg.content.lower().strip()

                    if response in ['yes', 'y']:
                        print(f"✅ 用户同意执行命令\n")
                        executor.waiting_for_approval = False
                        executor.approval_response = "yes"

                        # 执行待执行的命令
                        if executor.pending_decision:
                            print(f"🤖 【继续执行命令】\n")
                            decision = executor.pending_decision

                            # 执行工具
                            executor._handle_tool_execution(decision)

                            # 继续下一步 - 使用ensure_future避免嵌套asyncio问题
                            executor.step_count += 1
                            context = executor._build_context()
                            asyncio.ensure_future(executor._execute_step_async(executor.pending_user_request, context))

                            executor.pending_decision = None
                            executor.pending_user_request = None
                            executor.pending_context = None
                        continue

                    elif response in ['all', 'a']:
                        print(f"✅ 用户允许所有命令\n")
                        executor.allow_all_commands = True
                        executor.waiting_for_approval = False
                        executor.approval_response = "all"

                        # 执行待执行的命令
                        if executor.pending_decision:
                            print(f"🤖 【继续执行命令】\n")
                            decision = executor.pending_decision
                            executor._handle_tool_execution(decision)
                            executor.step_count += 1
                            context = executor._build_context()
                            asyncio.ensure_future(executor._execute_step_async(executor.pending_user_request, context))

                            executor.pending_decision = None
                            executor.pending_user_request = None
                            executor.pending_context = None
                        continue

                    elif response in ['no', 'n']:
                        print(f"❌ 用户拒绝执行命令\n")
                        executor.waiting_for_approval = False
                        executor.approval_response = "no"
                        executor.pending_decision = None
                        executor.pending_user_request = None
                        executor.pending_context = None

                        # 发送拒绝消息
                        reject_msg = OutboundMessage(
                            channel=msg.channel,
                            chat_id=msg.sender_id,
                            content="❌ 命令已取消",
                        )
                        await bus.publish_outbound(reject_msg)
                        continue
                    else:
                        # 无效的回复
                        invalid_msg = OutboundMessage(
                            channel=msg.channel,
                            chat_id=msg.sender_id,
                            content="⚠️ 无效的回复，请回复 yes/all/no",
                        )
                        await bus.publish_outbound(invalid_msg)
                        continue

                # 正常处理消息
                # Store message context
                executor.current_sender_id = msg.sender_id
                executor.current_chat_id = msg.chat_id
                executor.current_channel = msg.channel

                # Check for /clear command
                if msg.content.lower().strip() == "/clear":
                    executor._clear_history()
                    await executor._send_to_channel("✅ 历史会话已清除")
                    continue

                # Check for /stop command
                if msg.content.lower().strip() == "/stop":
                    executor.should_stop = True
                    executor.waiting_for_approval = False
                    executor.pending_decision = None
                    await executor._send_to_channel("⏹️ 任务已停止")
                    continue

                # Reset execution state for new message
                executor.execution_history = []
                executor.step_count = 0
                executor.allow_all_commands = False
                executor.should_stop = False

                # Execute task
                print(f"🤖 【AI 开始处理】\n")
                executor.execute_task(msg.content)
                print(f"\n✅ 【处理完成】\n")

            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Error processing message: {e}")

    # Run channels and message processor concurrently
    try:
        await asyncio.gather(
            channel_manager.start_all(),
            process_messages(),
            return_exceptions=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 正在关闭...\n")
        await channel_manager.stop_all()


def main():
    """Main chat loop"""
    # ASCII Art 欢迎图案
    ascii_art = """
    ███╗   ███╗██╗███╗   ██╗██╗██████╗  ██████╗ ████████╗
    ████╗ ████║██║████╗  ██║██║██╔══██╗██╔═══██╗╚══██╔══╝
    ██╔████╔██║██║██╔██╗ ██║██║██║  ██║██║   ██║   ██║
    ██║╚██╔╝██║██║██║╚██╗██║██║██║  ██║██║   ██║   ██║
    ██║ ╚═╝ ██║██║██║ ╚████║██║██████╔╝╚██████╔╝   ██║
    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝╚═════╝  ╚═════╝    ╚═╝

    轻量级 AI 自动化工具
    """
    print(ascii_art)
    print("✨ 我会一步步帮你完成任务")
    print("💡 按 Ctrl+C 可以中断当前任务，继续提问\n")

    executor = NaturalTaskExecutor()

    while True:
        try:
            user_input = get_user_input()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 再见！\n")
                break

            # Handle /clear command
            if user_input.lower().strip() == "/clear":
                executor._clear_history()
                continue

            # Reset for new task
            executor.execution_history = []
            executor.step_count = 0
            executor.allow_all_commands = False  # 重置命令允许状态

            print()
            executor.execute_task(user_input)

        except KeyboardInterrupt:
            print("\n\n⚠️  任务已中断")
            print("💡 你可以继续提问新的任务\n")
            # 不退出，继续循环
            continue
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}\n")


if __name__ == "__main__":
    import sys

    # Check for gateway mode
    if len(sys.argv) > 1 and sys.argv[1] == "gateway":
        asyncio.run(gateway_mode())
    else:
        main()
