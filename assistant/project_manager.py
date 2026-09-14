from pathlib import Path
import webbrowser


class ProjectManager:
    """Manages project directories and generated project files."""

    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.current_project: Path | None = None

    def create_project(self, project_name: str) -> Path:
        """Create a new project directory and make it active."""

        project_path = self.output_dir / project_name

        project_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.current_project = project_path

        print(
            f"Created project directory: "
            f"{project_path}"
        )

        return project_path

    def write_file(self, filename: str, content: str) -> bool:
        """Write a generated file into the active project."""

        if not self.current_project:
            print("No active project")
            return False

        try:
            file_path = (
                self.current_project / filename
            )

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path.write_text(
                content,
                encoding="utf-8",
            )

            print(f"Created: {filename}")

            return True

        except OSError as exc:
            print(
                f"Error writing "
                f"{filename}: {exc}"
            )

            return False

    def open_in_browser(self, filename: str = "index.html") -> None:
        """Open a project file in the default browser."""

        if not self.current_project:
            print("No active project")
            return

        file_path = (
            self.current_project / filename
        )

        if not file_path.exists():
            print(
                f"{filename} not found"
            )
            return

        try:
            webbrowser.open(
                file_path.as_uri()
            )

            print(
                f"Opened {filename} in browser"
            )

        except Exception as exc:
            print(
                f"Error opening browser: {exc}"
            )

    def list_project_files(self) -> None:
        """List all files in the active project."""

        if not self.current_project:
            print("No active project")
            return

        print(
            f"\n Project files in "
            f"{self.current_project.name}:"
        )

        for file_path in sorted(
            self.current_project.rglob("*")
        ):
            if not file_path.is_file():
                continue

            relative_path = (
                file_path.relative_to(
                    self.current_project
                )
            )

            size = file_path.stat().st_size

            print(
                f"{relative_path} "
                f"({size} bytes)"
            )