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
import json


class NaturalTaskExecutor:
    """Execute tasks with natural conversational flow"""

    def __init__(self):
        self.ai_engine = AIEngine()
        self.tool_executor = ExtendedToolExecutor()
        self.available_tools = self.tool_executor.get_available_tools()
        self.execution_history = []
        self.step_count = 0
        self.max_steps = 100
        self.allow_all_commands = False  # 是否允许所有命令
        self.timer_triggered = False  # 定时器是否被触发
        self.waiting_for_timer = False  # 是否在等待定时器

    def execute_task(self, user_request: str):
        """Execute task dynamically with natural flow"""
        # Build context from execution history
        context = self._build_context()

        # First step: Decide what to do
        self.step_count = 1
        self._execute_step(user_request, context)

    def _execute_step(self, user_request: str, context: str):
        """Execute a single step with natural description"""
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

重要提示:
- 如果任务涉及阅读文档（.pdf, .docx, .doc等），优先使用 read_pdf 工具
- read_pdf 工具可以处理多种文档格式，包括Word文档
- 如果任务还未完成，必须继续执行下一步
- 只有当任务真正完成时才给出最终回应
- 如果找到了任务所需的信息，使用它来进行下一步

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

        # 显示AI的回答（截断长内容）
        display_response = self._truncate_response(response, max_length=50)
        print(display_response)

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

        else:
            print(f"\n⚠️  未知操作: {action}，继续下一步...\n")
            self.step_count += 1
            context = self._build_context()
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

    def _parse_json_response(self, response: str, max_retries: int = 2) -> dict:
        """尝试解析JSON响应，失败时重试"""
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

                # 尝试修复未转义的引号问题
                import re

                # 首先尝试直接解析
                try:
                    decision = json.loads(json_str)
                    return decision
                except json.JSONDecodeError:
                    # 如果失败，尝试修复常见问题
                    # 处理 HTML 内容中的引号
                    json_str = re.sub(r'(?<=[a-zA-Z0-9])"(?=[a-zA-Z0-9=])', '\\"', json_str)

                    decision = json.loads(json_str)
                    return decision

            except json.JSONDecodeError as e:
                if attempt == max_retries - 1:
                    print(f"⚠️  JSON解析错误: {str(e)}")
                    print(f"原始响应: {response[:200]}...")
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

        while True:
            try:
                # 清空当前行并显示菜单
                print("\r" + " " * 80, end="\r")  # 清空行

                # 显示选项
                display = "[yes/all/no] 允许执行? "
                for i, opt in enumerate(options):
                    if i == selected:
                        display += f"[{opt}] "  # 当前选中的选项用方括号
                    else:
                        display += f" {opt}  "

                print(display, end="", flush=True)

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
    main()
