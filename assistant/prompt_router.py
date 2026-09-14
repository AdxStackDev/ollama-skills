import re
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

        # Build an explicit list of valid IDs to
        # anchor the model's output.
        valid_ids = ", ".join(
            f"'{sid}'"
            for sid in self.skill_manager.skills
        )

        analysis_prompt = f"""You are a skill routing assistant.

Available skill IDs: {valid_ids}

Available Skills:
{available_skills}

User Request: {user_prompt}

Which skill IDs from the list above are relevant?
Reply with ONLY the skill IDs exactly as shown, separated by commas.
Do not add explanations, parentheses, or any other text.
If none apply, reply with the single word: none

Reply:"""

        try:
            result = self.ollama_client.generate(
                analysis_prompt,
                stream=False,
            ).lower().strip()

            if not result or result == "none":
                return []

            # Keep only tokens that are valid skill IDs
            # or display names — drop any extra words the
            # model appended despite instructions.
            valid_skill_ids = set(
                self.skill_manager.skills.keys()
            )
            valid_display_names = {
                skill["name"].lower()
                for skill in self.skill_manager.skills.values()
            }

            candidates = [
                token.strip()
                for token in result.split(",")
                if token.strip()
            ]

            matched: List[str] = []
            for candidate in candidates:
                # Exact ID or display-name match.
                if (
                    candidate in valid_skill_ids
                    or candidate in valid_display_names
                ):
                    matched.append(candidate)
                    continue

                # Fallback: check if any valid ID/name
                # is a substring of the candidate
                # (handles "resume-portfolio (blah)").
                for vid in valid_skill_ids | valid_display_names:
                    if vid in candidate:
                        matched.append(vid)
                        break

            return matched

        except Exception as exc:
            print(
                f"Error analyzing prompt: {exc}"
            )
            return []