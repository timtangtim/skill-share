# Project Context

## Purpose
Skill-share is a centralized repository designed for managing and sharing AI Agent Skills across multiple platforms. Its primary goal is to provide a unified way to distribute "skills" (instructions, scripts, and resources) to different AI coding assistants like Google Antigravity, OpenCode, and Codex.

## Tech Stack
- **Shell (Bash/Zsh)**: Used for utility scripts (e.g., `mount-skill.sh`) to manage local installation and mounting.
- **Markdown**: Used for skill definitions (`SKILL.md`) and project documentation.
- **OpenSpec**: Used for specification-driven development and formalizing change proposals.

## Project Conventions

### Code Style
- **Shell Scripts**: Should include proper error handling and path resolution. Use double quotes for variables to handle paths with spaces. Target Bash 4+ or POSIX compliance where possible.
- **Markdown**: Follow GitHub Flavored Markdown (GFM) standards. Maintain a clean hierarchy and use descriptive headers.

### Architecture Patterns
- **Symlink Management**: The project uses a "mount" pattern where skills stored in the repository are symlinked to agent-specific global configuration directories (e.g., `~/.agent/skills`).
- **Skill Structure**: Each skill resides in its own folder and MUST contain a `SKILL.md` file defining its capabilities and usage.

### Testing Strategy
- **Verification**: Ensure that mounting scripts correctly create symlinks and that targets are accessible.
- **Spec Validation**: Use `openspec validate` to ensure all specifications and change proposals meet the project's requirements.

### Git Workflow
- **OpenSpec Proposals**: All significant changes or new capabilities follow the OpenSpec workflow (Stage 1: Proposal -> Stage 2: Implementation -> Stage 3: Archive).
- **Linear History**: Prefer rebasing or squash-merging to maintain a clean git history.

## Domain Context
- **AI Agent Skills**: A "skill" is a set of instructions and tools that extend an agent's capabilities. Different agents search for these skills in specific directories.
- **OpenSpec**: A framework for writing requirements and scenarios that drive development, ensuring AI agents understand the intended behavior of the system.

## Important Constraints
- **Path Resolution**: Scripts must handle absolute paths correctly (using `realpath`) to ensure symlinks don't break when executed from different directories.
- **Home Directory Portability**: Targets are typically relative to the user's home directory (`$HOME`).

## External Dependencies
- **OpenSpec CLI**: Required for managing project specifications and proposals.
- **Coreutils**: Relies on standard Unix utilities like `ln`, `mkdir`, and `realpath`.
