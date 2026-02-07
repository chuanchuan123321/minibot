"""Interactive CLI interface"""
import sys
from typing import Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
import os


class CLIInterface:
    """Interactive command-line interface"""

    def __init__(self, history_file: str = ".agent_history"):
        self.console = Console()
        self.history_file = history_file
        self.commands = {}
        self.running = False

    def register_command(self, name: str, handler: Callable, help_text: str = "") -> None:
        """Register a command handler"""
        self.commands[name] = {"handler": handler, "help": help_text}

    def print_welcome(self) -> None:
        """Print welcome message"""
        welcome_text = """
╔════════════════════════════════════════╗
║     AI Agent Terminal Interface        ║
║     Type 'help' for available commands ║
╚════════════════════════════════════════╝
        """
        self.console.print(welcome_text, style="cyan")

    def print_help(self) -> None:
        """Print help information"""
        table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan")
        table.add_column("Description")

        for cmd_name, cmd_info in self.commands.items():
            table.add_row(cmd_name, cmd_info["help"])

        self.console.print(table)

    def print_error(self, message: str) -> None:
        """Print error message"""
        self.console.print(f"[red]✗ Error:[/red] {message}")

    def print_success(self, message: str) -> None:
        """Print success message"""
        self.console.print(f"[green]✓ Success:[/green] {message}")

    def print_info(self, message: str) -> None:
        """Print info message"""
        self.console.print(f"[blue]ℹ Info:[/blue] {message}")

    def print_panel(self, content: str, title: str = "", style: str = "blue") -> None:
        """Print content in a panel"""
        panel = Panel(content, title=title, style=style)
        self.console.print(panel)

    def print_code(self, code: str, language: str = "python", theme: str = "monokai") -> None:
        """Print syntax-highlighted code"""
        syntax = Syntax(code, language, theme=theme, line_numbers=True)
        self.console.print(syntax)

    def get_input(self, prompt: str = "> ") -> str:
        """Get user input"""
        try:
            return input(prompt)
        except KeyboardInterrupt:
            return "exit"
        except EOFError:
            return "exit"

    def run_interactive_loop(self) -> None:
        """Run interactive command loop"""
        self.print_welcome()
        self.running = True

        while self.running:
            try:
                user_input = self.get_input("agent> ")

                if not user_input.strip():
                    continue

                parts = user_input.strip().split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if command == "exit" or command == "quit":
                    self.console.print("[yellow]Goodbye![/yellow]")
                    self.running = False
                    break

                if command == "help":
                    self.print_help()
                    continue

                if command in self.commands:
                    try:
                        self.commands[command]["handler"](args)
                    except Exception as e:
                        self.print_error(f"Command failed: {str(e)}")
                else:
                    self.print_error(f"Unknown command: {command}")

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted[/yellow]")
                continue

    def clear_screen(self) -> None:
        """Clear terminal screen"""
        os.system("clear" if os.name == "posix" else "cls")
