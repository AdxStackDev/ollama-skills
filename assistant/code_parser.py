import re
from typing import Dict


class CodeParser:
    """Extract generated source code from an Ollama Markdown response."""

    LANGUAGE_FILES = {
        "html": "index.html",
        "css": "styles.css",
        "javascript": "scripts.js",
        "js": "scripts.js",
        "python": "main.py",
        "sql": "schema.sql",
    }

    def extract_code_blocks(
        self,
        text: str,
    ) -> Dict[str, str]:
        """Extract supported Markdown code blocks."""

        code_blocks: Dict[str, str] = {}

        pattern = r"```(\w+)\n(.*?)```"

        matches = re.findall(
            pattern,
            text,
            re.DOTALL,
        )

        for language, code in matches:
            language = language.lower()
            code = code.strip()

            # Documentation is intentionally ignored.
            if language in {"markdown", "md"}:
                continue

            # JSON files.
            if language == "json":
                filename = (
                    "package.json"
                    if "package" in text.lower()
                    else "config.json"
                )

                code_blocks[filename] = code
                continue

            # Standard language → filename mapping.
            filename = self.LANGUAGE_FILES.get(language)

            if not filename:
                continue

            # Support multiple Python blocks.
            if filename == "main.py":
                if filename not in code_blocks:
                    code_blocks[filename] = code
                else:
                    index = 2

                    while (
                        f"script{index}.py"
                        in code_blocks
                    ):
                        index += 1

                    code_blocks[
                        f"script{index}.py"
                    ] = code

                continue

            code_blocks[filename] = code

        return code_blocks