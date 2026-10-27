# Project Context

## Purpose
Skill-share is a centralized repository designed for managing and sharing AI Agent Skills across multiple platforms. Its primary goal is to provide a unified way to distribute "skills" (instructions, scripts, and resources) to different AI coding assistants like Google Antigravity, OpenCode, and Codex.

## Tech Stack
- **Shell (Bash/Zsh)**: Used for utility scripts (e.g., `mount-skill.sh`) to manage local installation and mounting.
- **Markdown**: Used for skill definitions (`SKILL.md`) and project documentation.

## Project Conventions

### Code Style
- **Shell Scripts**: Should include proper error handling and path resolution. Use double quotes for variables to handle paths with spaces. Target Bash 4+ or POSIX compliance where possible.
- **Markdown**: Follow GitHub Flavored Markdown (GFM) standards. Maintain a clean hierarchy and use descriptive headers.

### Architecture Patterns
- **Symlink Management**: The project uses a "mount" pattern where skills stored in the repository are symlinked to `~/.agents/skills` (Codex), `~/.config/opencode/skills` (OpenCode), and `~/.gemini/config/skills` (Antigravity IDE). Existing entries are preserved; matching symlinks are reused.
- **Skill Structure**: Each skill resides in its own folder and MUST contain a `SKILL.md` file defining its capabilities and usage.
- **Batch mounting**: `./mount-skill.sh --all` mounts immediate non-hidden folders in the script's adjacent `skill/` directory. The complete batch is validated and checked for conflicts before links are created. Empty directories produce a successful no-op.

### Testing Strategy
- **Verification**: Ensure that mounting scripts correctly create symlinks and that targets are accessible.
- **Regression checks**: Run `bash -n mount-skill.sh` and `python3 -B -m unittest discover -s tests -v` using temporary home directories.

### Git Workflow
- **Linear History**: Prefer rebasing or squash-merging to maintain a clean git history.

## Domain Context
- **AI Agent Skills**: A "skill" is a set of instructions and tools that extend an agent's capabilities. Different agents search for these skills in specific directories.

## Important Constraints
- **Path Resolution**: Scripts must handle absolute paths correctly (using `cd` and `pwd -P`) to ensure symlinks don't break when executed from different directories.
- **Home Directory Portability**: Targets are typically relative to the user's home directory (`$HOME`).

## External Dependencies
- **Shell utilities**: Bash and standard macOS or GNU/Linux utilities including `ln`, `mkdir`, `readlink`, and `pwd`. Python 3 is needed only for tests.
