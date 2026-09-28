# xmind-plugin

Lets Claude create and read **XMind mind maps** (`.xmind` files). The XMind format is just a zip of three JSON files, so the bundled builder is standard-library-only Python — no XMind installation, extra packages, or venv required.

The core is an **Agent Skill** (`skills/xmind/`), which works on **both** Claude surfaces:

- **Claude Code** — installed as a plugin (this repo doubles as a marketplace).
- **Claude Desktop / claude.ai / mobile** — uploaded as a Skill (one zip).

Same skill folder, two delivery mechanisms.

## What's inside

- `skills/xmind/SKILL.md` — the skill: triggers on "mind map / mindmap / .xmind" requests; builds maps from any content and reads existing ones. Written surface-neutrally so it behaves correctly whether it runs on your local machine or in a sandboxed container.
- `skills/xmind/scripts/xmind_builder.py` — build + read CLI and importable library (stdlib only).
- `build-skill-zip.sh` — produces `dist/xmind-skill.zip` for uploading to the Claude apps. The zip is not committed; it is attached to each [GitHub release](https://github.com/darpal/xmind-plugin/releases).

## Install in Claude Code

This repo is its own marketplace (`patrik-plugins`).

```bash
claude plugin marketplace add darpal/xmind-plugin   # from GitHub (public)
# or, on the machine where the repo is checked out locally:
claude plugin marketplace add ~/local-coding/xmind-plugin

claude plugin install xmind@patrik-plugins --scope user
```

Then just ask Claude for a mind map in any session.

## Install in Claude Desktop / claude.ai / mobile

Skills are shared across the Claude apps by your account, so you upload once and it's available on desktop, web, and mobile.

1. Download `xmind-skill.zip` from the [latest release](https://github.com/darpal/xmind-plugin/releases/latest), or build it yourself:

   ```bash
   ./build-skill-zip.sh        # writes dist/xmind-skill.zip
   ```

2. In any Claude app: **Settings → Capabilities → Skills** (requires a plan with Skills / code execution enabled), then upload `xmind-skill.zip`.

3. Ask for a mind map. Claude builds the `.xmind` in its sandbox and gives you a downloadable file.

## CLI usage (standalone)

```bash
# Build: JSON tree -> .xmind
python3 skills/xmind/scripts/xmind_builder.py build tree.json output.xmind --sheet-title "My Map"

# Read: .xmind -> indented outline
python3 skills/xmind/scripts/xmind_builder.py read output.xmind
```

Tree format: nested `{"title": ..., "notes": ..., "children": [...]}`; wrap in `{"sheets": [{"title": ..., "tree": ...}]}` for multi-sheet files. See `skills/xmind/SKILL.md` for details.
