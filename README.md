# AI Context Optimizer

A lightweight, modular toolkit designed to drastically reduce the "discovery phase" time of autonomous AI coding agents (like Antigravity, AutoGPT, or local LLMs). 

By default, AI agents use native, asynchronous tool-calling to list directories and read files one by one. In large projects, this loop can take up to 40 minutes just to build context. This toolkit pre-compiles your project's architecture and file contents into a single, clean, AI-readable XML format in seconds.

## 🛠️ The Tools

The toolkit consists of two main entry points, powered by a shared library in `src/`:

### 1. `read_folder.py` (The Global Scanner)
Generates an ASCII tree of your project and extracts the contents of all valid files.

```bash
# Basic usage
python read_folder.py

# With manual exclusions and .gitignore support
python read_folder.py . --exclude node_modules --exclude .venv --exclude-gitignore
```

### 2. `read_files.py` (The Targeted Reader)
Reads only a specific list of files provided via a text file (preset).

```bash
# Reads paths from the default 'list.txt'
python read_files.py --exclude-gitignore

# Reads paths from a custom preset
python read_files.py presets/notifications.txt --exclude-gitignore
```

---

## 🚀 Highly Effective Workflows

To get the best speed and accuracy out of your AI agent, follow this methodology:

### Phase 1: The Global Scan (Architecture First)
**When to use:** At the start of a new feature, when refactoring, or when fixing bugs that span multiple modules.

**Why:** Agents often hallucinate imports or misunderstand the data flow if they don't see the big picture. 

**Action:** Run `python read_folder.py --exclude-gitignore`. Feed the generated `out_XXX.txt` to the AI and force it to rely *only* on this file for its architectural understanding. This prevents the agent from falling back into its slow, manual folder-browsing habits.

### Phase 2: Domain-Specific Presets (The "Sniper" Approach)
**When to use:** For iterative updates, isolated bug fixes, or extending an existing feature.

**Why:** Once the AI knows the architecture, feeding it the entire project for every small prompt wastes token context and slows down response times.

**Action:** Create thematic text files (presets) containing paths to highly coupled files. 

*Examples of presets:*
* `presets/auth.txt` (contains paths to `login.py`, `models/user.py`, `middleware/auth.py`)
* `presets/notifications.txt` (contains paths to `email_service.py`, `templates/alert.html`)

Run `python read_files.py presets/auth.txt` and provide the output to the AI. It will instantly have the exact context needed to implement the feature without reading thousands of irrelevant lines of code.

---

## 🤖 Instructions for AI Agents

*(Note for the user: Copy-paste this block into your initial prompt or set it as a global "Rule" in your agent's configuration).*

**CRITICAL DIRECTIVES FOR THE AI AGENT:**

1. **Do not use native file-search tools:** You are in an optimized workspace. Do not use your asynchronous tools to iteratively list directories or read files to discover the project.
2. **Use the compiled context:** - If you need to understand the whole project, execute `python read_folder.py --exclude-gitignore` and read the resulting `out_*.txt` file.
   - If you need to focus on specific files, write their paths into a file (e.g., `list.txt`), execute `python read_files.py list.txt`, and read the output.
3. **Understand the format:** The output is formatted with `<project_tree>`, `<file_contents>`, and `<file path="...">` XML tags. Use these boundaries to accurately isolate code blocks.
