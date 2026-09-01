---
department: foundation
name: computer-revive
description: >
  Measure what is actually eating RAM on the agent's own computer, explain it in plain
  English, and clean up only what they approve. Never anything with possibly-unsaved
  work, never a system process, never a startup item or system setting. Trigger on
  "revive my computer", "my computer is slow", "check my RAM", "clean up processes",
  "why is my computer crawling", or when the agent says their machine is lagging before
  a call or a showing. Works on Windows (PowerShell) and Mac (ps/Activity Monitor
  equivalents). Ends every run with one prevention habit, never a lecture.
---

# Computer Revive: measure, explain, ask, then clean

An agent's computer slows down the same way everyone's does: browser tabs pile up,
background helper apps never fully close, something got left running from yesterday.
This skill runs the same five-step loop every time: measure, explain, classify, act
only on approval, re-measure. That is how a slow computer becomes a two-minute fix
instead of a reboot-and-hope.

**This skill never kills anything without a green light, and it never touches anything
that isn't a running process.** It does not open Task Manager settings, does not
disable startup items, does not change power plans or system settings. Where a change
like that would help, it says so and lets the agent make it themselves.

---

## Step 1: Measure first

Never guess, never act on a vibe of "it feels slow." Pull real numbers before saying
anything.

**Windows (PowerShell):**
```
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 Name, Id, @{N='RAM_MB';E={[math]::Round($_.WorkingSet/1MB,0)}}
(Get-Process chrome -ErrorAction SilentlyContinue).Count
```

**Mac (ps / vm_stat):**
```
vm_stat
ps -A -o pid,rss,comm | sort -k2 -nr | head -15
ps -A | grep -c "Google Chrome"
```

Record: total RAM, free RAM, the top 10-15 processes by memory with their size in MB,
and a count of browser-related processes (each browser tab commonly runs as its own
process, so a big tab count often explains a big number on its own).

## Step 2: Report in plain English

Translate the numbers, don't dump them. Something like:

> You've got 11.2 of 16 GB in use. The two biggest things eating it: Chrome (38 tab
> processes, about 4.1 GB total) and Zoom, which looks like it's still running in the
> background from your last call at about 900 MB. Everything else is small.

Name the top few hogs with sizes. Skip anything under roughly 150-200 MB unless the
agent asks for the full list. A screenful of small helper processes doesn't help
anyone decide anything.

## Step 3: Classify before touching anything

Every process found in step 1 goes into exactly one bucket. Say which bucket each
named item is in when you report it. Don't just list processes and ask "which ones?"

**(a) Safe to close on your own judgment, no confirmation needed per item**
- Duplicate or orphaned helper processes (a second copy of something the user only
  runs once, an update-checker background task, a crashed process still holding memory)
- Extra tabs' worth of a browser's per-tab processes, but only the count/footprint,
  never the browser window itself (see (b))
- An app the agent has already told you in this conversation they're done with

**(b) Ask first, every time, no exceptions**
- Anything that could hold unsaved work: a document editor, a code editor, a design
  tool, a spreadsheet, a browser window itself (as opposed to background tab bloat)
- Anything the agent hasn't explicitly said they're finished with
- When in doubt, this bucket. A five-second question is cheaper than a lost draft.

**(c) Never touch, full stop**
- Operating system processes and anything the OS itself depends on to keep running
  (on Windows: anything the Task Manager labels as a Windows process or system
  service; on Mac: anything owned by root or shown as an Apple system process)
- Security/antivirus software
- The rule here is: **if you don't recognize what an app does, or if closing it
  could affect anything other than freeing memory, leave it alone and name it as
  "not touching this, unsure what it does" rather than guessing.** Never rely on an
  exhaustive list of "known safe" system names, since new machines have different ones.

## Step 4: Kill only what's approved, then re-measure

- List out exactly what you're about to close, bucket by bucket, and wait for a plain
  yes before closing anything in bucket (a) or (b). Bucket (a) items can be proposed
  together as a batch ("okay to close these six?") rather than one at a time.
  Bucket (b) items need an explicit answer per item or per named group. "Close Zoom
  too?" is a fair batch question, but never fold a possibly-unsaved app into a batch
  the agent didn't specifically see named.
- Close only what was approved.
- Re-run the exact same measurement from Step 1.
- Report before and after, plainly: "You went from 4.8 GB free to 9.1 GB free. Chrome's
  tab count dropped from 38 to 12."

If nothing was approved, that's a fine outcome. Report the numbers and stop. This
skill's job is to make an informed decision easy, not to force a cleanup.

## Step 5: One prevention habit, not a lecture

End every run with exactly one forward-looking habit, picked to fit what you actually
saw, not a generic checklist. Examples of the kind of thing to say (pick the one that
matches what caused today's slowdown, don't recite all of them):

- "Chrome was most of this. Closing and reopening it once a day keeps tab processes
  from compounding."
- "Zoom stayed open from your last call. Worth closing it right after instead of just
  minimizing."
- "A weekly restart clears out anything like this that quietly stacks up."

One sentence. Never a bulleted list of five habits after a two-minute cleanup.

---

## Hard rails

- **Never kill anything in bucket (b) without an explicit yes for that item.** A vague
  "sure, clean it up" from the agent covers bucket (a) only. Bucket (b) items need
  their own answer.
- **Never disable a startup item, never change a system or power setting.** If one
  would help (e.g., "you have twelve apps set to launch at login"), say so as a
  suggestion and stop there. The agent does that themselves in their own settings.
- **8 GB of RAM or less is a hardware ceiling, say so plainly.** On a machine that
  small, a cleanup buys a few minutes of headroom, not a fix. Tell the agent that
  directly rather than running the same steps and implying it solved the problem,
  something like: "This will help for a bit, but 8 GB is genuinely tight for what
  you're running day to day. The real fix here is more RAM, not another cleanup."
- **Never claim a number you didn't just measure.** If a measurement command fails
  (permissions, an unsupported OS version), say so and try the fallback for that
  platform rather than estimating.

## Chains from / into

Standalone. Runs entirely on the agent's own machine, reads nothing from and writes
nothing to any other skill's files, and needs no network access to do its job.

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
