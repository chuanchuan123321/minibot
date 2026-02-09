"""Shell execution tool"""
import subprocess
import os
import platform
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CommandResult:
    """Result of command execution"""
    returncode: int
    stdout: str
    stderr: str
    success: bool


class ShellTool:
    """Tool for executing shell commands"""

    def __init__(self, max_output_length: int = 5000):
        self.max_output_length = max_output_length
        self.last_result: Optional[CommandResult] = None

    def execute(self, command: str, cwd: Optional[str] = None) -> CommandResult:
        """Execute a shell command safely"""
        try:
            # Security: Prevent dangerous commands
            dangerous_patterns = [
                "rm -rf /",
                "dd if=/dev/zero",
                ":(){:|:&};:",  # fork bomb
            ]

            # Add Windows-specific dangerous patterns
            if platform.system() == 'Windows':
                dangerous_patterns.extend([
                    "del /s /q C:\\",
                    "format C:",
                    "diskpart",
                ])

            for pattern in dangerous_patterns:
                if pattern in command:
                    return CommandResult(
                        returncode=1,
                        stdout="",
                        stderr=f"Dangerous command blocked: {pattern}",
                        success=False
                    )

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=cwd or os.getcwd()
            )

            stdout = result.stdout[:self.max_output_length]
            stderr = result.stderr[:self.max_output_length]

            cmd_result = CommandResult(
                returncode=result.returncode,
                stdout=stdout,
                stderr=stderr,
                success=result.returncode == 0
            )

            self.last_result = cmd_result
            return cmd_result

        except subprocess.TimeoutExpired:
            return CommandResult(
                returncode=1,
                stdout="",
                stderr="Command timeout (30s)",
                success=False
            )
        except Exception as e:
            return CommandResult(
                returncode=1,
                stdout="",
                stderr=str(e),
                success=False
            )

    def get_current_dir(self) -> str:
        """Get current working directory"""
        return os.getcwd()

    def change_dir(self, path: str) -> Tuple[bool, str]:
        """Change working directory"""
        try:
            os.chdir(path)
            return True, f"Changed to {os.getcwd()}"
        except Exception as e:
            return False, str(e)

    def format_result(self, result: CommandResult) -> str:
        """Format command result for display"""
        output = []
        if result.stdout:
            output.append(f"Output:\n{result.stdout}")
        if result.stderr:
            output.append(f"Error:\n{result.stderr}")
        if not output:
            output.append("(No output)")

        status = "✓ Success" if result.success else f"✗ Failed (exit code: {result.returncode})"
        return f"{status}\n" + "\n".join(output)
