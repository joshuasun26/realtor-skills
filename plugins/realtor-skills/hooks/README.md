# Usage tracking — off by default, and it stays off until it is disclosed

This folder ships a hook that can tally which skills get run. It is **not active.**

## Why it exists

Knowing which skills are actually used tells you three useful things: which ones to
improve, which ones to delete, and which clients are getting real value versus quietly
drifting away before they say so.

## Why it is off

Recording a paying client's activity without telling them is a betrayal of the
relationship, whatever the intent. The same feature is welcome when it is stated up
front: *"I can see which skills you use, so I know what to improve for you."*

## Before enabling it on any client machine

All four, in this order:

1. **The client agreement says so in writing.** Name what is collected (skill names and
   timestamps), what is not (message content, contact data, file contents), where it is
   stored (their machine), and how they turn it off.
2. **The client has read that clause and signed.**
3. **The client can switch it off at any time** by deleting one file, and they know which
   file.
4. **Nothing is transmitted anywhere** unless a separate, explicitly agreed mechanism
   exists. This script has no network capability and it must never be given one.

## How it is wired (two switches, both required)

**Switch 1 — the file name.** Claude Code auto-loads a plugin's hooks from the exact
path `hooks/hooks.json` — it does this by convention, whether or not
`plugin.json` declares a `"hooks"` key. (The manifest key only lets you point at a
*different* path; it is not a gate. Verified against Claude Code's plugin docs and
confirmed with `claude plugin details`, which reports the hook as loaded even with no
`"hooks"` key in the manifest.) So the file in this folder ships as
**`hooks.json.disabled`**, not `hooks.json` — the renamed extension is what actually
keeps it inactive. To enable it, rename `hooks.json.disabled` to `hooks.json`. Do not
add a `"hooks"` key to `plugin.json` as a substitute for renaming the file — that step
alone does nothing.

**Switch 2 — the opt-in marker on the machine.** Create an empty file:

```
~/.realtor-skills/USAGE-TRACKING-ENABLED
```

Without that file, the script exits immediately even if the hook fires. This is the
switch the client controls. Deleting it stops all recording.

## What gets written

One JSON object per line in `~/.realtor-skills/skill-usage.jsonl`:

```json
{"ts": "2026-01-15T09:12:04-08:00", "skill": "listing-package", "plugin": "realtor-skills"}
```

Timestamp, skill name, plugin name. Nothing else. No arguments, no content, no contacts.

## Reading it

It is plain JSONL on the client's own machine. Count the lines by skill name. If a skill
has not been run in ninety days, that is a signal about the skill, not about the client.
