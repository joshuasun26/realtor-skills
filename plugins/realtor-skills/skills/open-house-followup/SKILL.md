---
department: open-house
name: open-house-followup
description: >
  Turn an open house sign-in list into individually drafted follow-up messages, segmented
  by what each visitor said they were, on a timed cadence — and hold every message for the
  agent's approval before anything sends. Trigger on "follow up on the open house", "who
  came Sunday", "draft the open house follow-ups", "what do I send the people who came",
  or as the final step of open-house-package. Do NOT trigger for general sphere touches —
  that is followup-queue.
---

# Open House Follow-Up — the 48 hours that decide whether the open house was worth it

Most agents hold the open house and then send nothing, or send one identical blast. The
follow-up is where the open house actually pays.

Reads `data/open-house-<slug>-<date>.csv`, `listings/<slug>/LISTING.md`,
`profile/AGENT.md`, and `profile/VOICE.md`.

---

## Segment first

Split the sign-in list by what each visitor told you:

| They said | What they are | Cadence |
|---|---|---|
| Actively looking | The reason to hold open houses | Same day, then day 3, then weekly |
| Just looking | Long horizon, real | Same day, then day 7, then monthly |
| Working with an agent | Do not poach | ONE courteous message, then stop |
| Neighbor | Future seller, best source | Same day, then at the sale |

**The "working with an agent" rule is a hard line.** Send one message thanking them for
coming and nothing else. Do not add them to a nurture sequence. Soliciting a client under
an exclusive representation agreement is an ethics complaint, and in most markets the
other agent will find out.

## Consent filter (runs before anything is drafted)

Drop every row whose `consent_tier` is `unknown` from all automated and bulk messaging.
They can be called or written to one at a time by the agent personally, and that is the
agent's judgment call — but this library will not queue them.

Drop every row tagged `optout`, permanently, across all channels.

Say the counts out loud: "42 signed in, 31 consented, 4 already working with an agent,
7 excluded for no consent."

## Draft each message individually

Not a template with a merge field. The whole advantage here is that each visitor had a
different conversation.

Every message should carry **one specific thing** — what they said about the kitchen,
that they mentioned a commute, that they asked about the schools district assignment,
that they were the neighbor two doors down. Ask the agent for their notes from the day. If
they have none, ask for the three visitors they remember and draft those individually,
and keep the rest short and honest rather than fake-personal.

**Message 1 (same day, evening):** thank them, one specific reference, one useful thing
(the listing link, the flyer PDF, the answer to a question they asked), one low-pressure
open. Short. Two or three sentences.

**Message 2 (day 3):** the actual value. What sold, what came on, what the property did.
This is where `market-brief` output gets attached — MLS-sourced, dated.

**Message 3 (day 7+):** the ask, once. A call, a showing, a buyer consultation. Then move
them to the long cadence in `followup-sequence`.

**Voice:** run `agent-voice` on every draft. Scan for the banned words before delivering.

## The approval gate — this is not optional

**Nothing sends automatically. Ever.**

Present the batch as a numbered list: recipient, channel, and the full message copy for
each one, in a file the agent can read and edit, not buried in chat scrollback. Then
wait.

- The agent approves the batch, or specific numbers, in this session.
- Approval on one batch is never approval on the next batch, the next wave, or tomorrow.
  New batch, new ask.
- "Looks good", silence, or ambiguity is not approval. If you are not certain, ask in one
  line and wait.
- After sending, say plainly what went and what did not. Count them. Name anything that
  failed. Never report a send as complete when a call errored.

## Log it

Write every sent message to `records/sent-log.md` with date, recipient, channel, and the
copy. Update `last_touch` in `data/contacts.csv`. Merge new consented visitors into the
contacts file via `contact-import` so they flow into the sphere skills from then on.

## Chains from / into

Called by `open-house-package`. Reads `open-house-signin` output. Uses `agent-voice`.
Hands long-term contacts to `followup-sequence` and `sphere-daily`.

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
