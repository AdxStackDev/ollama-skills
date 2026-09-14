from typing import List

from assistant.ollama_client import OllamaClient
from assistant.skill_manager import SkillManager


class PromptRouter:
    """Determines which skills should be used for a user request."""

    def __init__(
        self,
        ollama_client: OllamaClient,
        skill_manager: SkillManager,
    ) -> None:
        self.ollama_client = ollama_client
        self.skill_manager = skill_manager

    def analyze(self, user_prompt: str) -> List[str]:
        """Ask Ollama to select relevant skills."""

        available_skills = (
            self.skill_manager.get_skill_descriptions()
        )

        analysis_prompt = f"""You are a skill routing assistant.
Analyze the user's request and determine which skills are relevant.

Available Skills:
{available_skills}

User Request: {user_prompt}

Based on the user's request, which skills should be loaded?
Respond with ONLY the skill names
(like 'frontend-design', 'backend-api', etc.)
separated by commas, or 'none' if no specific skills are needed.

Your response (skill names only):"""

        try:
            result = self.ollama_client.generate(
                analysis_prompt,
                stream=False,
            ).lower()

            if result == "none" or not result:
                return []

            return [
                name.strip()
                for name in result.split(",")
                if name.strip()
            ]

        except Exception as exc:
            print(
                f"Error analyzing prompt: {exc}"
            )
            return []