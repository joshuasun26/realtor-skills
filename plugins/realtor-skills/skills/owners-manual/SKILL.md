---
department: foundation
name: owners-manual
description: >
  Write the owner's manual for everything installed on this machine, from what is actually
  on disk: each piece, the one command that runs it, where it writes, and what to do when
  it breaks, plus the six things that break in the first three weeks and their fixes.
  Trigger on "write my owner's manual", "write my playbook", "what is installed on this
  machine", "document my setup", "what do I do when it breaks", "it stopped working",
  "nothing texted me this morning", "what did we set up", or at the end of an install when
  the agent is about to run the system alone. Do NOT trigger for how one skill works (that
  skill's own playbook), for a slow machine (computer-revive), or for checking tools
  before an install (preflight).
---

# Owner's manual: the system documents itself, in front of the owner

The handoff moment in any install is the agent watching their own Claude write down what
is on their machine and how to use it. A manual written from a template describes some
other setup. This one reads the folder, the profile, the scheduled tasks and the plugin,
and writes only what is there. It is also the first thing to run when something stops
working, because the fix for most week-two failures is already in it.

Reads everything in `profile/`, `.env` (key names only), `voice/`, `data/`, `daily/`,
`records/`, the scheduled task list, and the installed plugin version. Writes
`OWNERS-MANUAL.md` in the workspace root.

## The rule that comes first

**This skill reads the machine; it changes nothing.** It uninstalls nothing, edits no
task, deletes no file. It never prints a secret: `.env` appears in the manual as a list of
key names, never values. Any fix that involves signing in, a permission dialog, or a
password (Claude Code's sign-in, a macOS grant, a token minted again) is the agent's own
hands; the manual says which button, and the agent clicks it.

## Levels, so nothing is promised before it is proven

- **Level 1, the inventory.** What is actually here, read from disk and from the system:
  profile files and their dates, data files and row counts, the voice wire and its
  transport, scheduled tasks and when each last ran, the plugin version and whether
  auto-update is on. Nothing described that was not found.
- **Level 2, the manual.** For each installed piece: the one command to run it, what it
  reads, what it writes, what it never does, and what to do when it breaks. Written from
  the inventory, in the agent's words where they gave them.
- **Level 3, the drill.** The six known breakages run live with the agent: restart a stale
  session, confirm a task actually fired, change one word in a skill file and see the next
  run use it. The drill is what turns a document into a habit.

## Who does what

| Step | Claude | The agent (their own hands) | Why |
|---|---|---|---|
| Inventory | Reads the folders, the task list, `/plugin list`, `.env` key names | Nothing | Read-only |
| Support terms | Asks who installed this, what the support window is, what counts as broken-broken | Answers, in their words | Not invented |
| Write the manual | Writes `OWNERS-MANUAL.md` | Reads it on the spot, corrects anything wrong | Their manual |
| The drill | Names each step | Does each step at the keyboard | They will need it alone |
| Re-auth, grants, tokens | Names the exact path | Signs in, clicks Allow, mints again | Credentials |
| Re-run later | Edits the manual in place, dated, keeps the change log | Nothing | It accumulates |

## The inventory, in order

1. **Profile.** `profile/AGENT.md` (name, brokerage, `Last updated`), `profile/VOICE.md`,
   `profile/STACK.md` sections, `profile/TOOLS.md` sections, `profile/PREFLIGHT.md` date.
   Flag any `TO CONFIRM WITH BROKER` still open; it blocks every public piece.
2. **Data.** `data/contacts.csv` row count and the count with a birthday; `data/pipeline.csv`
   if present; `listings/` folders; `records/sent-log.md` last entry date; `daily/` newest
   file. Counts and dates only, never the contents.
3. **The voice wire.** Transport from `profile/STACK.md`, the scripts present in `voice/`,
   which `.env` keys exist (names only), the working hours, and whether the loop-guard
   check is recorded as passed.
4. **Scheduled tasks.** The list, each with its schedule and its last run if the system
   shows one. A task with no last run is reported as "never fired yet," not as working.
5. **The plugin.** Version from `/plugin list`, and whether auto-update is on for this
   marketplace. Off is the default and it is the most common silent failure.
6. **Tools.** `git`, `python`, `ffmpeg`, Playwright: from `profile/PREFLIGHT.md` if it is
   under 30 days old, otherwise run `preflight` first.

## The manual

`OWNERS-MANUAL.md`, in this order, under 200 lines:

```
# Owner's manual: <agent name>'s system
Written YYYY-MM-DD by the system itself, from what is installed here. Re-run "write my
owner's manual" after any change.

## What is here
One line per piece, from the inventory. Only what was found.

## The daily habit
Open Claude Code in this folder. Type /clear at the start of every day. Say
"good morning" (sphere-daily) or wait for the brief on your phone. Say "save that to
memory" when you correct something.

## Each piece, and the one command
For every installed skill or wire: the trigger phrase, what it reads, what it writes,
what it never does. Taken from each skill's own description, not paraphrased into a
promise the skill does not make.

## When it breaks
The table below, with the fix lines adjusted to this machine (Mac or Windows, iMessage or
Telegram).

## Support
Who installed this, what the support window is and when, what counts as broken-broken,
and what a new build costs. In the agent's own words from this session. Blank if they
did not say.

## Change log
YYYY-MM-DD: first manual.
```

## When it breaks: the six known failures, in the order they happen

Every one of these has happened on a real install. None is a guess, and none is the
agent's fault.

| Days | What they see | Why | The fix, in the manual |
|---|---|---|---|
| 1 to 3 | Nothing fires. No brief this morning. | Laptop asleep, lid closed, or the task never had an awake machine. | Is the laptop open and plugged in? Scheduled tasks need an awake machine. Run the task by hand once; if it works by hand, the clock is the problem, not the task. |
| 3 to 7 | "Not logged in," or a task runs and nothing replies. | The Claude Code sign-in lapsed. | Type `claude`, sign in again with the same email that pays for the plan. One line, their hands. |
| 7 to 10 | The wire went quiet, or on a Mac it started replying to itself. | Mac: the `[claude]` prefix was edited out, or the cursor replayed history. Windows: the `.env` file moved or the token changed. | Mac: `python voice/imessage_poll_commands.py --reset`, then check the prefix in the reply script. Windows: re-run the test send from `voice-command` Level 1 and read the response. |
| 10 to 14 | A skill someone mentioned is not here. | Auto-update is off, the default for this marketplace. | `/plugin update realtor-skills@realtor-skills`, then `/plugin`, Marketplaces, auto-update on. |
| 14 | They stopped opening it. | Not a bug. The friction list went unanswered, or the first win was not theirs. | Text the friction list to whoever installed this. Then run one small thing that worked before, today. |
| 14 to 21 | It got slow and dumb. | The session context filled up; nobody started fresh. | `/clear` at the start of every day. If it is still slow, `computer-revive`. |

If it is none of these: screenshot it and paste it to Claude. That is the fastest way
through, and Claude will say which of the six it is closest to.

## The drill (Level 3)

Run each with the agent's hands, in this order, five minutes total:

1. Type `/clear`, then ask one question the profile answers. A stale session is now a
   fresh one and they have seen the difference.
2. Open the scheduled task list; pick the brief; run it now; confirm it landed on the
   phone. They have seen the difference between "scheduled" and "fired."
3. Open one skill file (say "show me the skill file for birthdays"), change one word in
   its output format, save, run it. They have seen that the words in the file are the
   behavior.
4. Say "save to memory: <one thing they corrected today>." They have seen how it learns.

Record in the manual's change log that the drill was done and the date.

## What this skill will not claim

- It will not list a task as working because it is scheduled. Only a last-run time the
  system shows, or a run done in the session, counts.
- It will not claim the plugin is current without reading the version from `/plugin list`
  in that session.
- It cannot see a phone. "The brief lands" is the agent's word, recorded as such.
- It will not fill in support terms, prices, or a support window the agent did not state.
  Blank is correct; invented is not.
- It will not describe a skill as installed that is not in `/plugin list` or in the
  workspace, even if the design for it exists somewhere.

## Chains from / into

Run at the end of an install and any time the agent asks what is wrong. Reads the output
of `preflight`, `agent-profile`, `voice-command`, `wire-a-tool`, `ghl-setup`,
`contact-import`, and `sphere-daily`. Routes to `computer-revive` for a slow machine and
to the owning skill for any one piece's fix.

If the user asks how this works, what it needs, or how to customize it, read
`PLAYBOOK-owners-manual.md` in this folder and answer from it.

---

<!-- self-improvement-loop v1 -->

## Self-improvement loop

Before ending a run of this skill, review the run:

1. Did any step fail, stall, or need a workaround you had to invent?
2. Did the user correct, reject, or rewrite something meaningful in the output?
3. Did you discover something a future run would want to know (a path that moved, a
   tool that replaced another, a preference they stated out loud)?

If yes to any, propose a specific edit to this SKILL.md in one or two lines and ask
whether to apply it. Propose only changes that would alter a future run's behavior --
skip cosmetic rewording, and never propose more than two edits at once.

Do not edit this file without their go-ahead. If they say no, drop it and do not re-raise
the same suggestion in a later run of the same session.
