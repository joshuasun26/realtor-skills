---
department: pipeline
name: social-scan
description: >
  Review the agent's recent Instagram activity — new followers, story viewers, post
  likers and commenters — classify each new person, check whether they are an
  existing sphere contact re-engaging, and draft a first DM for the ones worth
  reaching, capped at 5 per run. Trigger on "check my Instagram", "run my IG scan",
  "who engaged with my posts", "any new followers worth a DM", "social scan", or as a
  daily/scheduled routine. Do NOT trigger to write or schedule content — that is
  content-week and social-caption.
---

# Social Scan — turn Instagram activity into five ready-to-send DMs

Every agent's warmest leads are already tapping on their Instagram — a like on a listing
post, a view on a story about a new baby, a comment from someone whose name shows up in
`data/contacts.csv` from three years ago. Almost none of it gets a reply, because reading
the activity and writing a real first message takes longer than an agent will do between
showings.

This skill does the reading and the drafting. It never does the sending.

Reads `profile/AGENT.md`, `profile/VOICE.md`, `data/contacts.csv` (optional but
recommended — the skill still runs without it, just without the sphere cross-check).

---

## Step 1 — Get the activity

**This skill does not use the Instagram API and never will.** IG's API does not expose
story viewers or a clean likers/commenters feed to a normal account, and building around
scraping workarounds is exactly the kind of thing that gets an account flagged. Instead,
get the activity one of two ways — both are first-class, use whichever the agent has:

- **Browse it live.** If Claude Code's browser tools are available and the agent is
  logged into instagram.com in that browser session, open the activity feed, the story
  viewer lists on the last 24 hours of stories, and the likes/comments on the last few
  posts. Read what is on screen. Do not attempt to log in on the agent's behalf, do not
  touch saved passwords, and stop and ask if a login screen appears instead of the feed
  the agent expected.
- **Take what the agent hands over.** A screenshot of the activity tab, a screenshot of
  a story's viewer list, or a pasted list of names/handles. This is the fallback for any
  agent without the browser tools connected, and it is just as valid an input — treat it
  the same as a live browse.

Either way, pull three lists: **new followers since the last run**, **story viewers**
(only from stories still in the last 24 hours), and **likers/commenters** on posts from
the last 3 to 4 days. Note the date/time of the scan.

**Never attempt to view a private account's content the agent does not already follow
back or have visibility into.** If a profile is private and nothing beyond the handle and
name is visible, classify it as unknown and say so — do not try to work around the
privacy setting.

## Step 2 — Classify each new person

For everyone who is new since the last run (a new follower, a first-time story viewer, a
first-time engager), open their profile and read the bio, recent posts, and who they
follow. Classify into exactly one of:

- **(a) Fellow realtor / vendor** — bio says agent, broker, lender, title, photographer,
  stager, or the account is clearly a real estate business account. Worth a professional
  hello, not a client pitch.
- **(b) Potential buyer signal** — engaging specifically with listing posts, open house
  posts, or content about buying; or a bio/recent-post life signal that points toward a
  move (new job in the area, engagement, growing family, "just relocated").
- **(c) Potential seller signal** — bio or posts suggest they already own where the agent
  farms (local tags, a home-related post, a "we've outgrown this place" kind of caption),
  or they specifically engaged with market-value or "what's my home worth" content.
- **(d) Unknown / personal** — no signal either way, or clearly a personal friend/family
  account with no business angle. These get noted, not drafted.

Classify on what is actually visible. Do not guess at someone's finances, ethnicity, or
family status to sharpen a classification — if the signal is not there, it is unknown.

## Step 3 — Check the sphere first

Before doing anything else with a name, check it against `data/contacts.csv` (if it
exists). **A contact re-engaging after going quiet is the hottest signal this skill can
surface** — someone the agent already has a real relationship with just showed up again
on their own. Flag any match at the top of the report, above new-to-the-agent people,
regardless of what page of the funnel they otherwise classify into.

If the matched contact is tagged `optout` in any form, this skill does not draft anything
for them, on any channel, full stop — see Hard rails.

