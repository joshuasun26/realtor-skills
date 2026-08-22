---
department: foundation
name: usage-recap
description: >
  Read the local skill-usage log and turn it into a plain-English "your month with the
  library" recap: total runs, most-used skills, least-used or never-used skills, and a
  friendly line the agent can read aloud on the monthly membership office-hour Zoom.
  Trigger on "usage recap", "my month with the library", "what have I been using",
  "office hour recap", "usage summary", or ahead of a scheduled monthly office hour.
  Works entirely offline, off the agent's own machine. Degrades gracefully — with a
  clear friendly message, not an error — if tracking has never been turned on or the
  log is empty.
---

# Usage Recap — the office-hour mirror

Usage tracking in this library is off by default (see `hooks/README.md`). When an agent
has turned it on for themselves and their own written consent, the only thing recorded is
a skill name and a timestamp, appended locally to
`~/.realtor-skills/skill-usage.jsonl`. Nothing leaves their machine.

This skill's only job is to read that one local file and turn it into something a human
enjoys hearing — a short, honest recap of what got used, what did not, and what that
might mean. It is the concrete deliverable behind the Membership tier's monthly
"what shipped" changelog and group office hour.

---

## The check

1. Resolve the tally path: `~/.realtor-skills/skill-usage.jsonl` (or
   `$CLAUDE_PLUGIN_DATA/.realtor-skills/skill-usage.jsonl` if that environment variable
   is set — same resolution logic as `hooks/tally_skill_run.py`).
2. **If the file does not exist**, stop and say so plainly and warmly — see "No data yet"
   below. Do not treat this as an error. Tracking ships disabled by default, so this is
   the expected state for most agents, most of the time.
3. **If the file exists but is empty**, same friendly treatment — tracking was turned on
   but nothing has run since.
4. Otherwise, read it line by line. Each line is one JSON object:
   `{"ts": "...", "skill": "...", "plugin": "realtor-skills"}`. Skip any line that fails
   to parse rather than failing the whole read — a corrupted line is not a reason to lose
   the rest of the month.
5. Filter to the requested window (default: the trailing 30 days, or the calendar month
   if the agent asks for "this month"). If nothing falls in the window but older records
   exist, say that too — "nothing logged in the last 30 days, but there's history from
   earlier" — rather than reporting a flat zero with no context.

## Build the recap

From the filtered records, work out:

- **Total runs** in the window.
- **Most-used skills** — top 3-5 by count, with their counts.
- **Least-used or never-used skills** — compare the skills that appear in the log
  against the full list of installed skills (walk
  `plugins/realtor-skills/skills/*/SKILL.md` the same way `atlas/build.py` does, or read
  `atlas/index.html`'s baked-in skill list if that's faster) and call out anything with
  zero runs in the window by name. This is a signal about the skill or the workflow, not
  a judgment on the agent — frame it that way.
- **A trend line if there's a prior window to compare against** (e.g. this month vs. last
  month's total), but only if you actually have last month's data sitting in the same
  file — never estimate or imply a trend you can't see.

## Output template

Plain text, short enough to read aloud in the office hour without notes.

```
Your month with the library — [date range]

You ran [N] skills, [total] times.

Most used:
  1. [skill] — [count]x
  2. [skill] — [count]x
  3. [skill] — [count]x

Sitting unused this month: [skill, skill, skill]
  (Worth a look together — either they don't fit your workflow yet, or they're solving
  a problem you're not hitting. Either way, that's useful to know.)

One line for the group call:
  "This month I leaned hardest on [top skill] — [N] times — and haven't touched
  [unused skill] at all."
```

**Worked example:**

```
Your month with the library — Jul 22 to Aug 21, 2026

You ran 6 skills, 41 times.

Most used:
  1. listing-package — 14x
  2. sphere-daily — 11x
  3. market-brief — 6x

Sitting unused this month: home-anniversary, follow-up-sequencer
  (Worth a look together — either they don't fit your workflow yet, or they're solving
  a problem you're not hitting. Either way, that's useful to know.)

One line for the group call:
  "This month I leaned hardest on listing-package — 14 times — and haven't touched
  home-anniversary at all."
```

## No data yet

If the file is missing or empty, do not error and do not apologize for a failure that
did not happen. Say something like:

> Usage tracking hasn't been turned on yet, so there's no recap to run — that's expected,
> it ships off by default. If you want this ready for next month's office hour, tracking
> can be switched on locally (nothing leaves your machine — see `hooks/README.md`).

Never invent numbers to fill the gap.

## Privacy note, every time

This skill only ever reads a file on the agent's own machine and only ever displays it
back to that same agent. It has no network capability and must never be given one. If
the agent asks who else can see this recap: no one, unless they choose to say it out
loud on the office-hour call themselves.

## Chains from / into

Standalone. This skill does not chain from or into any other skill in the library — it
reads the output of the (opt-in, disabled-by-default) usage-tracking hook
(`hooks/tally_skill_run.py`) and nothing else. It is not called by, and does not call,
any other skill.

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
