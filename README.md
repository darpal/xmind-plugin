# xmind-plugin

A Claude Code plugin that lets Claude create and read **XMind mind maps** (`.xmind` files) in any project. The XMind format is just a zip of three JSON files, so the bundled builder is stdlib-only Python — no XMind installation, extra packages, or venv required.

## What's inside

- `skills/xmind/SKILL.md` — the skill: triggers on "mind map / mindmap / .xmind" requests, covers building maps from any content and reading existing ones.
- `skills/xmind/scripts/xmind_builder.py` — build + read CLI and importable library.

## Install

The repo is its own marketplace (`patrik-plugins`).

On any Mac:

```bash
claude plugin marketplace add darpal/xmind-plugin   # from GitHub (private repo — needs gh/git auth on that Mac)
# or, on the machine where the repo is checked out locally:
claude plugin marketplace add ~/local-coding/xmind-plugin

claude plugin install xmind@patrik-plugins --scope user
```

Then just ask Claude for a mind map in any session.

## CLI usage (standalone)

```bash
# Build: JSON tree -> .xmind
python3 skills/xmind/scripts/xmind_builder.py build tree.json output.xmind --sheet-title "My Map"

# Read: .xmind -> indented outline
python3 skills/xmind/scripts/xmind_builder.py read output.xmind
```

Tree format: nested `{"title": ..., "notes": ..., "children": [...]}`; wrap in `{"sheets": [{"title": ..., "tree": ...}]}` for multi-sheet files. See `skills/xmind/SKILL.md` for details.
