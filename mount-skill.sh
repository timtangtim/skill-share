#!/bin/bash

# Share local skills with OpenCode, Codex, and Google Antigravity IDE.
# Usage: ./mount-skill.sh <path-to-skill-folder> | --all

set -euo pipefail

fail() {
    echo "Error: $*" >&2
    exit 1
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-skill-folder> | --all" >&2
    exit 1
fi

[ -n "${HOME:-}" ] && [[ "$HOME" = /* ]] || fail 'HOME must be an absolute directory path.'
SKILLS=()
if [ "$1" = --all ]; then
    SCRIPT_DIR=$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
    [ -d "$SCRIPT_DIR/skill" ] || fail "Missing skill directory: $SCRIPT_DIR/skill"
    shopt -s nullglob
    for CANDIDATE in "$SCRIPT_DIR"/skill/*; do
        [ -d "$CANDIDATE" ] || continue
        SKILLS+=("$CANDIDATE")
    done
    if [ "${#SKILLS[@]}" -eq 0 ]; then
        echo "No skill folders found in $SCRIPT_DIR/skill. Nothing to mount."
        exit 0
    fi
else
    SKILLS=("$1")
fi

# Validate the entire batch before changing any destinations.
for INDEX in "${!SKILLS[@]}"; do
    [ -d "${SKILLS[$INDEX]}" ] || fail "${SKILLS[$INDEX]} is not a directory."
    SKILL_PATH=$(cd -- "${SKILLS[$INDEX]}" && pwd -P)
    SKILL_NAME=$(basename "$SKILL_PATH")
    if [ "${#SKILL_NAME}" -gt 64 ] || ! [[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        fail 'Skill directory names must be 1–64 lowercase letters/digits with single hyphen separators.'
    fi
    [ -f "$SKILL_PATH/SKILL.md" ] && [ -r "$SKILL_PATH/SKILL.md" ] && [ -s "$SKILL_PATH/SKILL.md" ] ||
        fail "The skill $SKILL_PATH must contain a readable, nonempty SKILL.md file."
    # Source aliases can resolve to a different basename. Reject duplicate names
    # so a batch cannot install two different sources into the same destination.
    for PREVIOUS in "${SKILLS[@]:0:$INDEX}"; do
        [ "$(basename "$PREVIOUS")" != "$SKILL_NAME" ] || fail "Duplicate skill name: $SKILL_NAME"
    done
    SKILLS[$INDEX]="$SKILL_PATH"
done

TARGETS=(
    "$HOME/.agents/skills"
    "$HOME/.config/opencode/skills"
    "$HOME/.gemini/config/skills"
)

# Check every destination before creating any links. Never remove user data,
# including broken links or links to a different source.
for SKILL_PATH in "${SKILLS[@]}"; do
    SKILL_NAME=$(basename "$SKILL_PATH")
    for TARGET in "${TARGETS[@]}"; do
        TARGET_PATH="$TARGET/$SKILL_NAME"
        if [ -L "$TARGET_PATH" ] && [ "$(readlink "$TARGET_PATH")" = "$SKILL_PATH" ]; then
            continue
        fi
        if [ -L "$TARGET_PATH" ] || [ -e "$TARGET_PATH" ]; then
            fail "$TARGET_PATH already exists. Move it aside manually before mounting."
        fi
        PARENT="$TARGET"
        while [ ! -e "$PARENT" ] && [ ! -L "$PARENT" ]; do
            PARENT=$(dirname "$PARENT")
        done
        [ -d "$PARENT" ] || fail "$PARENT is not a usable destination directory."
    done
done

# Prepare directories before linking; mkdir/ln failures stop the script and
# never print a successful completion message.
for TARGET in "${TARGETS[@]}"; do
    mkdir -p "$TARGET"
done

for SKILL_PATH in "${SKILLS[@]}"; do
    SKILL_NAME=$(basename "$SKILL_PATH")
    echo "Mounting skill '$SKILL_NAME' from $SKILL_PATH..."
    for TARGET in "${TARGETS[@]}"; do
        TARGET_PATH="$TARGET/$SKILL_NAME"
        if [ -L "$TARGET_PATH" ] && [ "$(readlink "$TARGET_PATH")" = "$SKILL_PATH" ]; then
            echo "Already mounted: $TARGET_PATH"
            continue
        fi
        # -h prevents following a destination symlink on macOS; on Linux use -T.
        if [ "$(uname -s)" = Darwin ]; then
            ln -sh "$SKILL_PATH" "$TARGET_PATH"
        else
            ln -sT "$SKILL_PATH" "$TARGET_PATH"
        fi
        echo "Mounted: $TARGET_PATH"
    done
done

echo 'Done! Links created for Codex, OpenCode, and Antigravity IDE.'
echo 'Check skill discovery in each agent; restart the agent if needed.'
