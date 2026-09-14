from pathlib import Path
from typing import Tuple


class CssValidator:
    """Performs basic structural validation of CSS files."""

    def validate(
        self,
        file_path: Path,
    ) -> Tuple[bool, str]:
        """Validate the basic structure of a CSS file."""

        if not file_path.exists():
            return (
                False,
                f"{file_path.name} not found",
            )

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            content = content.strip()

            checks = [
                (
                    bool(content),
                    "File is not empty",
                ),
                (
                    "{" in content,
                    "Contains opening braces",
                ),
                (
                    "}" in content,
                    "Contains closing braces",
                ),
                (
                    content.count("{") == content.count("}"),
                    "Braces are balanced",
                ),
            ]

            passed = all(
                check_passed
                for check_passed, _ in checks
            )

            details = "\n".join(
                f"  {'✅' if check_passed else '❌'} "
                f"{description}"
                for check_passed, description in checks
            )

            return passed, details

        except OSError as exc:
            return False, str(exc)