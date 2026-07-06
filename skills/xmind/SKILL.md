---
name: xmind
description: Create and read XMind mind maps (.xmind files). Use whenever the user wants a mind map or mindmap of anything — project structure, brainstorm, plan, notes, roadmap — or mentions a .xmind file, XMind, or mapping ideas out visually. Covers building new maps from any content and reading/summarizing existing .xmind files. No dependencies; works with system python3.
---

# XMind Mind Maps

Build real, openable `.xmind` files from structured content, and read existing ones back. The XMind format is just a zip of three JSON files — `scripts/xmind_builder.py` (stdlib only, no venv needed) handles both directions.

## Building a mind map

1. Turn the source content into a nested tree and save it as JSON in a temp/scratchpad file:

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
python3 <skill_dir>/scripts/xmind_builder.py build tree.json output.xmind --sheet-title "My Map"
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
python3 <skill_dir>/scripts/xmind_builder.py read some_map.xmind
```

Prints each sheet as an indented outline with notes — use this to summarize, extend, or convert an existing map. For the raw structure: `unzip -p some_map.xmind content.json | python3 -m json.tool`.

To extend a map: `read` it (or parse `content.json`), rebuild the tree with additions, and `build` a new file — don't edit the zip in place.

## Authoring tips

- Keep it scannable: aim for 3–7 branches per node; go deeper rather than wider.
- Short titles (a few words); push sentences and detail into `notes`.
- Mirror the user's structure (headings, phases, categories) rather than inventing one.
- Output location: the current project folder if working in one, otherwise `~/Downloads`. Always end with the file path, and offer `open <file>.xmind` to view it in XMind on macOS.

## Verify

After building, sanity-check the archive:

```bash
python3 <skill_dir>/scripts/xmind_builder.py read output.xmind
```

If the outline prints correctly, the file will open in XMind.
