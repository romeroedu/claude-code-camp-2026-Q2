---
name: mud-play
description: Play and automate the local MUD at localhost:4000 with persistent Markdown memory. Use when connecting, logging in, sending commands, reading room output, pursuing a multi-step goal such as reaching a level or defeating a named monster, or updating data/player.md and data/world.md.
---

# Mud Play

## Persistent Memory

Treat `data/player.md` and `data/world.md` as the working memory for every session. Read both before connecting or taking an action. Resolve these paths from the workspace root (the directory containing both `data/` and `mud-play/`); create the `data/` directory or files if they are missing.

- `data/player.md` stores volatile state: the active goal, measurable progress, current room, level/HP/XP, inventory, immediate plan, completed milestones, blockers, and the timestamp or turn of the last update.
- `data/world.md` stores durable discoveries: room and exit mappings, routes, NPCs, monsters, levels, weaknesses, loot, shops, quests, commands, and facts confirmed by live output. Do not put the character's current HP or inventory here.

Keep the existing headings and update the smallest relevant sections. Use Markdown checkboxes for milestones. Replace stale current-state values rather than appending contradictory values. Record uncertain information as `Unverified` until a live command confirms it. Never invent progress or world facts.

## Workflow

Use the bundled client for every MUD session instead of typing raw socket or telnet commands.

1. Read the two memory files. When the user supplies a goal, write it immediately into `player.md` and turn it into measurable milestones; for example: `Reach level 7` and `Defeat <named monster>`. Preserve completed milestones when resuming the same goal.
2. Start with `scripts/mud_client.py`; it connects to `localhost:4000` and logs in with the configured default credentials (`player` / `helloworld`). Use explicit overrides if the server requires different credentials.
3. Establish the live baseline with commands such as `look`, `score`/`status`, and `inventory`. Reconcile the result into `data/player.md` before acting.
4. Select the next safe milestone from the plan. Use `--command` for short actions and `--command-file` for a reviewed sequence. After each meaningful action or combat encounter, read the output before continuing.
5. Persist the result to memory before ending the turn, disconnecting, or changing strategy. Update player progress and add only newly confirmed durable facts to world memory.
6. Use `--interactive` only when a user explicitly wants a continuing session; still save memory at meaningful checkpoints.

If the user names a target monster but the world does not contain verified information about it, add the target to the player goal as `Unverified`, then scout safely before committing to combat.

For a long goal, maintain this loop:

`read memory → observe state → choose one milestone → act → verify output → update memory → repeat`

Break broad goals into milestones appropriate to the game state (for example, learn a route, obtain equipment, gain safe experience, locate the target, then engage it). Do not grind or fight indefinitely: stop when the next action is unsafe, the target is defeated, the goal is complete, or the server is unavailable, and record why.

## Script Usage

```bash
python3 scripts/mud_client.py --command "look"
python3 scripts/mud_client.py --command "inventory" --command "look"
python3 scripts/mud_client.py --command-file commands.txt
python3 scripts/mud_client.py --interactive
```

## Session Rules

- Prefer reading the room output before issuing the next command.
- Keep commands short and explicit.
- If the server presents unexpected login prompts, capture the text and adapt the script rather than hand-rolling socket logic.
- Treat combat and movement as state-changing: verify room, HP, level, XP, inventory, and target status after them when the game exposes those values.
- Record routes only after observing each relevant room/exit; label routes as verified and include the starting room.
- When a goal completes, mark every applicable checkbox complete, write the final verified state, and preserve useful world discoveries for future goals.
- If a command fails or the connection drops, record the failure and last verified state in `player.md`; do not mark the milestone complete.

## Memory Update Format

Keep `player.md` focused and current:

```markdown
## Active Goal
- Goal: ...
- Status: In progress | Complete | Blocked
- Milestones:
  - [ ] ...

## Current State
- Room: ...
- Level / XP: ...
- HP: ...
- Inventory: ...
- Last verified: ...
- Next action: ...
- Blockers: None
```

Keep `world.md` append-friendly but deduplicated:

```markdown
## Known World State

### Locations and Routes
- ... (verified ...)

### Monsters and Combat
- ...

### NPCs, Shops, and Quests
- ...

### Commands and Other Facts
- ...
```
