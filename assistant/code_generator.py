from pathlib import Path
from typing import Dict, List

from assistant.code_parser import CodeParser
from assistant.ollama_client import OllamaClient
from assistant.project_manager import ProjectManager
from assistant.prompt_router import PromptRouter
from assistant.skill_manager import SkillManager
from validators.css_validator import CssValidator
from validators.html_validator import HtmlValidator
from validators.javascript_validator import JavaScriptValidator


class CodeGenerator:
    """Orchestrates skill selection, code generation, file creation,
    and basic validation.
    """

    def __init__(
        self,
        ollama_client: OllamaClient,
        skill_manager: SkillManager,
        project_manager: ProjectManager,
    ) -> None:
        self.ollama_client = ollama_client
        self.skill_manager = skill_manager
        self.project_manager = project_manager

        self.code_parser = CodeParser()

        self.validators = {
            ".html": HtmlValidator(),
            ".css": CssValidator(),
            ".js": JavaScriptValidator(),
        }

    def list_available_skills(self) -> None:
        """Display all available skills."""

        print("\n📚 Available Skills:")

        if not self.skill_manager.skills:
            print("  No skills found.")
            return

        for skill_id, skill in self.skill_manager.skills.items():
            print(
                f"  • {skill_id}: "
                f"{skill['description']}"
            )

    def execute_request(
        self,
        user_prompt: str,
        router: PromptRouter,
    ) -> None:
        """Process a complete user request."""

        print("\n🔍 Analyzing request...")

        selected_skill_names = router.analyze(
            user_prompt
        )

        print(
            "🧠 Selected skills: "
            f"{', '.join(selected_skill_names) or 'none'}"
        )

        selected_skills = self._load_selected_skills(
            selected_skill_names
        )

        generation_prompt = self._build_generation_prompt(
            user_prompt=user_prompt,
            selected_skills=selected_skills,
        )

        print("\n🤖 Generating code...")

        response = self.ollama_client.generate(
            generation_prompt,
            stream=False,
        )

        if not response:
            print("❌ Ollama returned an empty response.")
            return

        code_blocks = self.code_parser.extract_code_blocks(
            response
        )

        if not code_blocks:
            print(
                "❌ No supported code blocks were found "
                "in the Ollama response."
            )
            return

        project_name = self._generate_project_name(
            user_prompt
        )

        self.project_manager.create_project(
            project_name
        )

        self._write_generated_files(
            code_blocks
        )

        self._validate_generated_files(
            code_blocks
        )

        print(
            f"\n✅ Project created: "
            f"{project_name}"
        )

    def _load_selected_skills(
        self,
        skill_names: List[str],
    ) -> List[Dict]:
        """Load skills selected by the prompt router."""

        selected_skills: List[Dict] = []

        for skill_name in skill_names:
            skill = self.skill_manager.get_skill_by_name(
                skill_name
            )

            if skill:
                selected_skills.append(skill)
            else:
                print(
                    f"⚠️ Skill not found: "
                    f"{skill_name}"
                )

        return selected_skills

    def _build_generation_prompt(
        self,
        user_prompt: str,
        selected_skills: List[Dict],
    ) -> str:
        """Build the prompt sent to Ollama for code generation."""

        skill_context = []

        for skill in selected_skills:
            skill_context.append(
                f"""
### Skill: {skill['name']}

Description:
{skill['description']}

Instructions:
{skill['content']}
"""
            )

            if skill["examples"]:
                skill_context.append(
                    "\nExamples:"
                )

                for example in skill["examples"]:
                    skill_context.append(
                        f"""
Example file: {example['filename']}

{example['content']}
"""
                    )

        skills_text = (
            "\n".join(skill_context)
            if skill_context
            else "No specific skills were selected."
        )

        return f"""You are a professional software developer.

Generate the complete code required for the user's request.

User Request:
{user_prompt}

Relevant Skills:
{skills_text}

Requirements:
- Generate complete working code.
- Do not omit important implementation details.
- Use the relevant skills when applicable.
- Return source code using Markdown fenced code blocks.
- Use supported language identifiers such as html, css, javascript, js, python, or json.
- Do not put explanations inside the code blocks.
- Make the generated code directly usable.

Generate the implementation now.
"""

    def _generate_project_name(
        self,
        user_prompt: str,
    ) -> str:
        """Generate a filesystem-safe project name."""

        prompt = f"""Generate a short project folder name for this request:

{user_prompt}

Rules:
- Return only the folder name.
- Use lowercase letters, numbers, and hyphens.
- Do not use spaces.
- Do not use special characters.
- Keep it short.
"""

        try:
            result = self.ollama_client.generate(
                prompt,
                stream=False,
            )

            project_name = result.strip()

            if project_name:
                return self._sanitize_project_name(
                    project_name
                )

        except Exception as exc:
            print(
                f"⚠️ Could not generate project name: "
                f"{exc}"
            )

        return "generated-project"

    @staticmethod
    def _sanitize_project_name(
        project_name: str,
    ) -> str:
        """Convert a generated name into a safe basic folder name."""

        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "0123456789-"
        )

        sanitized = "".join(
            character
            for character in project_name.lower()
            if character in allowed
        )

        return sanitized.strip("-") or "generated-project"

    def _write_generated_files(
        self,
        code_blocks: Dict[str, str],
    ) -> None:
        """Write parsed code blocks to the active project."""

        print("\n📝 Writing files...")

        for filename, content in code_blocks.items():
            success = self.project_manager.write_file(
                filename=filename,
                content=content,
            )

            if not success:
                print(
                    f"⚠️ Failed to write: {filename}"
                )

    def _validate_generated_files(
        self,
        code_blocks: Dict[str, str],
    ) -> None:
        """Run the appropriate validator for generated files."""

        print("\n🔎 Validating generated files...")

        project = self.project_manager.current_project

        if not project:
            print("❌ No active project.")
            return

        for filename in code_blocks:
            file_path = project / filename
            extension = Path(filename).suffix.lower()

            validator = self.validators.get(
                extension
            )

            if not validator:
                print(
                    f"  ℹ️ No validator for "
                    f"{filename}"
                )
                continue

            passed, details = validator.validate(
                file_path
            )

            print(f"\n📄 {filename}")
            print(details)

            if passed:
                print("  ✅ Validation passed")
            else:
                print("  ❌ Validation failed")