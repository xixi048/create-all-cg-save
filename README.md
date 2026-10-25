# create-all-cg-save

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776ab.svg)](https://www.python.org/)

> Create an all-CG save — unlock every CG, gallery, and recollection room in **your own offline single-player saves**.

An agent skill (plus a small zero-dependency Python toolkit) that turns "I want all CGs unlocked"
into a precise, reversible byte patch instead of a downloaded stranger's save file.

**中文说明见 [README.zh-CN.md](README.zh-CN.md).**

## What it does

- Scans the usual save locations on this machine and finds candidate save files for a game
- Identifies the engine (RPG Maker, Ren'Py, Kirikiri, Unity, Siglus, BGI, …)
- For parseable formats (e.g. RPG Maker's Ruby Marshal) it **computes the exact byte offset of every unlock flag**
- For opaque private binaries it reconstructs the unlock flags by **diffing a "before" and an "after" save**, fits the `start + stride` array, and extrapolates to the whole gallery
- Emits a human-readable unlock plan with dry-run, verification, automatic backup, and one-command rollback

It never downloads the game, never touches CG images or game assets, and never replaces your save
with someone else's — it only makes a minimal, surgical edit to a save you already own.

## Two routes

| Route | When | Mechanism |
|---|---|---|
| Engine fast path | Save format is known and parseable | Semantic parsing — jump straight to `switch[N]` / `variable[N]` |
| Generic diff path | Private binary, unknown structure | Byte diff → fit `start + stride` array → extrapolate |

Decision tree lives in [`skills/create-all-cg-save/SKILL.md`](skills/create-all-cg-save/SKILL.md).

## Quick start

```bash
# 1. Find the save file
python skills/create-all-cg-save/scripts/save_scout.py --game <game name>

# 2. RPG Maker VX / VX Ace / XP: inspect structure and current switch state
python skills/create-all-cg-save/scripts/engines/rgss_save.py inspect "Save01.rvdata2"

# 3. Build an unlock plan (flip the given switches ON)
python skills/create-all-cg-save/scripts/engines/rgss_save.py plan-switches \
    "Save01.rvdata2" --ids 1,3,5-40 --out plan.json

# 4. Dry-run → apply → verify (apply backs up automatically)
python skills/create-all-cg-save/scripts/apply_plan.py plan.json --dry-run
python skills/create-all-cg-save/scripts/apply_plan.py plan.json
python skills/create-all-cg-save/scripts/apply_plan.py plan.json verify

# Roll back if anything looks wrong
python skills/create-all-cg-save/scripts/apply_plan.py plan.json rollback
```

Unknown engine? Go through the diff path:

```bash
python skills/create-all-cg-save/scripts/save_diff.py A.save B.save --json ab.diff.json
python skills/create-all-cg-save/scripts/infer_plan.py ab.diff.json \
    --target A.save --stride 4 --count 128 --out unlock-plan.json
```

> `--stride` / `--start` matter. With only one or two observed flag positions the fitted stride is
> ambiguous (a stride-4 array where slots 0 and 5 were unlocked makes GCD report 20). The script
> warns loudly; pin the layout explicitly when you can.

## Verified target

**RPG Maker VX Ace (RGSS3)** — e.g. `Save0X.rvdata2`:

- The save is Ruby Marshal with **two concatenated Marshal streams** (stream 1 is
  `make_save_header` for the load menu, stream 2 is the 11-key `make_save_contents` hash)
- `:switches` → `@data` is a boolean array; `'T'` / `'F'` / `'0'` (nil) are one byte each, so the
  patch is an **equal-length replacement — file size not changed by a single byte**
- Result: 59 switch slots flipped ON, size 617,987 → 617,987 bytes, re-parsed as genuinely `true`,
  and `rollback` restored the file byte-for-byte

## Repository layout

```
create-all-cg-save/                  # repository
├── .claude-plugin/
│   └── marketplace.json            plugin-marketplace manifest (`/plugin marketplace add`)
└── skills/
    └── create-all-cg-save/         the skill itself (auto-indexed by skills.sh & friends)
        ├── SKILL.md                skill entry point (the workflow an agent reads)
        ├── scripts/
        │   ├── save_scout.py       locate candidate saves + engine fingerprinting
        │   ├── save_diff.py        byte-level diff of two saves
        │   ├── infer_plan.py       infer the flag array → unlock plan
        │   ├── apply_plan.py       apply / verify / roll back
        │   ├── common.py           backup, atomic write, hashing
        │   └── engines/
        │       ├── ruby_marshal.py dependency-free Ruby Marshal parser + encoders
        │       └── rgss_save.py    RPG Maker RGSS save adapter
        └── references/
            ├── engines.md          per-engine save locations and formats
            ├── diff-method.md      the full diff-method manual
            ├── unlock-plan-schema.md  diff / plan JSON schemas
            └── safety.md           backup, integrity, and compliance red lines
```

## Install as a skill

Straight from the public repo (no clone needed):

```bash
npx skills add xixi048/create-all-cg-save           # skills.sh / `npx skills` CLI
```

```text
/plugin marketplace add xixi048/create-all-cg-save  # Claude Code plugin marketplace
```

Or copy the folder into your agent's skills directory:

Drop the whole `skills/create-all-cg-save/` directory into your agent's skills directory:

- User level: `~/.workbuddy/skills/create-all-cg-save/`
- Project level: `<repo>/.workbuddy/skills/create-all-cg-save/`

The directory name must match the `name` field in `SKILL.md` frontmatter (`create-all-cg-save`).
The frontmatter follows the standard agent-skill shape: `name`, `description` (what + when, with
Chinese and English trigger keywords), `license`, and `metadata`.

> Why the extra `skills/` level? Directory sites that crawl GitHub (`skills.sh`, SkillsMP,
> `npx skills`, and Claude Code's plugin marketplaces) only look for `skills/<name>/SKILL.md`.
> A skill folder sitting at the repo root is never discovered, no matter how good it is.

> Note: all relative paths inside `SKILL.md` are relative to the **skill directory**, not your
> working directory. `cd` into it first, or prefix the commands with the absolute skill path.

## Use as an MCP server

The whole toolkit is also exposed over MCP (stdio, zero dependencies), so any MCP-capable agent can
drive it without knowing the repo layout:

```json
{
  "mcpServers": {
    "create-all-cg-save": {
      "command": "python",
      "args": ["C:/path/to/create-all-cg-save/mcp/server.py"]
    }
  }
}
```

Tools: `save_scout` · `engine_inspect` · `plan_unlock_switches` · `diff_saves` · `infer_unlock_plan` · `apply_plan`
(`apply_plan` takes `action: dry_run | apply | verify | rollback`; apply always backs up first).

Machine-discoverable index:

```text
https://xixi048.github.io/create-all-cg-save/.well-known/agent-skills/index.json
```

## Requirements

Python 3.8+, **zero third-party dependencies** (standard library only).

On a Windows console with a legacy code page you may need `chcp 65001` (or
`PYTHONIOENCODING=utf-8`) for the Chinese progress output to render correctly.

## Safety model

- Every write is backed up first as `<save>.allcg-bak-<timestamp>` — never an in-place overwrite
- `sha256_before` is verified before patching; a plan built for a different save is refused
- Patches that would change the file length are refused unless `--allow-resize` is passed
- Always dry-run before applying, and always load the game afterwards to confirm

See [`references/safety.md`](skills/create-all-cg-save/references/safety.md) for the full list.

## Known limits

- RPG Maker XP / VX / VX Ace has full automation; MV / MZ is easy when the save is plain JSON
- Ren'Py, Kirikiri, Unity, Siglus, BGI etc. usually need the diff method, and some saves are
  compressed/encrypted end-to-end, where plain diffing simply fails
- Cloud-only saves must be synced locally first
- Unlocking every switch can also trip story branches or game-over conditions — start with the
  IDs you have verified inside the game

## Disclaimer

This tool is for personal research and modification of **offline single-player games you legally own**.
Do not use it on online / multiplayer games, leaderboards, or anything where it could affect other
people. You are responsible for whatever happens to your save — every write is backed up, though.

## License

MIT — see [LICENSE](LICENSE).
