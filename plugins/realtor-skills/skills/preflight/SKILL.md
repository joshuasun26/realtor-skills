---
department: foundation
name: preflight
description: >
  Check whether this machine can run each part of the library before anything is
  attempted: Claude Code and the paid plan, the working folder and profile, git, Python,
  the render browser, ffmpeg, disk and memory. Reports one table, offers each missing
  install one at a time with a yes required, and tiers the library into what runs now,
  what runs if you brought the thing, and what needs an install first. Trigger on "check
  my setup", "am I ready", "preflight", "is my computer ready", "what can I run", "which
  one should I do", "will this work on my laptop", or as the first step of any skill that
  needs a tool it cannot find (Python, Playwright, ffmpeg, git, Node). Do NOT trigger for
  a slow machine (computer-revive), for filling in the profile itself (agent-profile), or
  for creating accounts (ghl-setup, or the stack skills).
---

# Preflight: find out what this laptop can do before promising it

Half the library needs nothing but Claude Code. The other half quietly assumes a headless
browser, ffmpeg, or a login the agent has to bring. A skill that discovers a missing tool
forty minutes in, and then improvises an install, is how a session dies. This skill finds
out in two minutes, says what is missing, and asks before it changes anything.

Reads `profile/AGENT.md` if it exists. Writes `profile/PREFLIGHT.md`, dated.

## The rule that comes first

**Nothing gets installed without naming what, why, and getting a yes for that one thing.**
Installers that ask for an administrator password, any consent screen, and the paid Claude
plan are the agent's own hands, every time. Claude runs the checks, prints the exact line
it would run, and waits. On a company-managed laptop where installs are blocked, it stops,
says so, and hands over the one-paragraph note for their IT person instead of trying a
workaround.

## Levels, so nothing is promised before it is proven

- **Level 1, look.** Every check below, read-only, one table. Nothing changes on the
  machine. This is the default and it is safe to run any time.
- **Level 2, fix.** Each missing tool offered one at a time with the exact install line,
  run only on a yes, verified after with the same check that found it missing.
- **Level 3, tier.** The library sorted for *this* machine: run it now, run it if you
  brought the thing, tonight after an install. Generated from the table, never promised.

## Who does what

| Step | Claude | The agent (their own hands) | Why |
|---|---|---|---|
| Run every check | Yes, read-only | Nothing | Nothing changes |
| Paid Claude plan | Reads whether `claude` opens without a plan warning | Upgrades with their own card if it does not | Payment |
| Package installs (Python, git, ffmpeg) | Prints the line, runs it on a yes | Says yes; types the administrator password if the installer asks | Their machine |
| Homebrew on a Mac, if absent | Prints the brew.sh address and stops | Installs it themselves; it asks for their password | Their machine |
| Playwright and its browser | Runs the two lines on a yes | Says yes | Downloads a browser, about 150 MB |
| Whisper model for video | Says the model download is 1 to 3 GB and offers the no-captions path | Decides | Disk and time |
| Company-managed laptop | Detects the failure, hands over the IT note | Forwards it | Not ours to bypass |

## The checks

Run all of them before saying anything. Report each as PASS, MISSING, or OLD with the
version found. On Windows use PowerShell; on a Mac use the terminal. Do not infer a result
from a filename or from memory; run the command.

| Check | How | If missing or old |
|---|---|---|
| Claude Code installed | `claude --version` prints | Re-run the one-line installer from the install page |
| Plan allows Claude Code | `claude` opens without a plan warning, signed in with the email that pays | Stop here. The upgrade is the agent's card; come back after |
| Working folder | Current folder is the one they will always use; `profile/` exists or can be created here | Create it, say the folder name, tell them to always open Claude Code there |
| Profile | `profile/AGENT.md` exists and `Last updated` is within 180 days | Route to `agent-profile` |
| Git | `git --version` | Windows: git-scm.com, defaults, "Add to PATH", then a NEW terminal window. Mac: `xcode-select --install` |
| Python 3.10+ and pip | `python --version` (Mac: `python3 --version`), `python -m pip --version` | Windows: `winget install Python.Python.3.12`. Mac: `brew install python`. Ask first |
| Playwright + Chromium (render skills) | `python -c "import playwright"` then `python -m playwright install --dry-run chromium` | `pip install playwright` then `python -m playwright install chromium`. Ask first |
| ffmpeg + ffprobe (video skills) | `ffmpeg -version` and `ffprobe -version` | Windows: `winget install Gyan.FFmpeg`. Mac: `brew install ffmpeg`. Ask first, then a NEW terminal |
| Word-level transcriber (video captions) | `pip show faster-whisper` | Offer the install, say the model is 1 to 3 GB, or offer the no-captions path |
| Node 18+ (only if a web page will be hosted) | `node --version` | Windows: `winget install OpenJS.NodeJS.LTS`. Mac: `brew install node`. Ask first, and only if a hosting skill is on the list |
| Free disk | Windows: `Get-PSDrive C`; Mac: `df -h /` | Under 5 GB free: say so, route to `computer-revive` before any install |
| Memory | Windows: `Get-CimInstance Win32_ComputerSystem`; Mac: `sysctl hw.memsize` | 8 GB or less: say the render and video skills will be slow and that `computer-revive` can help, not fix |
| Plugin auto-update | `/plugin`, Marketplaces tab, auto-update for this library | Off is the default. Turn it on in the room; a skill that never updates looks healthy |

