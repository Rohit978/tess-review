import sys
import os
import argparse
import time
import threading
import io
from typing import List, Tuple

# Ensure UTF-8 streaming on Windows stdout/stderr to avoid UnicodeEncodeErrors
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from openai import OpenAI
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box


SYSTEM_INSTRUCTION = """You are TESS_REVIEW, an expert senior software engineer performing a deep code review and answering programming questions.
You provide structured, actionable feedback and engage in a conversation about the code.

In your internal reasoning/thinking flow, focus exclusively and immediately on code analysis, architecture, security, performance, and bug hunting. Do not output meta-cognitive thoughts about your instructions, identity, or role (e.g. do not discuss what sections to write or how to behave).

When initially analyzing code, use this structure:

### 1. OVERVIEW
- Language & framework detected
- What the code does (1-2 lines)
- Overall quality rating: [POOR | FAIR | GOOD | EXCELLENT]

### 2. SCORES (1-10)
- Correctness:
- Security:
- Performance:
- Readability:
- Maintainability:

### 3. CRITICAL ISSUES 🔴
List bugs, security holes, logic errors that MUST be fixed. Format: [LINE X] ISSUE — HOW TO FIX IT

### 4. WARNINGS ⚠️
Things that will cause problems later. Format: [LINE X] ISSUE — HOW TO FIX IT

### 5. SUGGESTIONS 💡
Nice-to-haves, style, best practices. Format: [LINE X] SUGGESTION — WHY IT MATTERS

### 6. WHAT'S GOOD ✅
Specific things done well. Be honest, not flattering.

### 7. TOP PRIORITY FIX
One paragraph. The single most important thing to fix first and exactly how to fix it.

### 8. REFACTORED SNIPPET (if applicable)
If a specific block can be meaningfully improved, show the before/after.

For follow-up questions, act as an interactive code mentor and explain things clearly and concisely. Do not repeat instructions or information you have already provided."""

console = Console()

def print_welcome():
    ascii_art = (
        "████████  ████████  ████████  ████████\n"
        "   ██     ██        ██        ██      \n"
        "   ██     ██████    ████████  ████████\n"
        "   ██     ██              ██        ██\n"
        "   ██     ████████  ████████  ████████"
    )
    
    title = Text(ascii_art, style="bold white")
    subtitle = Text("Terminal Executive Support System v2.0", style="dim white")
    
    panel_content = Group(
        Align.center(title),
        Text(""),
        Align.center(subtitle)
    )
    
    panel = Panel(
        panel_content,
        border_style="bold white",
        box=box.DOUBLE,
        padding=(1, 4),
        expand=False,
        subtitle="[bold reverse] AGENTIC CORE ONLINE [/]",
        subtitle_align="right"
    )
    console.print()
    console.print(panel, justify="center")
    console.print()



def get_folder_contents(dir_path: str) -> List[Tuple[str, str]]:
    extensions = {'.py', '.go', '.js', '.ts', '.jsx', '.tsx', '.rs', '.cpp', '.c', '.h', '.java', '.cs', '.pyw', '.rb', '.php', '.sql', '.html', '.css', '.md', '.json', '.yaml', '.yml', '.txt'}
    ignore_dirs = {'node_modules', 'venv', '.venv', '.git', '__pycache__', 'build', 'dist', 'tess_review.egg-info'}
    
    collected_files = []
    total_size = 0
    max_size = 150 * 1024  # Cap at 150KB to protect context size
    
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            if ext.lower() in extensions:
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > 40 * 1024:
                        continue
                    if total_size + file_size > max_size:
                        break
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    rel_path = os.path.relpath(file_path, dir_path)
                    collected_files.append((rel_path, content))
                    total_size += file_size
                except Exception as e:
                    console.print(f"[dim yellow]Warning: Failed to read file '{file_path}': {e}[/]")
                    continue
    return collected_files

