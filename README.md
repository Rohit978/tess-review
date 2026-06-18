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
- An OpenRouter API Key (It uses `qwen/qwen-2.5-coder-32b-instruct:free` by default because we like good code and we like keeping our money).

### Setup
1. Clone the repo (you know the drill):
   ```bash
   git clone https://github.com/yourusername/code-reviewer.git
   cd code-reviewer
   ```

2. Install it locally:
   ```bash
   pip install -e .
   ```
   *Boom.* Now you have `tess-review` and `tess` installed as global commands.

---

## 🚀 Usage

### 1. Give it the API Key
It needs to eat. Feed it your OpenRouter API key via environment variables:

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="your-key-here"
```

**Windows (CMD):**
```cmd
set OPENROUTER_API_KEY=your-key-here
```

**Linux/macOS:**
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### 2. Change the Model (Optional)
TESS uses `qwen/qwen3-coder:free` by default. If you want to use a different OpenRouter model (like Claude 3.5 Sonnet or GPT-4o), just set the `TESS_MODEL` environment variable before running it:

**Windows (PowerShell):**
```powershell
$env:TESS_MODEL="anthropic/claude-3.5-sonnet"
```
**Linux/macOS:**
```bash
export TESS_MODEL="anthropic/claude-3.5-sonnet"
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
