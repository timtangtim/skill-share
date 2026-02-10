# Skill Share

A centralized repository for managing and sharing AI Agent Skills across platforms like Google Antigravity, OpenCode, and Codex.

## 🚀 Purpose

Skill-share provides a unified way to distribute and install AI "skills"—collections of instructions, scripts, and resources—into different AI coding assistants. It uses a "mount" pattern to symlink skills from this repository directly into the global configuration directories of your favorite AI tools.

## ⚙️ Features

- **Multi-Agent Support**: Compatible with Google Antigravity, OpenCode, and Codex.
- **Global Deployment**: Mounts skills to your home directory (`~`) for system-wide accessibility.
- **Spec-Driven**: Uses [OpenSpec](https://openspec.ai) for rigorous requirement and behavior tracking.
- **Simple Automation**: One script to rule them all (`mount-skill.sh`).

## 🛠 Usage

### Mounting a Skill

To make a skill available to your AI agents, run the `mount-skill.sh` script provided in the root:

```bash
chmod +x mount-skill.sh
./mount-skill.sh <path-to-skill-folder>
```

**Example:**
```bash
./mount-skill.sh skills/my-new-tool
```

The script will create symlinks in:
- `~/.agent/skills/` (Antigravity)
- `~/.opencode/skills/` (OpenCode)
- `~/.codex/skills/` (Codex)

## 📂 Project Structure

- `skill/`: Default directory for storing your custom skill folders.
- `mount-skill.sh`: Automation script for symlinking skills.
- `openspec/`: Contains project specifications and change proposals.
- `AGENTS.md`: Specific instructions for AI agents working on this project.

## 🤝 Contributing

This project follows **OpenSpec** conventions. For any new features, architecture changes, or breaking updates:
1. Create a proposal in `openspec/changes/<id>`.
2. Define requirements and scenarios.
3. Once approved, implement the changes according to the specification.

Refer to `openspec/AGENTS.md` for detailed developer instructions.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
