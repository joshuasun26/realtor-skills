---
department: sphere
name: birthday-watch
description: >
  Check the contact database for birthdays landing today and in the next seven days, and
  draft a genuine personal message for each one in the agent's voice. Trigger on "whose
  birthday is it", "birthdays this week", "birthday check", "run birthdays", or as part of
  sphere-daily. Do NOT trigger for home purchase anniversaries — that is home-anniversary.
---

# Birthday Watch — the touch nobody resents

A birthday message is the only unsolicited contact from a real estate agent that is
universally welcome. It costs nothing, it is not a pitch, and it produces more return
conversations than any campaign an agent will ever pay for.

It also fails badly when it is obviously automated. This skill exists to keep it real.

Reads `data/contacts.csv`, `profile/VOICE.md`, `profile/AGENT.md`.

---

## The check

Match on `birthday`. Only two formats are valid: `MM-DD` or `YYYY-MM-DD`. If a row's
`birthday` value is blank, or is in any other format (e.g. `March 3`, `3/3`, `03/03/1990`),
do not guess — skip that row for today's list, add it to a "needs fixing" count reported
to the agent, and do not include it in the next-7-days list either until the format is
corrected. Return:

- **Today**, drafted and ready
- **The next 7 days**, so the agent can plan a call or a card

Exclude anything tagged `optout` (any value: `all`, `text`, `email`, or `call` — if the
tagged channel is the one this skill would use, i.e. text or call, exclude; if the
contact opted out of a different channel only, proceed on this channel). Include tier D
contacts here only if `profile/AGENT.md` or the contact's own notes field names the agent
as knowing them personally (a job, a mutual friend, a specific shared memory) — a bare
imported row with no such detail does not qualify, however long it has been in the
database. A birthday text to a scraped contact is worse than no message.

## Draft each one individually

**Never a template with a merge field.** People can tell instantly, and a generic
"Happy Birthday [FirstName]!" from their real estate agent reads as a CRM, which is the
opposite of what this touch is for.

For each person, pull whatever context the file holds — how the agent knows them, when
they closed, what is in their notes — and write **one message that could only have been
sent to that person.** If the file holds nothing useful, write something short and warm
rather than something long and generic. Short and real beats long and hollow.

**Length:** one to three sentences. This is a birthday text, not a newsletter.

**Voice:** run `agent-voice`. Match their real greeting habit, their real emoji level,
their real spacing. Scan for banned words before delivering.

## The hard rule

**No business in a birthday message.** No market update, no "let me know if you're
thinking of selling", no link, no listing, no call to action of any kind.

The moment a birthday text carries a pitch, it stops being a gift and becomes an ad, and
the recipient files every future message from that agent the same way. The business return
on birthdays comes precisely from the fact that there is no ask in them.

If the agent asks to add a line about the market, say this plainly once, then do what they
decide.

## Escalate the important ones

For tier A contacts and anyone with a real relationship, propose **a call instead of a
text**, and for the top handful, a card in the mail. A voice message on someone's birthday
outperforms a text by a wide margin and takes forty seconds.

Rank the day's list so the agent knows which one or two are worth the call.

## Approval and sending

Present the batch as a numbered list with each recipient and the full message copy, in a
file the agent can edit. Then wait for their go.

Nothing sends without an explicit approval in this session for this specific batch.
Approval today is not approval tomorrow.

After sending, report what went and what did not, by count and by name. Update
`last_touch` in `data/contacts.csv` and log to `records/sent-log.md`.

## Filling the gap

Most databases have birthdays on well under a quarter of contacts, which is the single
biggest limiter on this skill. Tell the agent the count, then give them one practical way
to collect more — asking at closing, adding the field to the open house sign-in, or
capturing them from conversations as they happen. One method, not five.

## Wider birthday sources

`data/contacts.csv` is the read for the daily scan, but it is rarely the only place an
agent's birthdays live. When the agent wants to grow the file rather than wait on
one-at-a-time capture, offer these, one at a time, not all five in a wall of text:

1. **Phone contacts (.vcf).** If they export their phone contacts as a vCard, that is a
   `contact-import` job, not this skill's — send them there. `contact-import` already
   normalizes vCard `BDAY` fields into the `MM-DD` / `YYYY-MM-DD` schema this skill reads.
   Once re-imported, re-run this skill and the new birthdays are live.
2. **CRM birthday field, via export refresh.** Most CRMs (Lofty, Follow Up Boss, KW
   Command, etc.) have a birthday field that never gets surfaced anywhere. Ask the agent
   to pull a fresh CRM export and hand it to `contact-import` the same way. This is a
   refresh, not a first import — `contact-import`'s dedupe-on-conflict rule already keeps
   the more recently touched record, so re-running it is safe.
3. **Facebook birthdays.** If the agent has a logged-in browser session available to
   Claude, browse to `facebook.com/events/birthdays` and read the day's and week's names
   directly off the page. Match each name against `data/contacts.csv` by first+last name
   (fall back to a fuzzy match and confirm with the agent on anything uncertain — never
   silently guess an identity match). If no logged-in session is available, tell the agent
   plainly: "I can't reach Facebook from here — open facebook.com/events/birthdays
   yourself and paste me the names for today and this week."
