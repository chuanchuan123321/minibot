"""Skills system for Minibot - modular capability extensions"""
import os
import json
from pathlib import Path
from typing import Optional, List, Dict
import re
import subprocess


class SkillsLoader:
    """Load and manage skills from workspace and builtin directories"""

    def __init__(self, workspace: Path, builtin_skills_dir: Optional[Path] = None):
        """
        Initialize SkillsLoader

        Args:
            workspace: Path to workspace directory
            builtin_skills_dir: Path to builtin skills directory (default: agent/skills)
        """
        self.workspace = workspace
        self.workspace_skills = workspace / "skills"

        # Default builtin skills directory
        if builtin_skills_dir is None:
            builtin_skills_dir = Path(__file__).parent.parent / "skills"
        self.builtin_skills = builtin_skills_dir

        # Create workspace skills directory if it doesn't exist
        self.workspace_skills.mkdir(parents=True, exist_ok=True)

    def list_skills(self, filter_unavailable: bool = True) -> List[Dict[str, str]]:
        """
        List all available skills

        Args:
            filter_unavailable: If True, filter out skills with missing dependencies

        Returns:
            List of skill metadata dicts
        """
        skills = {}

        # Load builtin skills first
        if self.builtin_skills.exists():
            for skill_dir in self.builtin_skills.iterdir():
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        metadata = self._parse_skill_metadata(skill_file)
                        if metadata:
                            skills[metadata["name"]] = {
                                **metadata,
                                "location": "builtin",
                                "path": str(skill_file)
                            }

        # Load workspace skills (override builtin)
        if self.workspace_skills.exists():
            for skill_dir in self.workspace_skills.iterdir():
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        metadata = self._parse_skill_metadata(skill_file)
                        if metadata:
                            skills[metadata["name"]] = {
                                **metadata,
                                "location": "workspace",
                                "path": str(skill_file)
                            }

        # Filter unavailable skills
        if filter_unavailable:
            available_skills = {}
            for name, skill in skills.items():
                if self._check_skill_available(skill):
                    available_skills[name] = skill
            return list(available_skills.values())

        return list(skills.values())

    def load_skill(self, name: str) -> Optional[str]:
        """
        Load skill content by name, including scripts information

        Args:
            name: Skill name

        Returns:
            Skill content (without frontmatter) with scripts info or None if not found
        """
        # Try workspace first
        workspace_skill = self.workspace_skills / name / "SKILL.md"
        if workspace_skill.exists():
            skill_dir = workspace_skill.parent
            content = self._extract_skill_content(workspace_skill)
            scripts_info = self._get_scripts_info(skill_dir)
            if scripts_info:
                content += f"\n\n## 可用脚本\n\n{scripts_info}"
            return content

        # Try builtin
        builtin_skill = self.builtin_skills / name / "SKILL.md"
        if builtin_skill.exists():
            skill_dir = builtin_skill.parent
            content = self._extract_skill_content(builtin_skill)
            scripts_info = self._get_scripts_info(skill_dir)
            if scripts_info:
                content += f"\n\n## 可用脚本\n\n{scripts_info}"
            return content

        return None

    def load_skills_for_context(self, skill_names: List[str]) -> str:
        """
        Load multiple skills for AI context

        Args:
            skill_names: List of skill names to load

        Returns:
            Formatted skill content for context
        """
        contents = []
        for name in skill_names:
            content = self.load_skill(name)
            if content:
                contents.append(f"## {name.upper()} Skill\n\n{content}")

        return "\n\n---\n\n".join(contents)

    def build_skills_summary(self) -> str:
        """
        Build summary of all available skills in XML format (like nanobot)

        Returns:
            XML-formatted skills summary
        """
        skills = self.list_skills(filter_unavailable=False)

        summary = "<skills>\n"
        for skill in skills:
            available = self._check_skill_available(skill)
            status = "available" if available else "unavailable"

            summary += f"  <skill>\n"
            summary += f"    <name>{skill['name']}</name>\n"
            summary += f"    <description>{skill.get('description', 'N/A')}</description>\n"
            summary += f"    <location>{skill['location']}</location>\n"
            summary += f"    <status>{status}</status>\n"

            # Show missing requirements
            missing = self._get_missing_requirements(skill)
            if missing:
                summary += f"    <missing>{', '.join(missing)}</missing>\n"

            summary += f"  </skill>\n"

        summary += "</skills>"
        return summary

    def get_always_skills(self) -> List[str]:
        """
        Get skills marked as always=true

        Returns:
            List of always-loaded skill names
        """
        always_skills = []
        for skill in self.list_skills(filter_unavailable=False):
            if skill.get("always") == "true":
                always_skills.append(skill["name"])
        return always_skills

    def _parse_skill_metadata(self, skill_file: Path) -> Optional[Dict]:
        """Parse YAML frontmatter from SKILL.md"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                return None

            frontmatter = match.group(1)
            metadata = {}

            # Parse YAML-like format
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')

            return metadata if metadata.get('name') else None
        except Exception as e:
            print(f"Error parsing skill metadata: {e}")
            return None

    def _extract_skill_content(self, skill_file: Path) -> str:
        """Extract content without frontmatter"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove frontmatter
            match = re.match(r'^---\n.*?\n---\n(.*)', content, re.DOTALL)
            if match:
                return match.group(1).strip()
            return content
        except Exception as e:
            print(f"Error extracting skill content: {e}")
            return ""

    def _get_scripts_info(self, skill_dir: Path) -> str:
        """
        Scan skill directory for scripts and return their information

        Args:
            skill_dir: Path to skill directory

        Returns:
            Formatted script information
        """
        script_extensions = {'.py', '.sh', '.js', '.ts', '.go', '.rb', '.lua'}
        scripts = []

        try:
            for file in skill_dir.iterdir():
                if file.is_file() and file.suffix in script_extensions:
                    scripts.append(file)
        except Exception as e:
            print(f"Error scanning scripts: {e}")
            return ""

        if not scripts:
            return ""

        # Build script information
        info = []
        for script in sorted(scripts):
            script_name = script.name
            script_path = str(script)
            info.append(f"- **{script_name}** - `{script_path}`")

        return "\n".join(info)

    def _find_skill_dir(self, skill_name: str) -> Optional[Path]:
        """
        Find skill directory by name

        Args:
            skill_name: Name of the skill

        Returns:
            Path to skill directory or None if not found
        """
        # Try workspace first
        workspace_skill_dir = self.workspace_skills / skill_name
        if workspace_skill_dir.exists() and (workspace_skill_dir / "SKILL.md").exists():
            return workspace_skill_dir

        # Try builtin
        builtin_skill_dir = self.builtin_skills / skill_name
        if builtin_skill_dir.exists() and (builtin_skill_dir / "SKILL.md").exists():
            return builtin_skill_dir

        return None

    def _check_skill_available(self, skill: Dict) -> bool:
        """Check if skill dependencies are available"""
        # Check CLI tools
        requires_bins = skill.get("requires_bins", "").split(",")
        for bin_name in requires_bins:
            bin_name = bin_name.strip()
            if bin_name and not self._check_command_exists(bin_name):
                return False

        # Check environment variables
        requires_env = skill.get("requires_env", "").split(",")
        for env_var in requires_env:
            env_var = env_var.strip()
            if env_var and not os.getenv(env_var):
                return False

        return True

    def _get_missing_requirements(self, skill: Dict) -> List[str]:
        """Get list of missing requirements"""
        missing = []

        # Check CLI tools
        requires_bins = skill.get("requires_bins", "").split(",")
        for bin_name in requires_bins:
            bin_name = bin_name.strip()
            if bin_name and not self._check_command_exists(bin_name):
                missing.append(f"bin:{bin_name}")

        # Check environment variables
        requires_env = skill.get("requires_env", "").split(",")
        for env_var in requires_env:
            env_var = env_var.strip()
            if env_var and not os.getenv(env_var):
                missing.append(f"env:{env_var}")

        return missing

    @staticmethod
    def _check_command_exists(command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run(
                ["which", command],
                capture_output=True,
                timeout=1
            )
            return True
        except Exception:
            return False
