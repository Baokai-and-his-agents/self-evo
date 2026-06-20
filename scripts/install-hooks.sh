#!/bin/bash
# Self-evo Claude Code Hooks Installer
# This script automatically installs safety hooks into .claude/settings.json

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$REPO_ROOT/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
SAMPLE_FILE="$REPO_ROOT/scripts/hooks/claude-settings.sample.json"

echo "🔧 Self-evo Hooks Installer"
echo "================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is required but not found in PATH"
    echo "   Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python 3 detected: $PYTHON_VERSION"
echo ""

# Create .claude directory if it doesn't exist
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "📁 Creating .claude directory..."
    mkdir -p "$CLAUDE_DIR"
fi

# Check if settings.json already exists
if [ -f "$SETTINGS_FILE" ]; then
    echo "⚠️  Warning: .claude/settings.json already exists"
    echo ""
    echo "Current content:"
    cat "$SETTINGS_FILE"
    echo ""
    read -p "Do you want to OVERWRITE it? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "❌ Installation cancelled"
        exit 1
    fi
    echo ""
    echo "📝 Backing up existing settings.json to settings.json.backup..."
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
fi

# Extract hooks block from sample file using Python
echo "📦 Installing hooks configuration..."
python3 << 'PYTHON_SCRIPT'
import json
import os

repo_root = os.environ['REPO_ROOT']
sample_file = os.path.join(repo_root, 'scripts/hooks/claude-settings.sample.json')
settings_file = os.path.join(repo_root, '.claude/settings.json')

with open(sample_file, 'r', encoding='utf-8') as f:
    sample = json.load(f)

# Extract the hooks block
hooks = sample.get('hooks', {})

# Create settings.json with hooks
settings = {'hooks': hooks}

with open(settings_file, 'w', encoding='utf-8') as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
    f.write('\n')

print(f"✅ Created {settings_file}")
PYTHON_SCRIPT

# Verify installation
echo ""
echo "🔍 Verifying installation..."
echo ""
echo "Content of .claude/settings.json:"
cat "$SETTINGS_FILE"
echo ""

# Check current rollout mode
ROLLOUT_MODE=$(python3 -c "import json; print(json.load(open('$REPO_ROOT/scripts/hooks/config.json'))['rollout_mode'])")
echo "📊 Current rollout mode: $ROLLOUT_MODE"
echo ""

echo "✅ Hooks installation complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Restart Claude Code to activate hooks"
echo "   2. Current mode is '$ROLLOUT_MODE' (records but does not block)"
echo "   3. To change mode, edit scripts/hooks/config.json or set SELF_EVO_ROLLOUT_MODE env var"
echo "   4. Read scripts/README.md for full documentation"
echo ""
echo "🎯 Test the installation:"
echo "   python3 scripts/hooks/pretooluse.py"
echo "   (Press Ctrl+D to send empty input, should exit 0 with no output)"
