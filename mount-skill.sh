#!/bin/bash

# Script to mount a skill folder for various AI agents (OpenCode, Codex, Google Antigravity)
# Usage: ./mount-skill.sh <path-to-skill-folder>

if [ -z "$1" ]; then
    echo "Usage: $0 <path-to-skill-folder>"
    exit 1
fi

SKILL_PATH=$(realpath "$1")
SKILL_NAME=$(basename "$SKILL_PATH")

if [ ! -d "$SKILL_PATH" ]; then
    echo "Error: $SKILL_PATH is not a directory."
    exit 1
fi

# Define target directories for different agents in the home directory
# - Google Antigravity: looks in ~/.agent/skills
# - OpenCode: common convention in ~/.opencode/skills
# - Codex: common convention in ~/.codex/skills
TARGETS=(
    "$HOME/.agent/skills"    
    "$HOME/.opencode/skills" 
    "$HOME/.codex/skills"    
)

echo "Mounting skill '$SKILL_NAME' from $SKILL_PATH..."

for TARGET in "${TARGETS[@]}"; do
    mkdir -p "$TARGET"
    TARGET_PATH="$TARGET/$SKILL_NAME"
    
    if [ -L "$TARGET_PATH" ] || [ -e "$TARGET_PATH" ]; then
        echo "Updating existing mount in $TARGET_PATH"
        rm -rf "$TARGET_PATH"
    fi
    
    ln -s "$SKILL_PATH" "$TARGET_PATH"
    echo "✅ Mounted to $TARGET_PATH"
done

echo "Done! Skill '$SKILL_NAME' is now available to OpenCode, Codex, and Google Antigravity."
