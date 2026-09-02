# Your own AI texts your phone, and later you text it back

### 20 minutes for the brief, another 15 for the loop. A Mac that is yours, or on Windows the Telegram app on your phone. Python on the laptop (`check my setup` tells you).

## What this does for you

Right now your AI only works when you are sitting at the laptop. After this, it texts you
every morning: who is waiting on a reply from you, what on today's calendar needs prep,
and the one thing that matters most. Later, you text the same thread back from the car,
"draft a reply to the buyer from Saturday," and the answer comes back as a text.

What comes back: a brief on your phone on a schedule, in the app you already check. On a
Mac that is your own Messages thread with yourself. On Windows it is a Telegram bot that
only talks to you. No new phone number, no monthly fee, no registration wait.

The one rule it will not break: the only phone this can ever text is yours. Nothing it
does reaches a client, a lead, or your sphere. When you want it to send something to
another person, you say go for that message, in that exchange, every time.

## The one command
```
set up voice command
```
Open Claude Code **in your business folder** (the one with `profile/` in it). Type the
line. Answer by voice if that is easier.
**First time?** It will ask for two things.
1. Mac or Windows, and whether the laptop is yours or your office manages it.
2. On a Mac: two permission switches in System Settings, which it names one at a time.
   On Windows: a bot you create in Telegram on your phone (search BotFather, send
   `/newbot`, follow three prompts) and the code it gives you, pasted into a file called
   `.env`. Never into an email or a group chat.

## What you get back
```
Example shape, not a real run

[claude] Tue 9/10

Waiting on you
1. Maria L, asked about the inspection credit, 2 days
2. The Nguyens, want the Saturday showing time, since yesterday

Today
3:00 listing appointment, 41 Oak. Brief is in the folder.

The one thing
Call Maria before noon. The credit question is holding the deal.
```
Yours is built from your data, not this example. The setup lands in `profile/STACK.md`
under a Voice wire heading; the scripts live in `voice/`; your token, if any, lives only
in `.env`.

## Three things that break, and the fix
1. **No brief this morning** - the laptop was asleep or the lid was closed. Scheduled
   runs need an awake machine. Fix: open it, plug it in, and turn off sleep while on
   power. Nothing was lost; the next run catches up. Run the task by hand once to prove
   the task itself is fine.
2. **On a Mac, it texted itself over and over** - the `[claude]` tag at the front of its
   replies was edited out, or the history got replayed as commands. Fix: say "reset the
   command loop" (it runs `python voice/imessage_poll_commands.py --reset`) and check
   that every reply still starts with `[claude]`. Then the loop-guard check again before
   it is scheduled.
3. **On Windows, "Missing TELEGRAM_BOT_TOKEN"** - the `.env` file moved, or the token
   was never pasted in. Fix: open `.env` in your business folder, confirm the two lines
   are there, and say "send me a test message." It prints `sent` only when Telegram
   accepted it; then check your phone.
If it is none of these: screenshot it and paste it to Claude. That is the fastest way
through.

## Make it yours
- "Brief me at 6:30, not 7" - changes the schedule; saved in the task and in
  `profile/STACK.md`.
- "Only text me weekdays 8 to 6" - the working hours the loop polls inside; saved in
  `profile/STACK.md`.
- "Add my calendar to the brief" or "leave email out of it" - changes what the brief
  reads; saved in the skill file.
Say "show me the skill file" and it opens `skills/voice-command/SKILL.md`. Change the
words, save, and the next run uses them.

## How it works, in four lines
It reads your calendar and email if they are connected, your contacts file, and on a Mac
the threads where the last message is not yours. It decides who is waiting, what needs
prep, and the one thing, and sends nothing at all when nothing needs you. It writes the
brief to your own thread through a script that has exactly one recipient. It never
replies to anyone but you and never sends to another person without your go in that
exchange.

## Related
Reads the morning list from **Who do I contact today** (`good morning`) when it has run.
Level 3 hands any client text to **Set up my GoHighLevel** (`set up my GoHighLevel`)
Level 3, which is where sending to other people lives. **Find out what your laptop can
run** (`check my setup`) goes first if Python is missing.

Still stuck? Text Joshua at 858-585-4853.