4. **WhatsApp, WeChat, or anything else.** Same paste-in path as Facebook: the agent opens
   whatever app holds the birthday and pastes the names (and dates, if visible) into the
   chat. Claude never needs API access to these — a pasted list is enough to work with.

**Write discovered birthdays back into `data/contacts.csv`.** Whether a birthday came from
a vCard re-import, a CRM refresh, a Facebook scan, or a pasted list, the point is that the
file gets richer over time instead of this being a one-off lookup. Match the new birthday
to an existing `contact_id` where one exists (same dedupe logic as `contact-import`: phone,
then email, then exact first+last+city); if the person is not yet in the file at all, ask
the agent whether to add them as a new row rather than silently creating one. Report what
was added: "found 4 new birthdays from Facebook, wrote them into contacts.csv."

## Notification levels — how the daily result reaches the agent

The scan itself does not change across levels — same file, same read, same drafting rules
above. **Levels only change how today's brief gets in front of the agent**, and whether it
goes further than that. Ask the agent once, at setup, which level they want, and record the
choice in `profile/AGENT.md` so future runs do not have to ask again.

### Level 1 — Notify (everyone, day one)

The run writes the daily birthday brief — who, the relationship, their number, the drafted
message for each — same format as the existing approval-batch file. Delivery:

- If the agent has a mail connector connected in their Claude Code, draft and send an
  email **to the agent's own address** with the brief. This is Claude emailing the agent,
  not the agent's contacts — it needs no approval gate, since nothing is going to a third
  party.
- If no mail connector is connected, leave the brief file open and tell the agent plainly
  where it is and that it's ready for review.

This works on iPhone and Android and needs no phone number, no CRM, and no API key. It is
where every agent starts.

### Level 2 — Text me the list (needs a CRM number, e.g. Lofty)

For agents on a CRM with its own SMS-sending number, the skill can text the daily brief
**to the agent** from that number instead of (or alongside) the email.

**Lofty reference** (the CRM most of this library's agents use):

- API key: agent generates one in Lofty under **Settings > Integrations > API**. Docs at
  `developer.lofty.com`.
- Send endpoint: `POST /v1.0/message/sms/send`. This endpoint sends to a *lead*, not to an
  arbitrary phone number — so the one-time setup is: the agent adds **themselves** as a
  lead in Lofty with their own cell number.
- Store that lead's id as `leadId` in `profile/AGENT.md` under a `Birthday Watch` section,
  once, at setup. Every daily run reads it from there rather than asking again.
- If the API key or `leadId` is missing when this level is requested, stop and get them
  before the first send — do not guess or fall back to a channel the agent didn't ask for.

**Other CRMs.** If the agent's CRM has its own SMS-send API, the same pattern applies:
find the CRM's own docs (ask Claude to check them), find the equivalent of "add myself as
a recipient" and "send" endpoints, and store whatever id that CRM needs in
`profile/AGENT.md` the same way. Do not assume Lofty's exact shape carries over — verify
against that CRM's own documentation before wiring anything.

### Level 3 — Full loop (advanced)

**This is real plumbing. Expect to iterate on it before it feels smooth.** It is exactly
what Joshua sets up for clients in his 1:1 installs, and it is the right level for an agent
who wants to reply to the Level 2 text with a dictated birthday message and have it go out
without opening a laptop.

The loop:

1. The agent replies to the Level 2 text with a birthday message, dictated or typed.
2. A watcher — a scheduled Claude run polling
   `GET /v2.0/leads/{leadId}/activities` for inbound texts, or a webhook registered via
   `POST /v1.0/webhook` with event type `Text` — picks up that reply.
3. The watcher **always echoes back what it is about to send and to whom** before sending
   anything to the actual contact, and only fires on an explicit "send" (or equivalent
   clear go) in the agent's reply. A dictated draft that doesn't say "send" is held, not
   sent.
4. Once confirmed, the watcher sends the birthday text to the actual contact using the
   same `POST /v1.0/message/sms/send` endpoint, this time targeting the contact's own
   `leadId` (or the CRM equivalent), not the agent's.

**Known Lofty caveats to plan around:**
- Webhooks do not fire for `AUTO` communications — only for genuine inbound activity.
- The webhook callback URL must be HTTPS.

Mark this level plainly to the agent as advanced: it involves a second moving part (the
watcher) that has to stay scheduled and healthy, and it is worth setting up once it's clear
Level 1 or 2 is actually being used.

### The hard rail — unchanged at every level

**Messages to CONTACTS only go out after the agent's explicit go for that specific
message**, exactly as in the base skill above — this does not change no matter which
notification level is running. Level 1 and Level 2 deliveries are notifications *to the
agent themselves* about their own day; those are not gated, because nothing is reaching a
third party. The gate is on the outbound birthday message to the contact, always.

## Cadence

Run this daily, in the morning, before the agent's day starts — birthdays are the one item
on `sphere-daily` that is time-bound (today or nothing), so a scan that runs at noon has
already missed half its value.

To have Claude run it automatically, ask: "schedule my birthday check every morning at
[time]." That is a `schedule` skill job, not something this skill sets up itself.

## Chains from / into

Called by `sphere-daily`. Reads `contact-import` output and `agent-voice`. Sits alongside
`home-anniversary`.

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
