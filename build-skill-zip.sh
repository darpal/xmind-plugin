#!/usr/bin/env bash
# Package the xmind Agent Skill into a zip for uploading to the Claude apps
# (Claude Desktop / claude.ai / mobile: Settings -> Capabilities -> Skills).
# The Claude Code plugin does NOT use this zip — it reads skills/xmind/ directly.
set -euo pipefail

cd "$(dirname "$0")"

OUT="dist/xmind-skill.zip"
mkdir -p dist
rm -f "$OUT"

# Zip the skill folder itself so the archive contains xmind/SKILL.md at its root,
# which is what the Skills uploader expects. Exclude caches.
( cd skills && zip -r "../$OUT" xmind -x '*/__pycache__/*' '*.pyc' >/dev/null )

echo "Wrote $OUT"
unzip -l "$OUT"
