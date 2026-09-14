from pathlib import Path
from typing import Tuple


class HtmlValidator:
    """Performs basic structural validation of HTML files."""

    def validate(
        self,
        file_path: Path,
    ) -> Tuple[bool, str]:
        """Validate the basic structure of an HTML file."""

        if not file_path.exists():
            return (
                False,
                f"{file_path.name} not found",
            )

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            checks = [
                (
                    "<!DOCTYPE html>" in content,
                    "Has DOCTYPE declaration",
                ),
                (
                    "<html" in content,
                    "Has <html> tag",
                ),
                (
                    "<head>" in content,
                    "Has <head> section",
                ),
                (
                    "<body>" in content,
                    "Has <body> section",
                ),
                (
                    "</html>" in content,
                    "Properly closed",
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