**Windows and Mac differ on PATH.** A tool installed a minute ago is not visible to the
terminal that was already open. After any install, close every terminal window and open a
new one before re-running the check. Do not tell them to restart the computer.

## The tiers (Level 3)

After the table, sort the library for this machine. Three words, and the third one is the
honest one.

**Run it now** (nothing beyond Claude Code): `agent-profile`, `agent-voice`,
`compliance-check`, `source-check`, `computer-revive`, `lead-intake`, `followup-queue`,
`followup-sequence`, `listing-intake`, `listing-description`, `meeting-brief`,
`market-brief`, `sphere-audit`, `sphere-message`, `sphere-daily`, `home-anniversary`,
`revocation-watch`, `social-caption`, `content-week`, `wire-a-tool`, `owners-manual`.

**Run it if you brought the thing:** `contact-import` (a CRM .csv or a phone .vcf),
`birthday-watch` (contacts with a birthday column; most phone exports have none),
`market-pull` (the agent's own MLS login; aggregators are forbidden by that skill),
`buydown-math` (a dated lender rate sheet; it blocks without one), `social-scan` and
`social-audit` (Instagram logged in, or screenshots), `ghl-setup` (a GoHighLevel
account on the agent's own card), `voice-command` (Telegram installed on a Windows
agent's phone; a Mac that is not company-managed).

**Tonight, after an install:** `carousel-render`, `listing-carousel`, `listing-flyer`,
`market-carousel`, `open-house-flyer`, and the three orchestrators `listing-package`,
`market-update-package`, `open-house-package` (Python plus Playwright and Chromium);
`video-talking-head` and `video-event-recap` (ffmpeg, and a transcriber for captions;
30 to 60 minutes on first run); `open-house-signin` (a host for the page).

Print the three lists with the missing tool named next to each "tonight" item and the
install line it needs. That is the answer to "which one should I do."

## Output

`profile/PREFLIGHT.md`:

```
# Preflight, YYYY-MM-DD
Machine: Windows 11 | macOS 15, 16 GB, 41 GB free
Claude Code 2.x.y, plan OK, folder: <name>

| Check | Result | Version / note |
|---|---|---|
| ...   | PASS / MISSING / OLD | ... |

Run it now: ...
Run it if you brought the thing: ...
Tonight, after an install: ...

Installed this run (each on a yes): ...
Declined or blocked: ...
```

Overwrite it on every run; the date is the point. Other skills read the table instead of
re-checking.

## What this skill will not claim

- A version print is not a working render. This skill proves a tool is present, not that
  a carousel comes out; the render skill's own first run proves that.
- It will not fix a slow machine. That is `computer-revive`, and this skill says so
  instead of closing programs.
- It will not put a skill in "run it now" that it did not check the requirements of. If
  a new skill is not in the lists above, it says "not tiered yet" rather than guessing.
- It will not install anything on a company-managed machine that refuses, and it will not
  suggest a way around the refusal.

## Chains from / into

Called first by `carousel-render`, `video-talking-head`, `video-event-recap`,
`voice-command`, and any skill that hits a missing tool. Routes to `agent-profile` when
the profile is missing and to `computer-revive` when memory or disk is the problem.
`owners-manual` reads `profile/PREFLIGHT.md`.

If the user asks how this works, what it needs, or how to customize it, read
`PLAYBOOK-preflight.md` in this folder and answer from it.

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
