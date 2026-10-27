# Agent instructions

Read `README.md`, `docs/project.md`, and nearby code before making changes.

- Keep changes focused on local skill sharing for Codex, OpenCode, and Antigravity IDE.
- Preserve existing user files and symlinks. Never replace conflicting destinations automatically.
- Use quoted paths and maintain compatibility with Bash on macOS and GNU/Linux.
- Keep single-skill and `--all` mounting behaviour documented in the README.
- Update relevant documentation and add regression coverage when behaviour changes.
- Run `bash -n mount-skill.sh`, `python3 -B -m unittest discover -s tests -v`, and `git diff --check`.
- Tests must use temporary home directories and must not modify installed skills.
- State what changed, checks run, and any unverified behaviour in the handoff.
