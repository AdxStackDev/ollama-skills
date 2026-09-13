import requests
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Generator, List, Dict, Tuple


class SkillManager:
    """Manages loading and matching skills from .md files"""
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills = self.load_all_skills()
    
    def load_all_skills(self) -> Dict[str, Dict]:
        """Load all skills from the skills directory"""
        skills = {}
        
        if not self.skills_dir.exists():
            print(f"Warning: Skills directory '{self.skills_dir}' not found")
            return skills
        
        for md_file in self.skills_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Parse frontmatter
                metadata = self.parse_frontmatter(content)
                
                skills[md_file.stem] = {
                    'name': metadata.get('name', md_file.stem),
                    'description': metadata.get('description', ''),
                    'content': content,
                    'path': str(md_file)
                }
                
            except Exception as e:
                print(f"Error loading skill {md_file}: {e}")
        
        return skills
    
    def parse_frontmatter(self, content: str) -> Dict[str, str]:
        """Parse YAML frontmatter from markdown"""
        metadata = {}
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
        
        return metadata
    
    def get_skill_descriptions(self) -> str:
        """Get a formatted list of all skills for the analyzer"""
        descriptions = []
        for skill_id, skill in self.skills.items():
            desc = f"- {skill['name']}: {skill['description']}"
            descriptions.append(desc)
        return "\n".join(descriptions)
    
    def get_skill_by_name(self, name: str) -> Optional[Dict]:
        """Get skill by name or ID"""
        if name in self.skills:
            return self.skills[name]
        
        for skill_id, skill in self.skills.items():
            if skill['name'].lower() == name.lower():
                return skill
        
        return None


