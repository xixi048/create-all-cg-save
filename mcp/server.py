#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""create-all-cg-save — MCP server (stdio, zero dependencies).

Wraps the save toolkit in the Model Context Protocol so any MCP-capable agent
can drive it without knowing this repo's layout.

    python mcp/server.py          # JSON-RPC 2.0 on stdin/stdout

Tools (all local, no network):
  save_scout            find candidate save files for a game / directory
  engine_inspect        parse a known save format and list switch/variable state
  plan_unlock_switches  build an unlock plan for RPG Maker RGSS saves
  diff_saves            byte-diff a "before" and an "after" save
  infer_unlock_plan     fit the flag array from diffs and extrapolate
  apply_plan            dry-run / apply / verify / rollback a plan

Every write is preceded by an automatic timestamped backup and is reversible.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILL = os.path.join(ROOT, "skills", "create-all-cg-save")
SCRIPTS = os.path.join(SKILL, "scripts")

PROTOCOL_VERSION = "2025-06-18"

TOOLS = [
    {
        "name": "save_scout",
        "description": "Scan the usual save locations on this machine and list candidate save files, with engine fingerprinting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "game": {"type": "string", "description": "Game name keyword."},
                "dir": {"type": "string", "description": "Install directory to scan instead."},
                "changed_within": {"type": "number", "description": "Only files changed within N hours (great after quitting the game)."},
                "json_out": {"type": "string", "description": "Optional path to write the JSON result."},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "engine_inspect",
        "description": "Parse a save with a known engine adapter (RPG Maker RGSS) and report structure plus current switch/variable state.",
        "inputSchema": {
            "type": "object",
            "properties": {"save": {"type": "string", "description": "Absolute path to the save file."}},
            "required": ["save"],
            "additionalProperties": False,
        },
    },
    {
        "name": "plan_unlock_switches",
        "description": "Build an equal-length patch plan that turns the given RPG Maker switches ON. Does not write anything; returns the plan path.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "save": {"type": "string"},
                "ids": {"type": "string", "description": "Switch ids, e.g. '1,3,5-40'."},
                "all": {"type": "boolean", "description": "Flip every switch instead of an id list."},
                "out": {"type": "string", "description": "Where to write the plan JSON."},
            },
            "required": ["save", "out"],
            "additionalProperties": False,
        },
    },
    {
        "name": "diff_saves",
        "description": "Byte-diff two saves (before/after one unlock) and write a structured diff JSON.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "before": {"type": "string"},
                "after": {"type": "string"},
                "gap": {"type": "number", "description": "Merge changed bytes within N bytes. Default 8."},
                "json_out": {"type": "string"},
            },
            "required": ["before", "after", "json_out"],
            "additionalProperties": False,
        },
    },
    {
        "name": "infer_unlock_plan",
        "description": "Fit a start+stride flag array from diff files and extrapolate it into a full unlock plan.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "diffs": {"type": "array", "items": {"type": "string"}, "description": "One or two diff JSON paths."},
                "target": {"type": "string", "description": "The save the plan will be applied to."},
                "count": {"type": "number", "description": "Number of slots. Strongly preferred over auto-extend."},
                "stride": {"type": "number", "description": "Pin the stride when inference is ambiguous."},
                "start": {"type": "string", "description": "Pin the array start offset, e.g. 0x100."},
                "auto_extend": {"type": "boolean"},
                "out": {"type": "string"},
            },
            "required": ["diffs", "target", "out"],
            "additionalProperties": False,
        },
    },
    {
        "name": "apply_plan",
        "description": "Dry-run, apply, verify or roll back an unlock plan. Apply always backs up first; rollback re-verifies the backup hash.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "plan": {"type": "string"},
                "action": {"type": "string", "enum": ["dry_run", "apply", "verify", "rollback"], "description": "Default dry_run."},
                "allow_resize": {"type": "boolean", "description": "Permit length-changing patches. Off by default."},
            },
            "required": ["plan"],
            "additionalProperties": False,
        },
    },
]


def _run(script: str, args: list[str]) -> dict[str, Any]:
    cmd = [sys.executable, os.path.join(SCRIPTS, script), *args]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, timeout=600)
    out = (proc.stdout or "") + (proc.stderr or "")
    return {"exit_code": proc.returncode, "output": out[-8000:]}


def _text(res: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": res["output"]}],
            "isError": res["exit_code"] != 0}


def call_tool(name: str, a: dict[str, Any]) -> dict[str, Any]:
    if name == "save_scout":
        args = []
        if a.get("game"):
            args += ["--game", str(a["game"])]
        if a.get("dir"):
            args += ["--dir", str(a["dir"])]
        if a.get("changed_within"):
            args += ["--changed-within", str(a["changed_within"])]
        if a.get("json_out"):
            args += ["--json", str(a["json_out"])]
        return _text(_run("save_scout.py", args))

    if name == "engine_inspect":
        return _text(_run(os.path.join("engines", "rgss_save.py"), ["inspect", str(a["save"])]))

    if name == "plan_unlock_switches":
        args = ["plan-switches", str(a["save"])]
        if a.get("all"):
            args.append("--all")
        elif a.get("ids"):
            args += ["--ids", str(a["ids"])]
        args += ["--out", str(a["out"])]
        return _text(_run(os.path.join("engines", "rgss_save.py"), args))

    if name == "diff_saves":
        args = [str(a["before"]), str(a["after"])]
        if a.get("gap"):
            args += ["--gap", str(a["gap"])]
        args += ["--json", str(a["json_out"])]
        return _text(_run("save_diff.py", args))

    if name == "infer_unlock_plan":
        args = [*[str(d) for d in a["diffs"]], "--target", str(a["target"])]
        if a.get("count"):
            args += ["--count", str(a["count"])]
        if a.get("stride"):
            args += ["--stride", str(a["stride"])]
        if a.get("start"):
            args += ["--start", str(a["start"])]
        if a.get("auto_extend"):
            args.append("--auto-extend")
        args += ["--out", str(a["out"])]
        return _text(_run("infer_plan.py", args))

    if name == "apply_plan":
        action = a.get("action") or "dry_run"
        args = [str(a["plan"])]
        if action == "dry_run":
            args.append("--dry-run")
        elif action in ("verify", "rollback"):
            args.append(action)
        if a.get("allow_resize"):
            args.append("--allow-resize")
        return _text(_run("apply_plan.py", args))

    return {"content": [{"type": "text", "text": f"unknown tool: {name}"}], "isError": True}


def handle(msg: dict[str, Any]) -> dict[str, Any] | None:
    method, mid = msg.get("method"), msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "create-all-cg-save", "version": "1.3.0"},
        }}
    if method in ("notifications/initialized", "initialized"):
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        try:
            return {"jsonrpc": "2.0", "id": mid,
                    "result": call_tool(params.get("name", ""), params.get("arguments") or {})}
        except Exception as exc:  # noqa: BLE001
            return {"jsonrpc": "2.0", "id": mid,
                    "result": {"content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}],
                               "isError": True}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
