#!/usr/bin/env python3
"""Keep index.json and skills/*/SKILL.md in step.

    python3 scripts/check.py                    # structure only
    python3 scripts/check.py --tools tools.json --workflows workflows.json

The optional files are the JSON of GET /v1/tools and GET /v1/workflows (or the MCP list_tools and
list_workflows results). With them, every tool and workflow a skill names must exist and be
available. Exit 1 on any problem. Standard library only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUSES = {"shipped", "planned"}
GROUPS = {"creators", "studios"}
SHIPPED_FIELDS = ("category", "title", "line", "summary", "steps", "note", "tools", "workflows")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(text):
    """The `key: value` lines between the leading --- fences."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            out[key.strip()] = value.strip()
    return out


def catalogue(path):
    """Ids of the available entries of a list_tools / list_workflows JSON file, or None."""
    if not path:
        return None
    rows = json.loads(Path(path).read_text())["data"]
    return {r["id"] for r in rows if r.get("available", True)}


def check(tools_path=None, workflows_path=None):
    problems = []
    index = json.loads((ROOT / "index.json").read_text())
    entries = index.get("skills", [])
    tools, workflows = catalogue(tools_path), catalogue(workflows_path)

    seen = set()
    for e in entries:
        sid = e.get("id", "?")
        if sid in seen:
            problems.append(f"{sid}: listed twice")
        seen.add(sid)
        if not NAME_RE.match(sid):
            problems.append(f"{sid}: id must be lower-case words joined by hyphens")
        if e.get("status") not in STATUSES:
            problems.append(f"{sid}: status must be one of {sorted(STATUSES)}")
        if e.get("group") not in GROUPS:
            problems.append(f"{sid}: group must be one of {sorted(GROUPS)}")
        if e.get("status") != "shipped":
            continue
        missing = [f for f in SHIPPED_FIELDS if f not in e]
        if missing:
            problems.append(f"{sid}: shipped entry lacks {', '.join(missing)}")
        skill = ROOT / "skills" / sid / "SKILL.md"
        if not skill.is_file():
            problems.append(f"{sid}: shipped but skills/{sid}/SKILL.md does not exist")
            continue
        text = skill.read_text()
        for name in e.get("tools", []) + e.get("workflows", []):
            if name not in text:
                problems.append(f"{sid}: index names {name!r} but SKILL.md never mentions it")
        for name in e.get("tools", []):
            if tools is not None and name not in tools:
                problems.append(f"{sid}: tool {name!r} is not an available Wazza tool")
        for name in e.get("workflows", []):
            if workflows is not None and name not in workflows:
                problems.append(f"{sid}: workflow {name!r} is not an available Wazza workflow")

    shipped = {e["id"] for e in entries if e.get("status") == "shipped"}
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        folder = skill.parent.name
        meta = frontmatter(skill.read_text())
        if meta is None:
            problems.append(f"skills/{folder}: SKILL.md has no frontmatter")
            continue
        if meta.get("name") != folder:
            problems.append(f"skills/{folder}: frontmatter name is {meta.get('name')!r}")
        description = meta.get("description", "")
        if not description:
            problems.append(f"skills/{folder}: frontmatter has no description")
        elif len(description) > 1024:
            problems.append(f"skills/{folder}: description is over 1024 characters")
        if folder not in shipped:
            problems.append(f"skills/{folder}: folder exists but index.json does not list it as shipped")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tools", help="JSON of GET /v1/tools")
    parser.add_argument("--workflows", help="JSON of GET /v1/workflows")
    args = parser.parse_args()
    problems = check(args.tools, args.workflows)
    for p in problems:
        print(p)
    print("ok" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
