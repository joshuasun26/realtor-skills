---
department: foundation
name: safe-autonomy
description: >
  Stop Claude Code asking permission for every step, without removing the stops that
  matter. Sets up three layers on this machine: a deny list the machine refuses outright,
  an ask list that still prompts even in bypass mode (anything that leaves the machine or
  spends money), and the standing rules in CLAUDE.md for the judgment no setting can
  enforce. Verifies each layer with a live test before saying it works. Trigger on "stop
  asking me permission", "bypass permissions", "dangerously skip permissions", "yolo
  mode", "auto approve", "it asks me too much", "make it faster", "turn off the prompts",
  "is bypass mode safe", or when an agent is clicking Allow on everything without reading
  it. Do NOT trigger for a machine that cannot run something (preflight), for connecting
  an outside tool (wire-a-tool), or for cleaning up after a send that already went wrong.
---

# Safe autonomy: fast without being reckless

The permission prompt is not the safety system. It looks like one, which is the problem.
By the fortieth prompt in a session nobody is reading them, everybody is clicking Allow,
and the one prompt that actually mattered gets the same reflex click as the thirty-nine
that did not. Prompt fatigue does not make an agent safer. It makes the operator numb.

So the honest move is not "leave the prompts on and feel careful." It is: turn the prompts
off for the ninety-five percent that are noise, and put real, unclickable stops on the
five percent that can cost money, credibility, or a client relationship.

That is what this skill installs. Three layers, each doing a job the other two cannot.

## The three layers

| Layer | Where it lives | What it catches | Can it be clicked past? |
|---|---|---|---|
| **1. Deny** | `settings.json` `permissions.deny` | Destructive commands: wiping folders, force pushes, hard resets | No. The machine refuses. There is nothing to click |
| **2. Ask** | `settings.json` `permissions.ask` | Anything that leaves the machine or spends money: sends, posts, deploys, payments | It still prompts, even in bypass mode. One prompt, rare enough to actually be read |
| **3. Standing rules** | `CLAUDE.md` in the working folder | Judgment: approval that does not carry forward, numbers without a source, writing in their name | Only by the agent choosing to. This layer is a promise, not a wall. Say so out loud |

**Layer 2 is the one people leave out, and it is the one that does the work.** A deny list
stops the agent from destroying their own machine, which is not the common failure. The
common failure is a reasonable-looking message going to the wrong list at the wrong time,
and the agent finding out about it from a reply.

## What bypass mode does not do

Say all of this out loud before touching a setting. An agent who thinks bypass still means
"supervised" will use it in places it should never be used.

- **It does not make Claude careful.** It removes the ask. Nothing else changes.
- **It does not undo anything.** There is no trash can for a deleted file and no recall on
  a sent text. Git is the only real undo, which is why it is a precondition below.
- **It does not sandbox the folder.** Claude can read and write anything the agent's own
  Windows or Mac login can reach, which on most laptops is everything. That is why the
  working-folder rule is not optional.
- **It does not know what is confidential.** Client financials, a signed purchase
  agreement, and a grocery list all look the same to it.
- **It is not for a shared or brokerage-managed laptop.** If IT owns the machine, stop and
  route to IT. Some organizations disable bypass mode by policy, and the agent will see
  that as a policy message rather than a bug.

## Before you turn it on

Three preconditions. Do not skip one to save five minutes. Each exists because of a
specific way this goes wrong.

1. **A working folder, and only that folder.** One dedicated folder the agent always opens
   Claude Code in. Never the Desktop, never Documents, never the home directory. A bypass
   session opened at the top of the home directory has the whole machine in reach and no
   reason not to wander. Confirm the folder by name before continuing.
2. **An undo layer, which means git.** In the working folder: `git init`, then one commit
   of everything already there. This is the only real answer to "it changed something and
   I want it back." If git is missing, route to `preflight` first. Local only is fine.
   Nothing has to be pushed anywhere.
3. **A backup that is not on this machine.** External drive or cloud folder, and it has to
   have actually run at least once. Say the date of the last run out loud. "It is set up"
   is not the same as "it has run."

If any of the three is missing, fix that one and come back. An agent who turns on bypass
with no git and no backup has not gone faster. They have removed the brakes.

## Level 1, look before changing anything

Read the current state and report it. Change nothing yet.

- Find the settings file: `~/.claude/settings.json` on Mac, `C:\Users\<name>\.claude\settings.json`
  on Windows. A per-project `.claude/settings.json` in the working folder overrides it.
- **Back it up before the first edit.** Copy it to `settings.json.bak-<today>` and say the
  filename out loud. Every later step is recoverable from that one file.
- Report as a short table: current `defaultMode`, what is already in `allow`, `ask` and
  `deny`, whether a `CLAUDE.md` exists in the working folder, and whether that folder is a
  git repo with a clean status.
- If `defaultMode` is already `bypassPermissions` and `ask` is empty, say plainly that the
  machine is running with no middle layer at all, and that this is the gap being closed.

## Level 2, install the three layers

Show the agent the exact block before writing it. Write it, then verify it.

### Layer 1, the deny list

Machine-enforced. These never run, in any mode, with no prompt to click through.

