# Smart Ollama Assistant with Code Execution

An intelligent assistant that analyzes your prompts, loads relevant skills, and **automatically implements complete projects** with code validation.

## Features

- 🧠 **Intelligent Prompt Analysis**: Determines which skills are relevant to your request
- 📚 **Dynamic Skill Loading**: Loads expertise from `.md` skill files automatically
- 🤖 **Smart Folder Naming**: Ollama decides clean project folder names
- 📁 **Complete Implementation**: Creates all project files automatically
- ✅ **Code Validation**: Validates HTML, CSS, and JavaScript
- 🌐 **Browser Preview**: Opens projects in browser automatically
- 🚫 **Code Only**: Creates HTML, CSS, JS, Python files - NO .md files

## Quick Start

### Prerequisites

1. **Ollama running** with **qwen2.5-coder:7b** model
   ```bash
   ollama list
   # If model not available:
   ollama pull qwen2.5-coder:7b
   ```

2. **Python 3.8+** with **requests** library
   ```bash
   pip install requests
   ```

### Run

```bash
python smart_assistant_executor.py
```

## How It Works

1. **You describe what you want**: "Create a portfolio page for a backend developer"
2. **Analyzes request**: Determines relevant skills to load
3. **Generates folder name**: Ollama decides → `backend_portfolio`
4. **Implements code**: Writes all HTML, CSS, JS files
5. **Validates**: Checks all files for errors
6. **Ready to use**: Opens in browser

## Example Session

```
💬 You: Create a portfolio page for a fullstack developer

🔍 Analyzing your request...
📚 Loaded skills: frontend-design

🤖 Generating implementation...
[AI generates complete code with design principles...]

============================================================
🔨 IMPLEMENTATION PHASE
============================================================

📁 Created project directory: output/fullstack_portfolio

📝 Writing files...
✅ Created: index.html
✅ Created: styles.css
✅ Created: scripts.js

🔍 Validating files...
✅ HTML Validation: All checks passed
✅ CSS Validation: Syntax valid
✅ JavaScript Validation: No errors

============================================================
✅ IMPLEMENTATION COMPLETE
============================================================

📂 Project files in fullstack_portfolio:
  📄 index.html (2145 bytes)
  📄 styles.css (1567 bytes)
  📄 scripts.js (234 bytes)

🌐 Project location: E:\py\ai\skills\output\fullstack_portfolio

💡 Next steps:
   1. Review the generated files
   2. Type 'open' to view in browser
   3. Type 'edit' to make modifications

💬 You: open

🌐 Opened index.html in browser
```

## Commands

| Command | Action |
|---------|--------|
| Your request | Generates and implements project |
| `open` | Open current project in browser |
| `files` | List all files in current project |
| `skills` | Show available skills |
| `quit` / `exit` | End session |

## Available Skills

### Frontend Design
**Loaded for**: UI, landing pages, portfolios, dashboards, web design
**Provides**: Design principles, typography, layout, color palettes, avoiding generic patterns

### Backend API
**Loaded for**: REST APIs, endpoints, server routes, authentication
**Provides**: API design patterns, security, validation, error handling

### Database Design
**Loaded for**: Database schemas, SQL, tables, queries
**Provides**: Schema design, normalization, indexes, SQL/NoSQL patterns

### Python Best Practices
**Loaded for**: Python code, scripts, performance, testing
**Provides**: Code style, type hints, testing patterns, optimization

## Smart Folder Naming

Ollama intelligently names your project folders:

| Your Prompt | Generated Folder |
|-------------|-----------------|
| create a html page of portfolio for backend developer | `backend_portfolio` |
| build a landing page for coffee shop | `landing_page` |
| make a todo app with react | `react_todo_app` |
| design dashboard for admin | `admin_dashboard` |
| create REST API for users | `user_api` |
| build python web scraper | `web_scraper` |

## Project Structure

```
skills/
├── smart_assistant_executor.py   # Main script
├── output/                       # Generated projects
│   ├── backend_portfolio/
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── scripts.js
│   ├── todo_app/
│   └── landing_page/
├── skills/                       # Skills library
│   ├── frontend-design.md
│   ├── backend-api.md
│   ├── database-design.md
│   └── python-best-practices.md
└── README.md
```

## What Gets Created

### Web Projects
- `index.html` - Main HTML file
- `styles.css` - Styling
- `scripts.js` - JavaScript functionality

### Python Projects
- `main.py` - Main script
- Additional `.py` files as needed

### Config Files
- `package.json` - If Node.js project
- `requirements.txt` - If Python project

### NOT Created
- ❌ .md files (documentation)
- ❌ README files
- ✅ Only code files

## Configuration

### Change Model
```python
client = ExecutorOllamaClient(model="qwen2.5-coder:3b")
```

### Change Output Directory
```python
executor = CodeExecutor(output_dir="my_projects")
```

### Change Ollama URL
```python
client = ExecutorOllamaClient(base_url="http://your-server:11434")
```

## Validation Features

- **HTML**: DOCTYPE, structure, proper tags
- **CSS**: Syntax, rules, selectors
- **JavaScript**: Syntax checking (with Node.js if available)

## Troubleshooting

### "Error communicating with Ollama"
Check Ollama is running: `ollama list`

### "No code blocks found in response"
Be more specific: "Create a complete HTML portfolio page"

### Folder name unclear
Ollama generates the name. If unsatisfied, manually rename in `output/` folder

### Browser won't open
Manually open `output/project_name/index.html` in your browser

### Skills not loading
Check `skills/` folder exists and contains `.md` files

## Example Prompts

```
Create a portfolio page for a photographer
Build a landing page for a yoga studio
Make a todo list app with dark mode
Design a dashboard for analytics
Create a contact form with validation
Build a calculator app
Make a weather app with API integration
```

## Tips

1. **Be specific** - "Create a dark-themed portfolio with project cards" vs "Make a website"
2. **Review generated code** - Always check before deploying
3. **Use 'open' command** - Instantly preview in browser
4. **Iterate quickly** - Generate, review, request changes

## Performance

- Initial analysis: ~2-3 seconds
- Folder naming: ~1-2 seconds  
- Code generation: 10-30 seconds (depends on complexity)
- File creation: <1 second
- Total: ~15-35 seconds for complete project

## Requirements

- Python 3.8+
- requests library (`pip install requests`)
- Ollama with qwen2.5-coder:7b model
- Optional: Node.js (for JavaScript validation)

## License

See LICENSE.txt for complete terms.
