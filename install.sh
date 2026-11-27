#!/usr/bin/env bash
set -e

echo "🪄 Installing Grumo Framework..."

INSTALL_DIR="$HOME/.grumo"
BIN_DIR="$HOME/.local/bin"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

echo "📦 Setting up isolated environment in $INSTALL_DIR/venv..."
if command -v uv &> /dev/null; then
    echo "⚡ Using uv for blazing fast installation..."
    rm -rf "$INSTALL_DIR/venv"
    uv venv "$INSTALL_DIR/venv"
    uv pip install --python "$INSTALL_DIR/venv" --refresh --upgrade grumo
else
    if command -v python3 &> /dev/null; then
        rm -rf "$INSTALL_DIR/venv"
        python3 -m venv "$INSTALL_DIR/venv"
    elif command -v python &> /dev/null; then
        rm -rf "$INSTALL_DIR/venv"
        python -m venv "$INSTALL_DIR/venv"
    else
        echo "❌ Error: Python 3 is required but not found."
        exit 1
    fi
    "$INSTALL_DIR/venv/bin/pip" install --upgrade pip
    "$INSTALL_DIR/venv/bin/pip" install --upgrade grumo
fi

echo "🔗 Linking executable to $BIN_DIR/grumo..."
ln -sf "$INSTALL_DIR/venv/bin/grumo" "$BIN_DIR/grumo"

echo "✨ Grumo is installed!"
echo ""
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️  Please add $BIN_DIR to your PATH."
    echo "   Add this line to your ~/.zshrc or ~/.bashrc:"
    echo "   export PATH=\"$BIN_DIR:\$PATH\""
else
    echo "🚀 You can now run 'grumo new my_app' from anywhere."
fi