## Step 4 — Draft, at most 5

Rank everyone worth a message — sphere re-engagement first, then buyer/seller signals,
then realtor/vendor hellos — and draft no more than **5** DMs this run, even if more
people qualify. Say how many qualified and how many got held back, the same honesty
sphere-daily uses for its cap.

Every draft runs through `agent-voice` against `profile/VOICE.md` before it's shown.

**Rules for every draft:**

- **Reference the specific thing they did.** "Saw you liked the Wasatch listing" or "you
  watched my story about the open house Saturday" — never a generic "hey, thanks for the
  follow!" A message that could have been sent to anyone reads like a bot and gets
  ignored like one.
- **No pitch in the first message.** No "let me know if you're thinking of buying or
  selling," no link, no CTA. The first DM's only job is to sound like a person who
  noticed them, not a funnel that found them.
- **Match the touch to the engagement.** Instagram's own norms apply here: someone who
  only viewed a story gets a lighter, easier-to-ignore opener than someone who left a
  comment, because a comment is a bigger social move than a silent view and deserves a
  reply that acknowledges that. Do not open a story-viewer conversation as if they
  raised their hand — they didn't, yet.
- **Realtor/vendor hellos** stay peer-to-peer — no pitch at all, just a genuine
  professional hello, since these are future referral relationships, not leads.
- **Sound like a person.** Short. Real. One or two sentences unless the context genuinely
  calls for more.

## Step 5 — The report

Write one file, `scans/<YYYY-MM-DD-HHmm>.md`, not a wall of chat text. For each drafted
person:

```
### N. [Name / handle] — [classification]
Engagement: [what they did, and when]
Sphere match: [yes — contact_id, last_touch / no]
Why they matter: [one line]

[the full drafted DM]
```

Above the list: the scan window covered, total new activity seen, how many classified
into each bucket, how many qualified for a draft, how many were held back by the cap.

**The agent copies and pastes these themselves.** Nothing in this file is sent by this
skill — see Hard rails.

## Cadence

**Default: once a day, in the evening**, after the day's posting and engagement has had
time to land. A daily rhythm matters for a real reason, not just consistency: Instagram
gives a new DM roughly a 24-hour window before its own reply-rate signals start working
against the conversation, so a scan that runs every day catches people while that window
is still open. A scan that runs every third day is catching people after the moment has
mostly passed.

The agent can ask Claude to set this up as a recurring scheduled task rather than
remembering to ask for it — say so if they run it manually more than a couple of times.

**During a busy stretch — a just-listed property, an active giveaway, a post that took
off — tell the agent to ask for it more than once a day.** If people are replying to the
drafted DMs once sent, the reply traffic itself becomes worth checking on an
office-hours cadence rather than waiting for the evening run, since a reply sitting
unanswered for a day undoes the goodwill the first message built.

## Hard rails

- **Nothing sends. Ever, automatically.** This skill drafts. The agent copies each
  message into Instagram and sends it themselves, or explicitly directs another approved
  channel to send it. No send tool, no auto-DM, no "go ahead and send these" default —
  if the agent says go, that is still them doing the sending, this skill has no send
  capability to invoke.
- **No scraping, and no working around a private account.** Only read what is actually
  visible in the browser or in what the agent handed over.
- **Never draft to anyone tagged `optout`.** That tag is permanent, on every channel,
  including Instagram DMs, per `contact-import` and `revocation-watch`. Check the sphere
  match before drafting, not after.
- **Max 5 outreach drafts per run.** This is what keeps the whole thing feeling like a
  person reaching out instead of a bot working a list. If the agent wants more some day,
  say plainly that raising the cap changes what this looks like on the receiving end,
  then do what they decide.

## Chains from / into

Can run standalone or as part of a daily routine alongside `sphere-daily`. Reads
`contact-import` output and `agent-voice`. A sphere match with real buying/selling intent
hands off to `lead-intake`. A drafted DM that turns into a real conversation continues in
`sphere-message`.

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
