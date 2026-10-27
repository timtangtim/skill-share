# Skill mounting compatibility fix

Updated on 2026-10-27 to restore the advertised local sharing behaviour.

The installer now links into Codex's `.agents/skills`, OpenCode's
`.config/opencode/skills`, and Antigravity IDE's `.gemini/config/skills`
under the user's home directory. Current documentation links and a minimal
skill manifest are in the README.

The installer validates arguments, portable directory names, and the presence
of a readable, nonempty `SKILL.md`. It preserves existing destination entries,
checks all destinations before linking, and reuses links to the same absolute
source. Filesystem failures return a nonzero exit status. Source paths are
resolved with shell builtins rather than external `realpath`.

## Verification

- `bash -n mount-skill.sh`: passed.
- `python3 -B -m unittest discover -s tests -v`: all eight tests passed on macOS.
  Coverage includes all three destinations, paths with spaces, relative paths,
  repeat mounting, source updates through links, missing/empty manifests,
  invalid names/arguments/home paths, preserved conflicts, blocked parents,
  and failure reporting when link creation fails.
- `git diff --check`: passed.
- Manual diff review: checked destination paths, preservation of existing data,
  documented limitations, and removal of destructive replacement behaviour.

## Limits and next steps

Actual discovery and execution inside the three agents remain unverified.
Use a real portable skill, run the mount command, then check a fresh session
in each agent as described in the README. No real global skills were changed
during testing. GNU/Linux execution remains unverified.

Manifest YAML/schema validation and platform-specific dependencies remain the
responsibility of the skill author and host agent. Legacy mounts are preserved
for manual inspection. Link creation is not transactional; an I/O error can
leave earlier links installed. Concurrent installation is not supported.
