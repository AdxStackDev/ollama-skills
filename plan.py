#!/usr/bin/env python3
"""
Smart Ollama Assistant with Skill Routing
Analyzes user prompts and loads relevant skills automatically
"""

import requests
import json
import os
from pathlib import Path
from typing import Optional, Generator, List, Dict


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
        # Try exact match on ID
        if name in self.skills:
            return self.skills[name]
        
        # Try match on skill name
        for skill_id, skill in self.skills.items():
            if skill['name'].lower() == name.lower():
                return skill
        
        return None


class SmartOllamaClient:
    """Ollama client with intelligent skill routing"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5-coder:7b"):
        self.base_url = base_url
        self.model = model
        self.skill_manager = SkillManager()
    
    def analyze_prompt(self, user_prompt: str) -> List[str]:
        """
        Analyze user prompt to determine which skills to load
        Returns list of skill names
        """
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
            
            # Parse the response
            if result == "none" or not result:
                return []
            
            # Extract skill names
            skills = [s.strip() for s in result.split(',')]
            return skills
            
        except Exception as e:
            print(f"Error analyzing prompt: {e}")
            return []
    
    def chat_with_skills(self, user_prompt: str, skill_names: List[str] = None) -> Generator[str, None, None]:
        """
        Chat with automatically loaded skills
        
        Args:
            user_prompt: User's question/request
            skill_names: Optional list of skill names to load (if None, auto-analyze)
        """
        # Auto-analyze if skills not specified
        if skill_names is None:
            print("🔍 Analyzing your request...")
            skill_names = self.analyze_prompt(user_prompt)
        
        # Load relevant skills
        loaded_skills = []
        skill_context = ""
        
        for skill_name in skill_names:
            skill = self.skill_manager.get_skill_by_name(skill_name)
            if skill:
                loaded_skills.append(skill['name'])
                skill_context += f"\n\n=== SKILL: {skill['name']} ===\n{skill['content']}\n"
        
        if loaded_skills:
            print(f"📚 Loaded skills: {', '.join(loaded_skills)}")
        else:
            print("💬 No specific skills loaded - using base model")
        
        # Build the final prompt
        if skill_context:
            final_prompt = f"""{skill_context}

=== USER REQUEST ===
{user_prompt}

Please respond to the user's request following the guidance in the loaded skills above."""
        else:
            final_prompt = user_prompt
        
        # Generate response
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": final_prompt,
            "stream": True
        }
        
        try:
            response = requests.post(url, json=data, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
                    if chunk.get("done", False):
                        break
                        
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Error communicating with Ollama: {e}")
    
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
            print(f"  Path: {skill['path']}")
        
        print("\n" + "=" * 60)


def main():
    """Main application entry point"""
    client = SmartOllamaClient()
    
    print("=" * 60)
    print("🤖 Smart Ollama Assistant with Skill Routing")
    print("=" * 60)
    print("Commands:")
    print("  - Type your question/request normally")
    print("  - 'skills' - List all available skills")
    print("  - 'quit' or 'exit' - End the session")
    print("=" * 60)
    
    # Show available skills on startup
    client.list_available_skills()
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'skills':
                client.list_available_skills()
                continue
            
            # Process with skill routing
            print("\n🤖 Assistant: ", end="", flush=True)
            
            for chunk in client.chat_with_skills(user_input):
                print(chunk, end="", flush=True)
            
            print("\n")  # New line after response
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
