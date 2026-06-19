#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "==========================================="
echo "   TESS_REVIEW macOS/Linux Installer        "
echo "==========================================="

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Please install Python 3 using Homebrew:"
        echo "  brew install python"
    else
        echo "Please install Python 3 using your package manager."
    fi
    exit 1
fi

# Get absolute path of this script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

# 2. Create Virtual Environment if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv .venv
else
    echo "Virtual environment .venv already exists."
fi

# 3. Activate venv and install
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements and package in editable/development mode..."
pip install -e .

echo "==========================================="
echo "🎉 Installation Successful!"
echo "==========================================="

# 4. Prompt for LLM Provider
echo ""
echo "-------------------------------------------"
echo "🤖 LLM Provider Configuration"
echo "-------------------------------------------"
echo "Select your preferred LLM Provider:"
echo "  1) OpenRouter (default)"
echo "  2) Groq"
read -p "Enter choice (1 or 2): " provider_choice
provider_choice=${provider_choice:-1}

shell_config=""
# Auto-detect shell config
if [[ "$SHELL" == */zsh ]]; then
    shell_config="$HOME/.zshrc"
elif [[ "$SHELL" == */bash ]]; then
    shell_config="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    shell_config="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    shell_config="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    shell_config="$HOME/.bash_profile"
else
    shell_config="$HOME/.profile"
fi

if [ "$provider_choice" = "2" ]; then
    read -p "Enter your Groq API Key (press Enter to skip): " user_api_key
    if [ -n "$user_api_key" ]; then
        echo "" >> "$shell_config"
        echo "# TESS_REVIEW Environment Variables" >> "$shell_config"
        echo "export TESS_PROVIDER=\"groq\"" >> "$shell_config"
        echo "export GROQ_API_KEY=\"$user_api_key\"" >> "$shell_config"
        echo "✅ Successfully added TESS_PROVIDER and GROQ_API_KEY to $shell_config"
    fi
else
    read -p "Enter your OpenRouter API Key (press Enter to skip): " user_api_key
    if [ -n "$user_api_key" ]; then
        echo "" >> "$shell_config"
        echo "# TESS_REVIEW Environment Variables" >> "$shell_config"
        echo "export TESS_PROVIDER=\"openrouter\"" >> "$shell_config"
        echo "export OPENROUTER_API_KEY=\"$user_api_key\"" >> "$shell_config"
        echo "✅ Successfully added TESS_PROVIDER and OPENROUTER_API_KEY to $shell_config"
    fi
fi

# 5. Prompt for Aliases
echo ""
read -p "Would you like to automatically add 'tess' and 'tess-review' command aliases to your shell config? (y/n, default: y): " add_aliases
add_aliases=${add_aliases:-y}

if [ "$add_aliases" = "y" ] || [ "$add_aliases" = "Y" ]; then
    if [ -z "$shell_config" ]; then
        if [[ "$SHELL" == */zsh ]]; then
            shell_config="$HOME/.zshrc"
        elif [[ "$SHELL" == */bash ]]; then
            shell_config="$HOME/.bashrc"
        elif [ -f "$HOME/.zshrc" ]; then
            shell_config="$HOME/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            shell_config="$HOME/.bashrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            shell_config="$HOME/.bash_profile"
        else
            shell_config="$HOME/.profile"
        fi
    fi

    # Append aliases to shell config
    echo "" >> "$shell_config"
    echo "# TESS_REVIEW Aliases" >> "$shell_config"
    echo "alias tess='${DIR}/.venv/bin/tess'" >> "$shell_config"
    echo "alias tess-review='${DIR}/.venv/bin/tess-review'" >> "$shell_config"
    echo "✅ Successfully added 'tess' and 'tess-review' aliases to $shell_config"
fi

echo ""
echo "==========================================="
if [ -n "$shell_config" ]; then
    echo "To start using TESS, reload your shell configuration:"
    echo "  source $shell_config"
else
    echo "Please set up your API Key manually if you skipped it:"
    echo "  For OpenRouter:"
    echo "    export TESS_PROVIDER='openrouter'"
    echo "    export OPENROUTER_API_KEY='your-key-here'"
    echo "  For Groq:"
    echo "    export TESS_PROVIDER='groq'"
    echo "    export GROQ_API_KEY='your-key-here'"
fi
echo ""
echo "Now you can just type 'tess-review' in your terminal to analyze your code!"
echo "==========================================="
