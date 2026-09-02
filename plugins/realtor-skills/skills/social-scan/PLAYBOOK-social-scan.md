# Turn today's Instagram activity into five ready DMs

### 10 minutes. Instagram logged in for Claude's browser, or screenshots of activity / viewers / likers.

## What this does for you

Your warmest leads are already tapping your posts and stories. Almost none of them get a reply, because reading the activity and writing a real first message takes longer than you have between showings.

This skill reads new followers, story viewers, and recent likers or commenters, classifies each person, checks your sphere file when you have one, and drafts at most five first DMs in your voice.

It drafts only. It never sends. You copy and paste into Instagram yourself.

## The one command

```
check my Instagram
```

Open Claude Code **in your business folder** (the one with `profile/` in it). Type the line. Answer by voice if that is easier.

**First time?** It needs activity one of two ways:

1. A browser session already logged into instagram.com so Claude can open the activity feed, story viewers (last 24 hours), and likes/comments on recent posts.
2. Or screenshots / a pasted list of names and handles from those same screens.

Optional but useful: `data/contacts.csv` so it can flag sphere people re-engaging.

## What you get back

`Example shape, not a real run`

```
Scan window: <dates>
New activity seen: N
Buckets: realtor/vendor / buyer / seller / unknown
Qualified for draft: N | Held by 5-cap: N

### 1. [@handle] - [classification]
Engagement: [what they did, when]
Sphere match: yes - contact_id / no
Why they matter: [one line]

[drafted DM, specific to what they did, no pitch]
```

Yours is built from your data, not this example. The file lands at `scans/<YYYY-MM-DD-HHmm>.md`. Nothing in that file is sent by this skill.

## Three things that break, and the fix

1. **A login screen appears instead of your feed** - Claude will not log in for you. (*"Do not attempt to log in on the agent's behalf, do not touch saved passwords, and stop and ask if a login screen appears instead of the feed the agent expected."*) Fix: log into Instagram in that browser yourself, or drop screenshots of activity / viewers / likers.

2. **It tried to dig into a private profile it should not see** - private accounts stay opaque. (*"Never attempt to view a private account's content the agent does not already follow back or have visibility into."*) Fix: say "classify unknowns as unknown; do not work around privacy" and re-run on what is visible.

3. **You asked it to send the DMs and nothing went out** - that is by design. (*"Nothing sends. Ever, automatically. This skill drafts."*) Fix: copy each draft into Instagram yourself, or explicitly send on another approved channel; this skill has no send capability.

If it is none of these: screenshot it and paste it to Claude. That is the fastest way through.

## Make it yours

- "Raise the draft cap to 8 today" - changes the 5-cap for that run only after Claude warns what it looks like on the receiving end; lasting change goes in `skills/social-scan/SKILL.md`.
- "Always put sphere re-engagements first" - already the rank order; reinforce in `profile/` if a run drifts.
- "Skip drafting for fellow realtors; list them only" - narrows Step 4; edit the skill file classification rules.

Say 'show me the skill file' and it opens `skills/social-scan/SKILL.md`. Change the words, save, and the next run uses them.

## How it works, in four lines

It reads activity from a logged-in browse or from what you hand over (never the Instagram API, never scraping workarounds). It classifies each new person from what is actually visible on their profile. It cross-checks `data/contacts.csv` when present, skips anyone tagged opt-out, and drafts at most five DMs through your voice file. It writes a scan report and never sends a message.

## Related

Runs well next to your daily sphere check (`sphere-daily`). A sphere match with real buying or selling intent can hand off to lead intake. A drafted DM that turns into a conversation continues in sphere messaging.

Still stuck? Text Joshua.
