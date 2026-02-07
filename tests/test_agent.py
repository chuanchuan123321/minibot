"""Unit tests for AI Agent"""
import unittest
import os
import tempfile
from pathlib import Path

from agent.core.ai_engine import AIEngine, Message
from agent.tools.shell import ShellTool, CommandResult
from agent.tools.file import FileTool


class TestAIEngine(unittest.TestCase):
    """Test AI Engine"""

    def setUp(self):
        self.engine = AIEngine()

    def test_add_message(self):
        """Test adding messages"""
        self.engine.add_message("user", "Hello")
        self.assertEqual(len(self.engine.conversation_history), 1)
        self.assertEqual(self.engine.conversation_history[0].role, "user")

    def test_clear_history(self):
        """Test clearing history"""
        self.engine.add_message("user", "Hello")
        self.engine.clear_history()
        self.assertEqual(len(self.engine.conversation_history), 0)

    def test_get_history(self):
        """Test getting history in API format"""
        self.engine.add_message("user", "Hello")
        self.engine.add_message("assistant", "Hi there")
        history = self.engine.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")


class TestShellTool(unittest.TestCase):
    """Test Shell Tool"""

    def setUp(self):
        self.shell = ShellTool()

    def test_execute_success(self):
        """Test successful command execution"""
        result = self.shell.execute("echo 'test'")
        self.assertTrue(result.success)
        self.assertIn("test", result.stdout)

    def test_execute_failure(self):
        """Test failed command execution"""
        result = self.shell.execute("false")
        self.assertFalse(result.success)
        self.assertNotEqual(result.returncode, 0)

    def test_dangerous_command_blocked(self):
        """Test dangerous command blocking"""
        result = self.shell.execute("rm -rf /")
        self.assertFalse(result.success)
        self.assertIn("blocked", result.stderr.lower())

    def test_get_current_dir(self):
        """Test getting current directory"""
        cwd = self.shell.get_current_dir()
        self.assertEqual(cwd, os.getcwd())


class TestFileTool(unittest.TestCase):
    """Test File Tool"""

    def setUp(self):
        self.file_tool = FileTool()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_write_and_read_file(self):
        """Test writing and reading files"""
        test_file = "test.txt"
        test_content = "Hello, World!"

        success, msg = self.file_tool.write_file(test_file, test_content)
        self.assertTrue(success)

        success, content = self.file_tool.read_file(test_file)
        self.assertTrue(success)
        self.assertEqual(content, test_content)

    def test_file_exists(self):
        """Test file existence check"""
        test_file = "test.txt"
        self.file_tool.write_file(test_file, "content")
        self.assertTrue(self.file_tool.file_exists(test_file))
        self.assertFalse(self.file_tool.file_exists("nonexistent.txt"))

    def test_create_directory(self):
        """Test directory creation"""
        test_dir = "test_dir"
        success, msg = self.file_tool.create_directory(test_dir)
        self.assertTrue(success)
        self.assertTrue(Path(test_dir).exists())

    def test_list_files(self):
        """Test listing files"""
        self.file_tool.write_file("file1.txt", "content1")
        self.file_tool.write_file("file2.txt", "content2")

        success, files = self.file_tool.list_files(".")
        self.assertTrue(success)
        self.assertGreaterEqual(len(files), 2)


if __name__ == "__main__":
    unittest.main()