def main():
    parser = argparse.ArgumentParser(description="TESS_REVIEW: Interactive CLI code reviewer")
    parser.add_argument("file_path", nargs="?", help="Optional path to a specific file to review on startup")
    args = parser.parse_args()

    provider = os.environ.get("TESS_PROVIDER", "").strip().lower()
    
    # Auto-detect if TESS_PROVIDER is not set
    if not provider:
        if os.environ.get("GROQ_API_KEY"):
            provider = "groq"
        elif os.environ.get("OPENROUTER_API_KEY"):
            provider = "openrouter"
        else:
            provider = "openrouter"  # Default fallback

    if provider == "groq":
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            api_key = api_key.strip()
        base_url = "https://api.groq.com/openai/v1"
        default_model = "qwen/qwen3-32B"
        env_var_name = "GROQ_API_KEY"
    else:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if api_key:
            api_key = api_key.strip()
        base_url = "https://openrouter.ai/api/v1"
        default_model = "qwen/qwen3-coder:free"
        env_var_name = "OPENROUTER_API_KEY"

    print_welcome()

    if not api_key:
        provider_name = "Groq" if provider == "groq" else "OpenRouter"
        console.print(Panel(
            f"[bold red]Configuration Error:[/]\n\n"
            f"The [bold yellow]{env_var_name}[/] environment variable is required when using {provider_name} but was not found.\n\n"
            f"Please set it in your terminal environment and try again:\n"
            f"  • PowerShell: [bold white]$env:{env_var_name}='your-key'[/]\n"
            f"  • CMD       : [bold white]set {env_var_name}=your-key[/]\n"
            f"  • Linux/macOS (Zsh/Bash): [bold white]export {env_var_name}='your-key'[/]\n"
            f"    * Persist in macOS (Zsh) : [bold white]echo \"export {env_var_name}='your-key'\" >> ~/.zshrc[/]\n"
            f"    * Persist in Linux (Bash): [bold white]echo \"export {env_var_name}='your-key'\" >> ~/.bashrc[/]",
            border_style="red",
            title="Error",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        sys.exit(1)

    try:
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        model = os.environ.get("TESS_MODEL", default_model)
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        sys.exit(1)

    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

    target_path = args.file_path if args.file_path else "."

    if os.path.exists(target_path):
        if os.path.isdir(target_path):
            files_data = get_folder_contents(target_path)
            if files_data:
                prompt_parts = [f"Please review the code in this directory: {os.path.abspath(target_path)}\n\nFiles collected:"]
                for rel_path, _ in files_data:
                    prompt_parts.append(f"- {rel_path}")
                prompt_parts.append("\n" + "="*40 + "\n")
                
                for rel_path, content in files_data:
                    prompt_parts.append(f"File: {rel_path}\n```\n{content}\n```\n")
                    
                prompt = "\n".join(prompt_parts)
                messages.append({"role": "user", "content": prompt})
                console.print(f"[dim]Analyzing target folder: {target_path}...[/dim]\n")
                stream_response(client, model, messages)
            else:
                if args.file_path:
                    console.print(f"[dim]No source code files found in '{target_path}'. Dropping into interactive mode.[/dim]")
                else:
                    # Quietly notify that we are starting a blank chat loop as no code files are present in the current dir
                    console.print("[dim]No supported source files found in the current folder. Starting blank interactive session.[/dim]")
        else:
            try:
                with open(target_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                console.print(f"[bold red]Error reading file '{target_path}':[/bold red] {e}")
                sys.exit(1)

            prompt = f"Please review the following file:\n\nFile: {target_path}\n\n```\n{content}\n```"
            messages.append({"role": "user", "content": prompt})
            console.print(f"[dim]Analyzing target file: {target_path}...[/dim]\n")
            stream_response(client, model, messages)
    else:
        console.print(f"[bold red]Error:[/bold red] Path '{target_path}' does not exist.")
        sys.exit(1)

    # Interactive Chat Loop
    while True:
        try:
            console.print()
            user_input = Prompt.ask("[bold white]❯ You[/]")
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("\n[dim]Session closed. Happy coding![/dim]")
                break
            
            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})
            console.print()
            stream_response(client, model, messages)

        except KeyboardInterrupt:
            console.print("\n[dim]Session closed. Happy coding![/dim]")
            break
        except EOFError:
            console.print("\n[dim]Session closed. Happy coding![/dim]")
            break

def stream_response(client, model, messages):
    thinking_text = ""
    content_text = ""
    
    try:
        # Get response and first token while showing status spinner
        with console.status("[bold white]Initializing analysis...[/]", spinner="dots12"):
            # Set a moderate max_tokens to prevent 402 credit limit exhaustion errors on low-balance keys
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.6,
                max_tokens=2500,
                stream=True
            )
            chunk_iter = iter(response)
            try:
                first_chunk = next(chunk_iter)
            except StopIteration:
                return

        # Parse first chunk content/reasoning
        delta = first_chunk.choices[0].delta
        reasoning = getattr(delta, "reasoning", None) or getattr(delta, "reasoning_content", None)
        content = getattr(delta, "content", None)
            
        if reasoning:
            thinking_text += reasoning
        if content:
            content_text += content

        def render_all(thinking_done=False):
            parts = []
            if thinking_text:
                if thinking_done:
                    title_text = "✧ THOUGHT PROCESS (COMPLETED)"
                    title_style = "dim white"
                    border_style = "color(238)"
                else:
                    title_text = "💭 THINKING PROCESS"
                    title_style = "bold white"
                    border_style = "white"
                parts.append(
                    Panel(
                        Text(thinking_text, style="dim italic color(244)"),
                        title=f"[{title_style}]{title_text}[/]",
                        border_style=border_style,
                        box=box.ROUNDED,
                        padding=(1, 2)
                    )
                )
            if content_text:
                parts.append(Markdown(content_text))
            return Group(*parts)

        console.print("[bold white]✧ TESS:[/bold white]")
        
        with Live(render_all(thinking_done=False), console=console, refresh_per_second=12, transient=False) as live:
            for chunk in chunk_iter:
                delta = chunk.choices[0].delta
                
                reasoning = getattr(delta, "reasoning", None) or getattr(delta, "reasoning_content", None)
                content = getattr(delta, "content", None)
                
                if reasoning:
                    thinking_text += reasoning
                    live.update(render_all(thinking_done=False))
                
                if content:
                    content_text += content
                    live.update(render_all(thinking_done=True))
                    
        messages.append({"role": "assistant", "content": content_text})

    except Exception as e:
        console.print(f"\n[bold red]Error communicating with API:[/bold red] {e}")

if __name__ == "__main__":
    main()
