from assistant.code_generator import CodeGenerator
from assistant.ollama_client import OllamaClient
from assistant.project_manager import ProjectManager
from assistant.prompt_router import PromptRouter
from assistant.skill_manager import SkillManager


def print_banner() -> None:
    """Display application information and available commands."""
    print("=" * 60)
    print("🚀 Smart Ollama Assistant with Code Execution")
    print("=" * 60)
    print("This assistant will:")
    print("  ✓ Analyze your request")
    print("  ✓ Load relevant skills")
    print("  ✓ Generate complete code")
    print("  ✓ Execute and validate step-by-step")
    print("=" * 60)

    print("\nCommands:")
    print("  - Type your project request")
    print("  - 'skills' - List all available skills")
    print("  - 'open' - Open current project in browser")
    print("  - 'files' - List current project files")
    print("  - 'quit' or 'exit' - End the session")
    print("=" * 60)


def main() -> None:
    """Main application entry point."""

    skill_manager = SkillManager()

    ollama_client = OllamaClient()

    prompt_router = PromptRouter(
        ollama_client=ollama_client,
        skill_manager=skill_manager,
    )

    project_manager = ProjectManager()

    code_generator = CodeGenerator(
        ollama_client=ollama_client,
        skill_manager=skill_manager,
        project_manager=project_manager,
    )

    print_banner()

    code_generator.list_available_skills()

    while True:
        try:
            user_input = input("\n💬 You: ").strip()

            if not user_input:
                continue

            command = user_input.lower()

            if command in {"quit", "exit"}:
                print("\n👋 Goodbye!")
                break

            if command == "skills":
                code_generator.list_available_skills()
                continue

            if command == "open":
                project_manager.open_in_browser()
                continue

            if command == "files":
                project_manager.list_project_files()
                continue

            code_generator.execute_request(
                user_prompt=user_input,
                router=prompt_router,
            )

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted. Goodbye!")
            break

        except Exception as exc:
            print(f"\n❌ Error: {exc}")


if __name__ == "__main__":
    main()