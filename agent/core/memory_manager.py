"""Memory management system for storing and retrieving compressed context."""

import json
import asyncio
from pathlib import Path
from datetime import datetime


class MemoryManager:
    """Manages persistent memory storage for accumulated compression and metadata."""

    def __init__(self, memory_dir: str | None = None):
        """
        Initialize memory manager.

        Args:
            memory_dir: Path to memory directory. If None, uses default Memory folder.
        """
        if memory_dir is None:
            memory_dir = str(Path(__file__).parent.parent.parent / "Memory")

        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.compression_file = self.memory_dir / "accumulated_compression.md"
        self.execution_history_file = self.memory_dir / "execution_history.md"
        self.index_file = self.memory_dir / "index.json"

    def _get_today_folder(self) -> Path:
        """Get or create today's date folder."""
        today = datetime.now().strftime("%Y-%m-%d")
        today_folder = self.memory_dir / today
        today_folder.mkdir(parents=True, exist_ok=True)
        return today_folder

    def _get_compression_filename(self) -> str:
        """Get archive filename with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{timestamp}_历史.md"

    def load_accumulated_compression(self) -> str:
        """Load accumulated compression from file."""
        if self.compression_file.exists():
            with open(self.compression_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def save_accumulated_compression(self, compression: str) -> None:
        """Save accumulated compression to file."""
        with open(self.compression_file, 'w', encoding='utf-8') as f:
            f.write(compression)

    def save_compression_archive(self, compression_content: str) -> str:
        """
        Save compression to archive folder with date and timestamp.

        Returns:
            The relative path to the saved compression file.
        """
        today_folder = self._get_today_folder()
        filename = self._get_compression_filename()
        filepath = today_folder / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(compression_content)

        # Return relative path from Memory folder
        return f"{filepath.relative_to(self.memory_dir)}"

    def load_execution_history(self) -> list[str]:
        """Load execution history from file."""
        if self.execution_history_file.exists():
            with open(self.execution_history_file, 'r', encoding='utf-8') as f:
                lines = f.read().strip().split('\n')
                return [line for line in lines if line.strip()]
        return []

    def save_execution_history(self, history: list[str]) -> None:
        """Save execution history to file."""
        with open(self.execution_history_file, 'w', encoding='utf-8') as f:
            for entry in history:
                f.write(entry + '\n')

    async def async_save_execution_history(self, history: list[str]) -> None:
        """Asynchronously save execution history to file."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save_execution_history, history)

    def append_execution_step(self, step: str) -> None:
        """Append a single execution step to history file."""
        with open(self.execution_history_file, 'a', encoding='utf-8') as f:
            f.write(step + '\n')

    async def async_append_execution_step(self, step: str) -> None:
        """Asynchronously append a single execution step to history file."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.append_execution_step, step)

    def load_index(self) -> dict:
        """Load index of all memories."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except json.JSONDecodeError:
                pass
            except Exception:
                pass

        return {"compressions": []}

    def save_index(self, index: dict) -> None:
        """Save index of all memories."""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def add_compression_entry(self, compression_num: int, summary: str, archive_path: str) -> None:
        """Add a new compression entry to the index."""
        index = self.load_index()

        entry = {
            "compression_num": compression_num,
            "timestamp": datetime.now().isoformat(),
            "summary": summary[:100] + "..." if len(summary) > 100 else summary,
            "archive_path": archive_path,
        }

        index["compressions"].append(entry)
        self.save_index(index)

    def clear_all(self) -> None:
        """Clear all memory files including archives."""
        import shutil

        # Clear main memory files
        if self.compression_file.exists():
            self.compression_file.unlink()
        if self.execution_history_file.exists():
            self.execution_history_file.unlink()
        if self.index_file.exists():
            self.index_file.unlink()

        # Clear all archived files in date-based folders
        if self.memory_dir.exists():
            # Remove the entire Memory directory and all its contents
            shutil.rmtree(self.memory_dir)
            # Recreate the basic directory structure
            self.memory_dir.mkdir(parents=True, exist_ok=True)
            # Recreate the main files (empty)
            self.compression_file.touch()
            self.execution_history_file.touch()
            self.index_file.touch()

    def clear_execution_history(self) -> None:
        """Clear only the execution history file content (keep the file)."""
        # 清空文件内容而不是删除文件
        with open(self.execution_history_file, 'w', encoding='utf-8') as f:
            f.write("")

    def get_memory_stats(self) -> dict:
        """Get statistics about stored memories."""
        compression = self.load_accumulated_compression()
        history = self.load_execution_history()

        # Count compressions by splitting on compression markers
        compression_count = len(compression.split('【任务')) - 1

        return {
            "compression_count": compression_count,
            "compression_size": len(compression),
            "execution_history_steps": len(history),
        }


