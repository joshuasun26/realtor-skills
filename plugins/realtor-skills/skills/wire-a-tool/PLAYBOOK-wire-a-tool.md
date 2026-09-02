# Let Claude see the tools you already use

### 10 to 25 minutes, depending on the rung. Logged into the tool in your browser; Claude Code signed in.

## What this does for you

Your client info lives in your CRM, your tasks live in something else, and Claude can see
none of it unless you paste. This walks a five-step ladder for any tool, from the best
connection to the simplest, and stops at the first one that works on your plan and your
machine: an official connector, an API key, a CSV export, Claude reading your screen, or
a paste. It never says "it can't be done." It says which step is next.

What comes back: Claude reading your real data in your own account, proved by one real
read ("show me my tasks due this week," "how many contacts have a phone number"), and a
short note in `profile/TOOLS.md` on how you connected so next month you do not have to
remember.

The one rule it will not break: creating the app, clicking Allow, generating a key, and
logging in are your hands. It never types your password and never asks you to paste a
secret into chat. A key goes from the tool's page into a file called `.env`, by you.

## The one command
```
connect [tool] to Claude
```
Open Claude Code **in your business folder** (the one with `profile/` in it). Type the
line with the tool's name. Answer by voice if that is easier.
**First time?** It will ask for two things.
1. What the tool holds and what you want out of it. Then it opens the tool with you and
   looks at one real record.
2. Depending on the step it lands on: a click on Allow in your browser, or a key you
   generate on the tool's settings page and paste into `.env`, or an Export button.

## What you get back
```
Example shape, not a real run

## Asana
Holds: client tasks, one project per transaction
Rung: 1, official connector (claude mcp add ... asana)
Verified: 2026-09-10, "list my tasks due this week" returned 7 real tasks
Export path, if the connector ever breaks: Project Actions > Export > CSV
Secrets: none in this file
```
Yours is built from your data, not this example. It lands at `profile/TOOLS.md` in your
business folder, one section per tool.

## Three things that break, and the fix
1. **The tool's app page or API key page is not available to you** - your plan or your
   workspace admin restricts it. Fix: say "drop to the next rung." A CSV export always
   works, and it is the right first version for most tools anyway.
2. **The one test read comes back 401 or 403** - the key was created without the right
   permission, or it was pasted with a stray space. Fix: generate a new key on the tool's
   page, paste it into `.env` again on one clean line, and say "try the read again." Claude
   will not guess at a fix for a key it cannot see.
3. **It quotes a menu path that is not on your screen** - the vendor moved the menu since
   the path was last read. Fix: screenshot what you see and paste it. Claude reads the
   vendor's own help page again in the session and updates the note for next time.
If it is none of these: screenshot it and paste it to Claude. That is the fastest way
through.

## Make it yours
- "Use the CSV, not the API, for my CRM" - pins the tool to the export rung; saved in
  `profile/TOOLS.md`.
- "Let it create tasks in Asana when I ask" - turns on Level 2 for that tool; it shows
  each change before making it; saved in `profile/TOOLS.md`.
- "Pull my CRM into the morning brief" - Level 3, a scheduled read, only after the first
  read has worked; saved in the brief's task and `profile/STACK.md`.
Say "show me the skill file" and it opens `skills/wire-a-tool/SKILL.md`. Change the
words, save, and the next run uses them.

## How it works, in four lines
It reads the vendor's own developer or help page in the session, and your `.env` for a key
by name, never by value. It decides the rung from what the vendor offers and what your
plan includes, and says why in one line. It writes `profile/TOOLS.md` and, at Level 2, the
one change you asked for after showing it. It never types a password, never stores a
secret anywhere but `.env`, and never writes to a tool you did not ask it to.

## Related
Once a CSV exists, **Load my contacts** (`import my contacts`) takes over. GoHighLevel
has its own playbook, **Set up my GoHighLevel** (`set up my GoHighLevel`). The morning
brief in **Text me from my own laptop** (`set up voice command`) is where a Level 3
scheduled read usually lands.

Still stuck? Text Joshua at 858-585-4853.