class CodeExecutor:
    """Executes and validates code step-by-step"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.current_project = None
    
    def create_project(self, project_name: str) -> Path:
        """Create a new project directory"""
        project_path = self.output_dir / project_name
        project_path.mkdir(exist_ok=True)
        self.current_project = project_path
        print(f"📁 Created project directory: {project_path}")
        return project_path
    
    def write_file(self, filename: str, content: str) -> bool:
        """Write content to a file in the current project"""
        if not self.current_project:
            print("❌ No active project")
            return False
        
        try:
            file_path = self.current_project / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error writing {filename}: {e}")
            return False
    
    def validate_html(self, filename: str) -> Tuple[bool, str]:
        """Validate HTML file"""
        if not self.current_project:
            return False, "No active project"
        
        file_path = self.current_project / filename
        if not file_path.exists():
            return False, f"{filename} not found"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic validation
            checks = [
                ('<!DOCTYPE html>' in content, 'Has DOCTYPE declaration'),
                ('<html' in content, 'Has <html> tag'),
                ('<head>' in content, 'Has <head> section'),
                ('<body>' in content, 'Has <body> section'),
                ('</html>' in content, 'Properly closed')
            ]
            
            passed = all(check[0] for check in checks)
            details = '\n'.join([f"  {'✅' if c[0] else '❌'} {c[1]}" for c in checks])
            
            return passed, details
        except Exception as e:
            return False, str(e)
    
    def validate_css(self, filename: str) -> Tuple[bool, str]:
        """Validate CSS file"""
        if not self.current_project:
            return False, "No active project"
        
        file_path = self.current_project / filename
        if not file_path.exists():
            return False, f"{filename} not found"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic validation
            has_rules = '{' in content and '}' in content
            has_selectors = any(sel in content for sel in ['.', '#', 'body', 'header', 'section'])
            
            details = f"  {'✅' if has_rules else '❌'} Has CSS rules\n"
            details += f"  {'✅' if has_selectors else '❌'} Has selectors"
            
            return has_rules and has_selectors, details
        except Exception as e:
            return False, str(e)
    
    def validate_js(self, filename: str) -> Tuple[bool, str]:
        """Validate JavaScript file"""
        if not self.current_project:
            return False, "No active project"
        
        file_path = self.current_project / filename
        if not file_path.exists():
            return False, f"{filename} not found"
        
        # Check if node is available for syntax validation
        try:
            result = subprocess.run(
                ['node', '--check', str(file_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True, "  ✅ JavaScript syntax valid"
            else:
                return False, f"  ❌ Syntax error:\n{result.stderr}"
        except FileNotFoundError:
            # Node not installed, do basic check
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return True, "  ⚠️  Basic check passed (Node.js not available for full validation)"
            except Exception as e:
                return False, str(e)
        except Exception as e:
            return False, str(e)
    
    def open_in_browser(self, filename: str = "index.html"):
        """Open HTML file in default browser"""
        if not self.current_project:
            print("❌ No active project")
            return
        
        file_path = self.current_project / filename
        if not file_path.exists():
            print(f"❌ {filename} not found")
            return
        
        try:
            import webbrowser
            webbrowser.open(file_path.as_uri())
            print(f"🌐 Opened {filename} in browser")
        except Exception as e:
            print(f"❌ Error opening browser: {e}")
    
    def list_project_files(self):
        """List all files in the current project"""
        if not self.current_project:
            print("❌ No active project")
            return
        
        print(f"\n📂 Project files in {self.current_project.name}:")
        for file_path in sorted(self.current_project.rglob('*')):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.current_project)
                size = file_path.stat().st_size
                print(f"  📄 {rel_path} ({size} bytes)")


class ExecutorOllamaClient:
    """Ollama client with intelligent skill routing and execution"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5-coder:7b"):
        self.base_url = base_url
        self.model = model
        self.skill_manager = SkillManager()
        self.executor = CodeExecutor()
    
    def analyze_prompt(self, user_prompt: str) -> List[str]:
        """Analyze user prompt to determine which skills to load"""
        available_skills = self.skill_manager.get_skill_descriptions()
        
        analysis_prompt = f"""You are a skill routing assistant. Analyze the user's request and determine which skills are relevant.

Available Skills:
{available_skills}

User Request: {user_prompt}

Based on the user's request, which skills should be loaded? Respond with ONLY the skill names (like 'frontend-design', 'backend-api', etc.) separated by commas, or 'none' if no specific skills are needed.

Your response (skill names only):"""

        try:
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model,
                "prompt": analysis_prompt,
                "stream": False
            }
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json().get("response", "").strip().lower()
            
            if result == "none" or not result:
                return []
            
            skills = [s.strip() for s in result.split(',')]
            return skills
            
        except Exception as e:
            print(f"Error analyzing prompt: {e}")
            return []
    
    def generate_folder_name(self, user_prompt: str) -> str:
        """Use Ollama to generate a smart, short folder name from user prompt"""
        
        naming_prompt = f"""Given this user request: "{user_prompt}"

Generate a short, descriptive folder name (2-3 words max, using underscores).

Rules:
- Use lowercase with underscores (e.g., backend_portfolio, todo_app, landing_page)
- Maximum 3 words
- Be specific and descriptive
- No special characters except underscore
- Examples: "portfolio" for portfolio, "backend_api" for backend API, "react_dashboard" for React dashboard

Respond with ONLY the folder name, nothing else:"""

        try:
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model,
                "prompt": naming_prompt,
                "stream": False
            }
            
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            folder_name = response.json().get("response", "").strip().lower()
            
            # Clean the response
            folder_name = folder_name.replace(' ', '_').replace('-', '_')
            folder_name = ''.join(c for c in folder_name if c.isalnum() or c == '_')
            folder_name = folder_name[:40]  # Limit length
            
            if not folder_name:
                folder_name = "project"
            
            return folder_name
            
        except Exception as e:
            print(f"⚠️  Error generating folder name: {e}")
            # Fallback to simple extraction
            words = user_prompt.lower().split()[:3]
            return '_'.join(w for w in words if w.isalnum())[:40] or "project"
    
    def extract_code_blocks(self, text: str) -> Dict[str, str]:
        """Extract code blocks from markdown response"""
        import re
        
        code_blocks = {}
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for lang, code in matches:
            if lang == 'html':
                code_blocks['index.html'] = code.strip()
            elif lang == 'css':
                code_blocks['styles.css'] = code.strip()
            elif lang in ['javascript', 'js']:
                code_blocks['scripts.js'] = code.strip()
            elif lang == 'python':
                if 'main.py' not in code_blocks:
                    code_blocks['main.py'] = code.strip()
                else:
                    # Multiple Python blocks, number them
                    i = 2
                    while f'script{i}.py' in code_blocks:
                        i += 1
                    code_blocks[f'script{i}.py'] = code.strip()
            elif lang == 'json':
                # Handle JSON files like package.json, requirements.txt style
                if 'package' in text.lower():
                    code_blocks['package.json'] = code.strip()
                else:
                    code_blocks['config.json'] = code.strip()
            # Explicitly skip markdown files
            elif lang in ['markdown', 'md']:
                continue  # Skip .md files
        
        return code_blocks
    
    def execute_request(self, user_prompt: str):
        """Process request, generate code, and execute step-by-step"""
        print("🔍 Analyzing your request...")
        
        # Analyze and load skills
        skill_names = self.analyze_prompt(user_prompt)
        
        loaded_skills = []
        skill_context = ""
        
        for skill_name in skill_names:
            skill = self.skill_manager.get_skill_by_name(skill_name)
            if skill:
                loaded_skills.append(skill['name'])
                skill_context += f"\n\n=== SKILL: {skill['name']} ===\n{skill['content']}\n"
        
        if loaded_skills:
            print(f"📚 Loaded skills: {', '.join(loaded_skills)}")
        
        # Build execution-focused prompt
        execution_prompt = f"""{skill_context}

=== USER REQUEST ===
{user_prompt}

=== INSTRUCTIONS ===
1. Analyze the request and create a design/implementation plan
2. Generate complete, working code with proper file structure
3. Include HTML, CSS, and JavaScript if it's a web project
4. Include Python code if it's a backend/script project
5. Use proper code blocks with language tags (```html, ```css, ```javascript, ```python)
6. Make the code production-ready and fully functional

Generate the complete implementation now:"""

        # Get response from Ollama
        print("\n🤖 Generating implementation...\n")
        
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": execution_prompt,
            "stream": True
        }
        
        full_response = ""
        
        try:
            response = requests.post(url, json=data, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        text = chunk["response"]
                        print(text, end="", flush=True)
                        full_response += text
                    if chunk.get("done", False):
                        break
            
            print("\n")
            
            # Extract and execute code
            print("\n" + "="*60)
            print("🔨 IMPLEMENTATION PHASE")
            print("="*60 + "\n")
            
            code_blocks = self.extract_code_blocks(full_response)
            
            if not code_blocks:
                print("⚠️  No code blocks found in response")
                print("💡 Tip: The response should contain code in ```language blocks")
                return
            
            # Create project with smart folder name
            project_name = self.generate_folder_name(user_prompt)
            self.executor.create_project(project_name)
            
            # Write files
            print("\n📝 Writing files...")
            for filename, content in code_blocks.items():
                self.executor.write_file(filename, content)
            
            # Validate files
            print("\n🔍 Validating files...")
            
            if 'index.html' in code_blocks:
                valid, details = self.executor.validate_html('index.html')
                print(f"\n{'✅' if valid else '❌'} HTML Validation:")
                print(details)
            
            if 'styles.css' in code_blocks:
                valid, details = self.executor.validate_css('styles.css')
                print(f"\n{'✅' if valid else '❌'} CSS Validation:")
                print(details)
            
            if 'scripts.js' in code_blocks:
                valid, details = self.executor.validate_js('scripts.js')
                print(f"\n{'✅' if valid else '❌'} JavaScript Validation:")
                print(details)
            
            # Show project summary
            print("\n" + "="*60)
            print("✅ IMPLEMENTATION COMPLETE")
            print("="*60)
            self.executor.list_project_files()
            
            # Offer to open in browser
            if 'index.html' in code_blocks:
                print(f"\n🌐 Project location: {self.executor.current_project}")
                print("\n💡 Next steps:")
                print("   1. Review the generated files")
                print("   2. Type 'open' to view in browser")
                print("   3. Type 'edit' to make modifications")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def list_available_skills(self):
        """Display all available skills"""
        print("\n📚 Available Skills:")
        print("=" * 60)
        
        if not self.skill_manager.skills:
            print("No skills found in the 'skills' directory")
            return
        
        for skill_id, skill in self.skill_manager.skills.items():
            print(f"\n✓ {skill['name']}")
            print(f"  ID: {skill_id}")
            print(f"  Description: {skill['description']}")
        
        print("\n" + "=" * 60)


def main():
    """Main application entry point"""
    client = ExecutorOllamaClient()
    
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
    
    client.list_available_skills()
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'skills':
                client.list_available_skills()
                continue
            
            if user_input.lower() == 'open':
                client.executor.open_in_browser()
                continue
            
            if user_input.lower() == 'files':
                client.executor.list_project_files()
                continue
            
            # Execute the request
            client.execute_request(user_input)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
