---
name: xmind
description: Create and read XMind mind maps (.xmind files). Use whenever the user wants a mind map or mindmap of anything — project structure, brainstorm, plan, notes, roadmap — or mentions a .xmind file, XMind, or mapping ideas out visually. Covers building new maps from any content and reading/summarizing existing .xmind files. No dependencies; runs on any Python 3.
---

# XMind Mind Maps

Build real, openable `.xmind` files from structured content, and read existing ones back. The XMind format is just a zip of three JSON files — `scripts/xmind_builder.py` (Python standard library only, no packages or venv needed) handles both directions. It runs anywhere Python 3 runs: Claude Code on your machine, or the sandboxed code-execution container behind Claude Desktop / claude.ai / mobile.

> Paths below are written as `scripts/xmind_builder.py` — relative to **this skill's own directory**. Run the script from the skill directory, or prefix it with the skill's absolute path.

## Building a mind map

1. Turn the source content into a nested tree and save it as JSON in a temp/working file:

```json
{
  "title": "Central Topic",
  "notes": "Optional note text (shows in XMind's notes panel)",
  "children": [
    {
      "title": "Branch 1",
      "children": [
        {"title": "Leaf 1a"},
        {"title": "Leaf 1b", "notes": "Detail lives in notes, not titles"}
      ]
    },
    {"title": "Branch 2", "children": [{"title": "Leaf 2a"}]}
  ]
}
```

Every node: `title` (required), `notes` (optional), `children` (optional list of the same shape).

2. Build it:

```bash
python3 scripts/xmind_builder.py build tree.json output.xmind --sheet-title "My Map"
```

Multiple sheets in one file — wrap trees in a `sheets` list:

```json
{"sheets": [
  {"title": "Sheet A", "tree": { ... tree ... }},
  {"title": "Sheet B", "tree": { ... tree ... }}
]}
```

Or import directly from Python (`build_xmind(tree, path, sheet_title=...)` / `build_xmind_multi(sheets, path)`) when generating the tree programmatically.

## Reading an existing .xmind

```bash
python3 scripts/xmind_builder.py read some_map.xmind
```

Prints each sheet as an indented outline with notes — use this to summarize, extend, or convert an existing map. For the raw structure: `unzip -p some_map.xmind content.json | python3 -m json.tool`.

To extend a map: `read` it (or parse `content.json`), rebuild the tree with additions, and `build` a new file — don't edit the zip in place.

## Authoring tips

- Keep it scannable: aim for 3–7 branches per node; go deeper rather than wider.
- Short titles (a few words); push sentences and detail into `notes`.
- Mirror the user's structure (headings, phases, categories) rather than inventing one.

## Delivering the result

Write the `.xmind` to the working directory, then hand it to the user in whatever way fits the surface:

- **Claude Code (local machine):** default to the current project folder, or `~/Downloads` if not in a project. Report the path and offer `open <file>.xmind` to view it in XMind (macOS).
- **Claude Desktop / claude.ai / mobile (sandboxed):** the file lives in the container — present it as a **downloadable file** so the user can save it and open it in XMind.

Either way, end by giving the user the file and a one-line summary of the map's top-level branches.

## Verify

After building, sanity-check the archive by reading it back:

```bash
python3 scripts/xmind_builder.py read output.xmind
```

If the outline prints the expected structure, the file will open in XMind.