```json
"deny": [
  "Bash(rm -rf:*)",
  "Bash(sudo rm:*)",
  "Bash(git push --force:*)",
  "Bash(git push -f:*)",
  "Bash(git reset --hard:*)",
  "Bash(git clean -fd:*)",
  "Bash(Remove-Item -Recurse -Force:*)",
  "Bash(rd /s:*)",
  "Bash(del /s:*)"
]
```

The last three are the Windows spellings of the first one. Include them on a PC, or the
deny list has a hole in it shaped exactly like the most common way a Windows folder gets
wiped by accident.

### Layer 2, the ask list

Still prompts, even under bypass. This is the layer being paid for. Everything in it has
one thing in common: it reaches a person outside the machine, or it spends money.

```json
"ask": [
  "Bash(git push:*)",
  "Bash(gh pr create:*)",
  "Bash(npm publish:*)",
  "Bash(vercel:*)",
  "Bash(curl -X POST:*)",
  "Bash(curl -X PUT:*)",
  "Bash(curl -X DELETE:*)"
]
```

Then add, by exact name, every connected tool that can send, post, or spend.

**Do not guess at the names.** Read the live list off that machine first. A rule with a
misspelled tool name is worse than no rule at all: it looks like a guardrail on the page
and enforces nothing. Ask Claude to list its own available tools, take the ones that send
an email or a text, post to social, move money, or write to a CRM, and add each one by the
exact name that machine uses. What to look for: anything with `send`, `post`, `publish`,
`draft_send`, `payment`, or `delete` in the name.

**Verify this layer or do not claim it.** It is the only layer whose failure is silent.
After writing it, in a fresh session, have the agent ask Claude to run one harmless command
from the ask list, `git push --dry-run`, and confirm a prompt appears. If no prompt appears,
say so plainly and stop. Do not describe the setup as finished.

### Layer 3, the standing rules

Written into `CLAUDE.md` in the working folder, where they load into every session. These
are the ones no setting can enforce, which is exactly why they get written down instead of
remembered. Adapt the wording to the agent. Keep every rule.

```markdown
## Standing rules

- **Show me the copy before anything sends.** Who it goes to, the subject, the words.
  Drafting and staging need no permission at all. Only the send is gated.
- **Approval never carries forward.** A yes on one batch is not a yes on the next batch,
  the next wave, or the same list tomorrow. New batch, new ask.
- **Ambiguity means stop.** "Looks good" and silence are not a go. Ask in one line and wait.
- **Never write a number I did not open a source for.** Not from memory, not from an
  earlier message, not from a past session. Those are leads, not evidence. If it cannot be
  sourced, remove it rather than hedge it. A hedged wrong number is still wrong.
- **Never a password, a card number, or a verification code.** Those are my own hands,
  every time, no exceptions, including when I am the one saying it is fine.
- **Say plainly what did and did not happen.** Never report a send as done when the call
  failed. Count them and name anything that did not go.
- **Client files are confidential.** Nothing from a client folder gets uploaded, published,
  or pasted into an outside tool without me saying so for that specific file.
```

### Then set the mode

Only after all three layers are in and Layer 2 has been verified:

```json
"defaultMode": "bypassPermissions"
```

Quit Claude Code fully and reopen it. Settings load at startup. An edit made mid-session
does nothing until the restart, and that is the single most common reason someone thinks
the setup did not work.

## Level 3, the drill

Five minutes, the agent's own hands, fresh session, in the working folder. Anything that
fails gets fixed before they trust this on real work.

| # | Ask Claude to | It passes when |
|---|---|---|
| 1 | Create and edit a scratch file in the working folder | It just does it. No prompt |
| 2 | Run `git push --dry-run` | It prompts. **If it does not, Layer 2 is not live** |
| 3 | Draft a text to a contact and stop before sending | It shows the copy and waits |
| 4 | Run `rm -rf` on a scratch folder | Refused outright. No clickable prompt |
| 5 | State a number about their business from memory | It declines and names what it would open instead |

Record the result and the date in `profile/AUTONOMY.md`, including anything that failed. A
checklist that only records passes is decoration.

## The honest rails

- **Never set this up for someone who is not in the room.** The agent runs the drill with
  their own hands. Someone who has never watched a prompt appear has no idea what its
  absence means.
- **A missing prompt is not proof of a working rule.** It is equally consistent with a typo
  in a tool name. Test 2 is what separates those two, which is why it is not optional.
- **This changes the machine globally, not one project.** Everything the agent ever opens
  Claude Code on inherits it. If they do work inside someone else's folder or repo, say
  that out loud before writing the file.
- **When something does go out wrong, the first move is to say so.** Then check every live
  surface still carrying it. Silence is how a small error becomes the one that ends a
  relationship.
- **Revert is one line.** Set `defaultMode` back to `default`, or restore the `.bak` file
  from Level 1, then restart. Tell the agent this before they say yes, not after.

## Related

`preflight` for whether git and the rest of the toolchain are even on the machine.
`owners-manual` for writing the finished setup down so it survives being forgotten.
`compliance-check` for the fair housing and advertising review that Layer 3 leans on.
