# TESS_REVIEW 🤖💼

Look, I didn't want to build this. I really didn't. But after staring at one too many pull requests that made me question my career choices, and waiting forever for human code reviews that just said "LGTM 👍", I snapped. 

Thus, **TESS_REVIEW** (Terminal Executive Support System) was born out of sheer, unadulterated necessity. 

It's an interactive, completely overly-professional CLI code reviewer that lives right in your terminal. It judges your code, streams its deep reasoning (so you can see exactly how disappointed it is), and gives you actionable feedback without ever having to switch to a browser. 

---

## ✨ Features (Because we need bullet points)

- **Cognitive Flow Output:** It streams its internal thinking live in a neat little panel. It's like watching a senior dev sigh deeply before telling you why your variable names are terrible.
- **Folder & File Analysis:** Run it on a single file or a whole directory. It knows what to ignore (I'm looking at you, `node_modules` and `venv`).
- **Interactive Chat Loop:** After it tears your code apart, you can actually argue with it. Or politely ask it for refactoring snippets. 
- **Grayscale Professional Design:** Styled with a clean double-bordered layout. Because if it's going to judge my code, it should do it in a sleek, retro, black-and-white aesthetic.
- **Windows Unicode-Safe:** I suffered through enough `UnicodeEncodeError` crashes on Windows CMD so you don't have to.

---

## 🛠️ How to get this thing running

### Prerequisites
- Python 3.8+ (Welcome to the present)
- An API Key from either OpenRouter or Groq:
  - **OpenRouter**: Default model is `qwen/qwen3-coder:free`.
  - **Groq**: Default model is `qwen/qwen3-32B`.

### Setup

#### Option A: macOS & Linux (One-Click Virtual Env Installer)
Modern macOS and Linux environments block global `pip` installation by default (PEP 668). We provide an `install.sh` script that automatically creates a Python virtual environment and installs the packages safely:

1. Clone the repo (you know the drill):
   ```bash
   git clone https://github.com/yourusername/code-reviewer.git
   cd code-reviewer
   ```
2. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
This will set up everything inside a local `.venv/` directory and print setup instructions for your shell.

#### Option B: Global Install via pipx (Recommended for macOS/Linux)
If you want `tess` to be globally accessible without managing shell aliases:
1. Install `pipx` (if you don't have it):
   ```bash
   brew install pipx   # macOS
   pipx ensurepath
   ```
2. Install TESS:
   ```bash
   pipx install .
   ```

#### Option C: Windows Install
1. Clone the repo and run:
   ```powershell
   pip install -e .
   ```
   *Boom.* Now you have `tess-review` and `tess` installed as global commands.

---

## 🚀 Usage

### 1. Configure your LLM Provider and API Key
It needs to eat. Configure the active provider and its API key via environment variables.

#### Option A: OpenRouter (Default)
**Windows (PowerShell):**
```powershell
$env:TESS_PROVIDER="openrouter"
$env:OPENROUTER_API_KEY="your-key-here"
```

**Windows (CMD):**
```cmd
set TESS_PROVIDER=openrouter
set OPENROUTER_API_KEY=your-key-here
```

**macOS/Linux (Zsh - Default):**
```bash
export TESS_PROVIDER="openrouter"
export OPENROUTER_API_KEY="your-key-here"
```

#### Option B: Groq
**Windows (PowerShell):**
```powershell
$env:TESS_PROVIDER="groq"
$env:GROQ_API_KEY="your-key-here"
```

**Windows (CMD):**
```cmd
set TESS_PROVIDER=groq
set GROQ_API_KEY=your-key-here
```

**macOS/Linux (Zsh - Default):**
```bash
export TESS_PROVIDER="groq"
export GROQ_API_KEY="your-key-here"
```

*(Note: If `TESS_PROVIDER` is not set, TESS will automatically detect which provider to use based on the presence of `GROQ_API_KEY` or `OPENROUTER_API_KEY`.)*

### 2. Change the Model (Optional)
TESS defaults to `qwen/qwen3-coder:free` (OpenRouter) or `qwen/qwen3-32B` (Groq). If you want to use a different model, set the `TESS_MODEL` environment variable:

**Windows (PowerShell):**
```powershell
$env:TESS_MODEL="your-chosen-model-id"
```
**macOS/Linux:**
```bash
export TESS_MODEL="your-chosen-model-id"
```

### 3. Judge some code
Point it at a file, or just run it in an entire directory. Don't worry, I added a 150KB hard cap so you don't accidentally send your entire 2GB monorepo to the API:
```bash
tess-review spaghetti_code.py
```
Or just run it blindly in your current folder:
```bash
tess
```

It will print a fancy ASCII banner, analyze the code, output scores (prepare your ego), and drop you into an interactive `❯ You` prompt to chat.

---

## 🧱 What's it built on?
- **openai**: To talk to OpenRouter seamlessly.
- **rich**: Because standard terminal output is boring and I wanted markdown, tables, and spinners.
- **setuptools**: So you can just type `tess` anywhere.

Enjoy. Or don't. But at least your code will be better.
