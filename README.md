# Skill Share

Share one local skill folder with Codex, OpenCode, and Google Antigravity IDE using symlinks. Source edits are visible through every link. Keep the source folder on disk at the same location.

## Usage

Create a folder such as `skill/my-new-tool/` containing `SKILL.md` and optional `scripts/` or `references/` folders. Names must be 1–64 lowercase letters/digits, with single hyphens between words. Start `SKILL.md` with YAML frontmatter:

```markdown
---
name: my-new-tool
description: Explain what this skill does and when to use it.
---

Instructions for the agent. Reference bundled resources relative to this folder.
```

From the repository root, run:

```bash
./mount-skill.sh skill/my-new-tool
```

To mount every skill in the repository at once:

```bash
./mount-skill.sh --all
```

`--all` reads the `skill/` directory beside the script, even when called from
another working directory. It includes immediate, non-hidden subdirectories;
files such as `.gitkeep` are ignored. Each included directory must contain a
readable, nonempty `SKILL.md`. No recursive search is performed. An empty
`skill/` directory prints a message and exits successfully without making links.
Duplicate names after resolving source symlinks are rejected.

Other source directories and quoted paths containing spaces work too. Requires Bash and standard macOS or GNU/Linux utilities; no external `realpath` or Python dependency. Python 3 is needed only for tests.

| Agent | Global destination |
| --- | --- |
| Codex | `~/.agents/skills/<skill-name>` |
| OpenCode | `~/.config/opencode/skills/<skill-name>` |
| Antigravity IDE | `~/.gemini/config/skills/<skill-name>` |

Paths follow the current [Codex](https://learn.chatgpt.com/docs/build-skills), [OpenCode](https://docs.opencode.ai/docs/skills/), and [Antigravity IDE](https://antigravity.google/docs/skills?app=antigravity-ide) documentation. Other Antigravity products or older releases may use different global directories.

## Validation and conflicts

- The script checks the directory name and requires a readable, nonempty `SKILL.md`. It does not parse YAML or validate the full Agent Skills schema. Include `name` and `description`, and match the name to the directory.
- All skills and destinations are checked for validation errors and conflicts before links are created, including the entire batch with `--all`. Existing files, directories, broken links, or links to different sources are preserved and the command fails. Inspect conflicts and move them aside manually.
- Running again for the same source keeps matching links.
- Filesystem errors stop the command with a nonzero status. An error during mounting can leave earlier links in place; correct the error and rerun. Avoid concurrent mounting into the same destinations.

Older versions linked into `~/.agent/skills`, `~/.opencode/skills`, and `~/.codex/skills`. These entries are left untouched. Inspect old links and remove obsolete links manually to avoid duplicate discovery in agents that support legacy paths. Preserve real skill directories during migration.

## Verify discovery

Start a fresh session in each agent and ask it to list available skills. Codex CLI and the IDE extension also provide `/skills`. Restart if changes do not appear.

Successful mounting confirms filesystem links, not agent discovery or execution. Skills that use platform-specific tools, plugins, credentials, or subagent APIs need compatible alternatives in each agent. Mounting does not install dependencies or grant permissions.

This is local sharing on one machine. It does not publish skills, synchronize machines, or download skills from a catalog. No example skills are bundled yet.

## Checks and structure

```bash
bash -n mount-skill.sh
python3 -B -m unittest discover -s tests -v
```

Tests use temporary home directories and never modify installed skills.

- `skill/`: source skill folders (initially empty).
- `mount-skill.sh`: global symlink installer.
- `tests/`: installer regression tests.
- `docs/`: maintenance and verification notes.

## Contributing

Read `AGENTS.md` and [project context](docs/project.md). Keep changes focused, update relevant documentation, and run the checks above before handing off changes.

## License

[MIT](LICENSE).
