# Free up RAM so your laptop stops crawling

### 5 minutes. Nothing beyond Claude Code.

## What this does for you

Your laptop slows down the same way every realtor's does: browser tabs pile up, Zoom never fully closed, something from yesterday is still holding memory.

You say one line. Claude measures what is actually using RAM, explains it in plain English, and only closes what you approve. Then it measures again so you can see the before and after.

It will never kill a process that might hold unsaved work without a clear yes from you, and it will never touch system processes or change startup settings.

## The one command

```
revive my computer
```

Open Claude Code **in your business folder** (the one with `profile/` in it). Type the line. Answer by voice if that is easier.

**First time?** Nothing to gather. It runs on your machine with built-in OS tools (PowerShell on Windows, `ps` / `vm_stat` on Mac).

## What you get back

`Example shape, not a real run`

```
You've got about 11 GB of 16 GB in use.
Biggest items:
- Chrome (many tab processes, several GB total)
- Zoom still running in the background from your last call

Safe to close as a batch: orphaned helpers A, B, C.
Ask first: Zoom, the browser window itself.

Okay to close the helpers? Close Zoom too?
```

Yours is built from your data, not this example. Nothing is written to disk; the report lives in the chat, then a one-sentence prevention habit at the end.

## Three things that break, and the fix

1. **It closed something you still needed, or it refused a vague "clean it up"** - bucket (b) items need their own yes. (*"Never kill anything in bucket (b) without an explicit yes for that item. A vague 'sure, clean it up' from the agent covers bucket (a) only."*) Fix: name the app ("close Zoom") or say yes to each named group.

2. **The numbers look guessed or the measure step failed** - a failed command is not an estimate. (*"Never claim a number you didn't just measure."*) Fix: paste the error, then say "try the fallback for my OS" so it re-runs the platform measure commands.

3. **Cleanup helped for ten minutes, then it crawled again on a small machine** - low RAM is a ceiling, not a habit problem. (*"8 GB of RAM or less is a hardware ceiling, say so plainly."*) Fix: treat the cleanup as temporary headroom; the real fix is more RAM, not another revive loop.

If it is none of these: screenshot it and paste it to Claude. That is the fastest way through.

## Make it yours

- "Always propose Chrome tab cleanup first" - changes which habit it suggests after a run; Claude can note it in `profile/` for next time.
- "Never offer to close my code editor, even if I say clean it up" - keeps editors in bucket (b) permanently; save the preference in `profile/` or the skill file.
- "Skip the prevention tip; just give me the numbers" - shortens the closing; edit `skills/computer-revive/SKILL.md` Step 5.

Say 'show me the skill file' and it opens `skills/computer-revive/SKILL.md`. Change the words, save, and the next run uses them.

## How it works, in four lines

It reads live process and memory numbers from your OS. It classifies each named process into safe, ask-first, or never-touch. It closes only what you approved, then re-measures. It never disables startup items, never changes system settings, and never invents a number it did not just pull.

## Related

Standalone. When the machine is clear, pick up the work you were about to do (a scan, a flyer, a market brief).

Still stuck? Text Joshua.
