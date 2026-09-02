# Your system writes its own owner's manual, and fixes itself with it

### 10 minutes. Nothing beyond Claude Code. Run it at the end of an install and again whenever something stops working.

## What this does for you

At the end of an install you have a laptop full of things that work and no idea what they
are called. This makes your own Claude read the machine and write it down: every piece
that is installed, the one sentence that runs it, where it saves things, and what to do
when it breaks. It is written from what is actually on your computer, not from a
template, so it matches your setup and nobody else's.

What comes back is one file, `OWNERS-MANUAL.md`, in your business folder, plus a
five-minute drill where you do each fix once with your own hands: start a fresh session,
prove a scheduled task fired, change one word in a skill and watch the next run use it.

The one rule it will not break: it reads; it changes nothing. It never uninstalls, never
edits a schedule, never deletes a file, and never prints a password or a key. If a fix
means signing in or clicking a permission, that is you, and it tells you which button.

## The one command
```
write my owner's manual
```
Open Claude Code **in your business folder** (the one with `profile/` in it). Type the
line. Answer by voice if that is easier.
**First time?** It will ask for one thing: who installed this, when your support window
is, and what counts as broken-broken. Answer in your own words. It writes those down
exactly and invents nothing.

## What you get back
```
Example shape, not a real run

# Owner's manual: Jane's system
Written 2026-09-12 by the system itself.

## What is here
Profile (updated 9/5), voice file, 412 contacts (61 with birthdays),
Telegram wire (verified 9/5), morning brief 7:00 weekdays (last ran today),
plugin realtor-skills 0.3.0, auto-update ON

## When it breaks
Days 1-3   No brief          Laptop asleep. Open it, plug in, run the task by hand.
Days 3-7   "Not logged in"   Type claude, sign in with the email that pays.
Days 7-10  Wire went quiet   Say "send me a test message" and read the reply.
Days 10-14 Missing a skill   /plugin update realtor-skills@realtor-skills
Day 14     Stopped opening   Text your friction list. Run one small thing today.
Days 14-21 Slow and dumb     /clear at the start of every day.

## Support
Installed by: <as you said it>. Window: Tuesdays, 15 minutes, by text.
```
Yours is built from your data, not this example. It lands at `OWNERS-MANUAL.md` in your
business folder.

## Three things that break, and the fix
1. **It lists a task as "never fired yet" that you are sure runs** - it reports only a
   last-run time the system shows. Fix: run the task by hand once while it watches, and
   say "write my owner's manual" again. Now the line has a real time on it.
2. **It says the plugin is out of date or auto-update is off** - that is the most common
   silent failure and it is not your fault; off is the default. Fix: type
   `/plugin update realtor-skills@realtor-skills`, then `/plugin`, Marketplaces, and
   turn auto-update on.
3. **The support section is blank** - you did not say who installed it or when the window
   is, and it will not guess. Fix: say it in one sentence and it fills the section in.
If it is none of these: screenshot it and paste it to Claude. That is the fastest way
through.

## Make it yours
- "Add a section on how I like the brief formatted" - adds your preference to the manual
  and to `profile/STACK.md`.
- "Put the fixes on one printable page" - writes a one-page card from the "When it breaks"
  table, saved next to the manual.
- "Re-write it, we added the listing engine" - re-reads the machine and edits the manual
  in place, with a dated line in its change log.
Say "show me the skill file" and it opens `skills/owners-manual/SKILL.md`. Change the
words, save, and the next run uses them.

## How it works, in four lines
It reads your profile folder, your data files (counts and dates only), the voice wire,
the scheduled task list, and the installed plugin version. It decides what is actually
here and what has actually run, from evidence, not from what was planned. It writes
`OWNERS-MANUAL.md` and nothing else. It never changes a setting, never prints a secret,
and never claims a task works because it is scheduled.

## Related
Reads the results of **Find out what your laptop can run** (`check my setup`) and **Text
me from my own laptop** (`set up voice command`). Sends a slow machine to **Get your slow
computer back** (`my computer is slow`).

Still stuck? Text Joshua at 858-585-4853.
