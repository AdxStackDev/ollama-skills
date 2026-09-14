from pathlib import Path
from typing import Dict, Optional


class SkillManager:
    """Manages loading and matching skills from .md files."""

    def __init__(self, skills_dir: str = "skills") -> None:
        self.skills_dir = Path(skills_dir)
        self.skills = self.load_all_skills()

    def load_all_skills(self) -> Dict[str, Dict]:
        """Load flat skills and directory-based skills."""

        skills: Dict[str, Dict] = {}

        if not self.skills_dir.exists():
            print(
                f"Warning: Skills directory "
                f"'{self.skills_dir}' not found"
            )
            return skills

        # Load flat skill files:
        #
        # skills/
        # ├── backend-api.md
        # ├── database-design.md
        # └── frontend.md
        #
        for md_file in self.skills_dir.glob("*.md"):
            try:
                content = md_file.read_text(
                    encoding="utf-8"
                )

                metadata = self.parse_frontmatter(content)

                skills[md_file.stem] = {
                    "name": metadata.get(
                        "name",
                        md_file.stem,
                    ),
                    "description": metadata.get(
                        "description",
                        "",
                    ),
                    "content": content,
                    "path": str(md_file),
                    "examples": [],
                }

            except OSError as exc:
                print(
                    f"Error loading skill "
                    f"{md_file}: {exc}"
                )

        # Load directory-based skills:
        #
        # skills/
        # └── resume-portfolio/
        #     ├── skill.md
        #     └── examples/
        #
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_file = skill_dir / "skill.md"

            if not skill_file.exists():
                continue

            try:
                content = skill_file.read_text(
                    encoding="utf-8"
                )

                metadata = self.parse_frontmatter(
                    content
                )

                examples = []

                examples_dir = skill_dir / "examples"

                if examples_dir.exists():
                    for ex_file in sorted(
                        examples_dir.glob("*.md")
                    ):
                        examples.append(
                            {
                                "filename": ex_file.name,
                                "content": ex_file.read_text(
                                    encoding="utf-8"
                                ),
                            }
                        )

                skills[skill_dir.name] = {
                    "name": metadata.get(
                        "name",
                        skill_dir.name,
                    ),
                    "description": metadata.get(
                        "description",
                        "",
                    ),
                    "content": content,
                    "path": str(skill_file),
                    "examples": examples,
                }

            except OSError as exc:
                print(
                    f"Error loading skill "
                    f"{skill_dir}: {exc}"
                )

        return skills

    @staticmethod
    def parse_frontmatter(
        content: str,
    ) -> Dict[str, str]:
        """Parse the YAML-like frontmatter used by skills."""

        metadata: Dict[str, str] = {}

        if not content.startswith("---"):
            return metadata

        parts = content.split("---", 2)

        if len(parts) < 3:
            return metadata

        frontmatter = parts[1].strip()

        for line in frontmatter.splitlines():
            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            metadata[key.strip()] = value.strip()

        return metadata

    def get_skill_descriptions(self) -> str:
        """Return skill names and descriptions."""

        descriptions = []

        for skill in self.skills.values():
            descriptions.append(
                f"- {skill['name']}: "
                f"{skill['description']}"
            )

        return "\n".join(descriptions)

    def get_skill_by_name(
        self,
        name: str,
    ) -> Optional[Dict]:
        """Find a skill by ID or display name."""

        # Try skill ID first.
        if name in self.skills:
            return self.skills[name]

        # Then try display name.
        for skill_id, skill in self.skills.items():
            if skill["name"].lower() == name.lower():
                return skill

        return None