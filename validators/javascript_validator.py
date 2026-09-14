from pathlib import Path
from typing import Tuple


class JavaScriptValidator:
    """Performs basic structural validation of JavaScript files."""

    def validate(
        self,
        file_path: Path,
    ) -> Tuple[bool, str]:
        """Validate the basic structure of a JavaScript file."""

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
                    content.count("{") == content.count("}"),
                    "Braces are balanced",
                ),
                (
                    content.count("(") == content.count(")"),
                    "Parentheses are balanced",
                ),
                (
                    content.count("[") == content.count("]"),
                    "Square brackets are balanced",
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