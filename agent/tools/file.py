"""File operations tool"""
import os
import shutil
from typing import List, Tuple, Optional
from pathlib import Path
import subprocess


class FileTool:
    """Tool for file operations"""

    @staticmethod
    def expand_path(path: str) -> str:
        """Expand path with support for ~, Desktop, Documents, etc."""
        # Replace common aliases
        path = path.replace("桌面", "Desktop")
        path = path.replace("文档", "Documents")
        path = path.replace("下载", "Downloads")

        # Expand ~ to home directory
        path = os.path.expanduser(path)

        # If path is not absolute, make it absolute from home
        # Use os.path.isabs() for cross-platform compatibility
        if not os.path.isabs(path):
            path = os.path.join(os.path.expanduser("~"), path)

        return path

    @staticmethod
    def read_file(path: str, max_lines: Optional[int] = None) -> Tuple[bool, str]:
        """Read file contents"""
        try:
            file_path = Path(FileTool.expand_path(path)).resolve()

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if max_lines:
                lines = lines[:max_lines]

            content = ''.join(lines)
            return True, content

        except FileNotFoundError:
            return False, f"File not found: {path}"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    @staticmethod
    def write_file(path: str, content: str, append: bool = False) -> Tuple[bool, str]:
        """Write content to file"""
        try:
            file_path = Path(FileTool.expand_path(path)).resolve()

            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            mode = 'a' if append else 'w'
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)

            return True, f"File {'appended' if append else 'written'}: {path}"

        except Exception as e:
            return False, f"Error writing file: {str(e)}"

    @staticmethod
    def list_files(path: str = ".", recursive: bool = False) -> Tuple[bool, List[str]]:
        """List files in directory"""
        try:
            dir_path = Path(FileTool.expand_path(path)).resolve()

            if not dir_path.is_dir():
                return False, [f"Not a directory: {path}"]

            if recursive:
                files = [str(p.relative_to(dir_path)) for p in dir_path.rglob('*')]
            else:
                files = [str(p.relative_to(dir_path)) for p in dir_path.iterdir()]

            return True, sorted(files)

        except Exception as e:
            return False, [f"Error listing files: {str(e)}"]

    @staticmethod
    def delete_file(path: str) -> Tuple[bool, str]:
        """Delete a file"""
        try:
            file_path = Path(FileTool.expand_path(path)).resolve()

            if not file_path.exists():
                return False, f"File not found: {path}"

            if file_path.is_dir():
                return False, "Use delete_directory for directories"

            file_path.unlink()
            return True, f"File deleted: {path}"

        except Exception as e:
            return False, f"Error deleting file: {str(e)}"

    @staticmethod
    def delete_directory(path: str) -> Tuple[bool, str]:
        """Delete a directory"""
        try:
            dir_path = Path(FileTool.expand_path(path)).resolve()

            if not dir_path.exists():
                return False, f"Directory not found: {path}"

            if not dir_path.is_dir():
                return False, "Use delete_file for files"

            shutil.rmtree(dir_path)
            return True, f"Directory deleted: {path}"

        except Exception as e:
            return False, f"Error deleting directory: {str(e)}"

    @staticmethod
    def create_directory(path: str) -> Tuple[bool, str]:
        """Create a directory"""
        try:
            dir_path = Path(FileTool.expand_path(path)).resolve()
            dir_path.mkdir(parents=True, exist_ok=True)
            return True, f"Directory created: {path}"

        except Exception as e:
            return False, f"Error creating directory: {str(e)}"

    @staticmethod
    def file_exists(path: str) -> bool:
        """Check if file exists"""
        return Path(FileTool.expand_path(path)).exists()

    @staticmethod
    def get_file_info(path: str) -> Tuple[bool, dict]:
        """Get file information"""
        try:
            file_path = Path(FileTool.expand_path(path)).resolve()

            if not file_path.exists():
                return False, {}

            stat = file_path.stat()
            return True, {
                "path": str(file_path),
                "size": stat.st_size,
                "is_file": file_path.is_file(),
                "is_dir": file_path.is_dir(),
                "modified": stat.st_mtime,
            }

        except Exception as e:
            return False, {"error": str(e)}
