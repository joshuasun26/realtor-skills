# Find out what your laptop can run before you spend an hour on it

### 2 minutes. Nothing beyond Claude Code.

## What this does for you

Half of this library needs nothing but Claude Code. The other half quietly needs a
program you may not have: a hidden browser to draw carousels, ffmpeg to cut video, your
MLS login, a contacts file with birthdays in it. Finding that out forty minutes into a
session, on a laptop that then needs an install, is how an afternoon disappears.

What comes back is one table of what your machine has and what it is missing, then three
short lists: what you can run right now, what you can run if you brought the thing it
needs, and what to set up tonight with the install line already written out.

The one rule it will not break: it installs nothing without naming it, saying why, and
getting a yes from you for that one thing. Anything that asks for your administrator
password, and the paid Claude plan itself, are your hands.

## The one command
```
check my setup
```
Open Claude Code **in your business folder** (the one with `profile/` in it). Type the
line. Answer by voice if that is easier.
**First time?** It asks nothing. It runs the checks and shows the table. If it offers an
install, say yes or no to each one.

## What you get back
```
Example shape, not a real run

Preflight, 2026-09-10
Machine: Windows 11, 16 GB, 41 GB free
Claude Code 2.1.x, plan OK, folder: my-ops

| Check                    | Result  | Note                          |
| Git                      | PASS    | 2.4x                          |
| Python 3.10+             | PASS    | 3.12                          |
| Playwright + Chromium    | MISSING | pip install playwright ...    |
| ffmpeg                   | MISSING | winget install Gyan.FFmpeg    |
| Profile                  | PASS    | updated 12 days ago           |
| Plugin auto-update       | OFF     | turn it on: /plugin           |

Run it now: profile, voice, compliance check, follow-up queue, meeting brief ...
Run it if you brought the thing: contacts (a .csv or .vcf), birthdays, MLS pull ...
Tonight, after an install: carousels and flyers (Playwright), video (ffmpeg)
```
Yours is built from your data, not this example. It lands at `profile/PREFLIGHT.md` in
your business folder, dated, and other skills read it instead of re-checking.

## Three things that break, and the fix
1. **It says a tool is missing right after you installed it** - the terminal that was
   already open cannot see a program installed a minute ago. Fix: close every terminal
   window, open a new one, type `check my setup` again. Do not restart the computer.
2. **"Claude Code needs a paid plan" or it will not open** - the plan on the account you
   signed in with does not include Claude Code, or you signed in with a different email
   than the one that pays. Fix: sign in with the email that pays; if that is the free
   plan, the upgrade is yours to make with your own card, then come back.
3. **The install fails with a permissions error** - the laptop is managed by your office
   and blocks installs. Fix: nothing here, and that is deliberate. Ask Claude for the
   one-paragraph note for your IT person and forward it.
If it is none of these: screenshot it and paste it to Claude. That is the fastest way
through.

## Make it yours
- "Skip the video checks, I will never cut video here" - drops ffmpeg and the transcriber
  from the table; saved as a line in `profile/PREFLIGHT.md`.
- "Always ask before running the install lines" - already the default, and saying it
  once records the preference in the skill file so it never changes.
- "Add a check for [tool]" - adds one row to the table; saved in the skill file.
Say "show me the skill file" and it opens `skills/preflight/SKILL.md`. Change the
words, save, and the next run uses them.

## How it works, in four lines
It reads the versions your machine reports for Claude Code, git, Python, the render
browser, ffmpeg, disk and memory, and the date on your profile. It decides which of three
lists each skill belongs in, from what it found. It writes `profile/PREFLIGHT.md` and
nothing else. It never installs anything without a yes, and never on a managed laptop
that refuses.

## Related
Runs first inside **Build the carousel** (`carousel-render`), the two video skills, and
**Text me from my own laptop** (`set up voice command`). Sends you to **Set up my profile**
(`set up my profile`) if the profile is missing and to **Get your slow computer back**
(`my computer is slow`) if memory is the problem.

Still stuck? Text Joshua at 858-585-4853.
