"""
xmind_builder.py
Generate real, openable .xmind mind map files from a plain Python dict or JSON —
no XMind installation, plugin, or CLI required. Stdlib only.

XMind's modern file format is just a ZIP archive containing:
  - content.json   -> the actual map data (sheets -> rootTopic -> children)
  - metadata.json  -> creator info
  - manifest.json  -> lists which files are inside the archive

LIBRARY USAGE
-------------
from xmind_builder import build_xmind

tree = {
    "title": "Central Topic",
    "notes": "Optional note text on the root",
    "children": [
        {"title": "Branch 1", "children": [
            {"title": "Leaf 1a"},
            {"title": "Leaf 1b", "notes": "A note on a leaf"},
        ]},
        {"title": "Branch 2", "children": [{"title": "Leaf 2a"}]},
    ],
}

build_xmind(tree, "example.xmind", sheet_title="Sheet 1")

CLI USAGE
---------
Build from a JSON file (single tree, or {"sheets": [{"title": ..., "tree": ...}, ...]}):
    python3 xmind_builder.py build tree.json output.xmind [--sheet-title TITLE]

Read an existing .xmind as an indented outline (titles + notes):
    python3 xmind_builder.py read some_map.xmind
"""

import argparse
import json
import sys
import uuid
import zipfile
from pathlib import Path

_CREATOR = {"name": "xmind-plugin", "version": "0.1.0"}


def _new_id() -> str:
    # XMind ids are short hex-ish strings; any unique string works.
    return uuid.uuid4().hex


def _build_topic(node: dict) -> dict:
    """Recursively convert a {"title": ..., "notes": ..., "children": [...]} node
    into an XMind topic dict."""
    topic = {
        "id": _new_id(),
        "class": "topic",
        "title": node.get("title", ""),
    }

    if node.get("notes"):
        topic["notes"] = {"plain": {"content": node["notes"]}}

    if node.get("labels"):
        topic["labelIds"] = node["labels"] if isinstance(node["labels"], list) else [node["labels"]]

    children = node.get("children") or []
    if children:
        topic["children"] = {
            "attached": [_build_topic(child) for child in children]
        }

    return topic


def _build_sheet(tree: dict, sheet_title: str) -> dict:
    return {
        "id": _new_id(),
        "class": "sheet",
        "title": sheet_title,
        "rootTopic": _build_topic(tree),
        "topicOverlapping": "overlap",
    }


def _write_archive(content_json: list, output_path: str) -> str:
    output_path = str(output_path)
    if not output_path.endswith(".xmind"):
        output_path += ".xmind"

    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
            "manifest.json": {},
        }
    }
    metadata = {"creator": _CREATOR}

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.json", json.dumps(content_json, ensure_ascii=False))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False))
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False))

    return output_path


def build_xmind(tree: dict, output_path: str, sheet_title: str = "Sheet 1") -> str:
    """
    Build a .xmind file from a nested dict and write it to output_path.

    tree: {"title": str, "notes": str (optional), "children": [tree, ...] (optional)}
    Returns the output_path for convenience.
    """
    return _write_archive([_build_sheet(tree, sheet_title)], output_path)


def build_xmind_multi(sheets: list, output_path: str) -> str:
    """
    Build a .xmind file with multiple sheets.
    sheets: [{"title": "Sheet name", "tree": {...}}, ...]
    """
    content_json = [_build_sheet(s["tree"], s.get("title", "Sheet")) for s in sheets]
    return _write_archive(content_json, output_path)


def read_xmind(path: str) -> list:
    """Return the parsed content.json (list of sheets) from a .xmind file."""
    with zipfile.ZipFile(path) as zf:
        return json.loads(zf.read("content.json"))


def _print_outline(topic: dict, depth: int = 0) -> None:
    indent = "  " * depth
    print(f"{indent}- {topic.get('title', '')}")
    note = topic.get("notes", {}).get("plain", {}).get("content")
    if note:
        for line in note.splitlines():
            print(f"{indent}    note: {line}")
    for child in topic.get("children", {}).get("attached", []):
        _print_outline(child, depth + 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or read .xmind mind map files")
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Build a .xmind from a JSON tree file")
    p_build.add_argument("tree_json", help="JSON file: a tree dict, or {\"sheets\": [...]} for multi-sheet")
    p_build.add_argument("output", help="Output .xmind path")
    p_build.add_argument("--sheet-title", default="Sheet 1", help="Sheet title (single-tree input only)")

    p_read = sub.add_parser("read", help="Print a .xmind file as an indented outline")
    p_read.add_argument("xmind_file", help="Path to an existing .xmind file")

    args = parser.parse_args()

    if args.command == "build":
        data = json.loads(Path(args.tree_json).read_text())
        if isinstance(data, dict) and "sheets" in data:
            path = build_xmind_multi(data["sheets"], args.output)
        else:
            path = build_xmind(data, args.output, sheet_title=args.sheet_title)
        print(f"Wrote {path}")
    elif args.command == "read":
        for sheet in read_xmind(args.xmind_file):
            print(f"# Sheet: {sheet.get('title', '')}")
            _print_outline(sheet.get("rootTopic", {}))
            print()


if __name__ == "__main__":
    main()
