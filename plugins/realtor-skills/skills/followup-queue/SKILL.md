---
department: pipeline
name: followup-queue
description: >
  Work out who is due for a follow-up touch today across every active sequence and every
  open pipeline item, draft each message personalized against that contact's real record,
  and hold the batch for approval. Trigger on "who's due today", "run my follow-ups",
  "follow-up queue", "what did I forget", "who's falling through the cracks", or as part
  of sphere-daily. Do NOT trigger to design a cadence — that is followup-sequence.
---

# Follow-Up Queue — the thing that catches what falls through

Reads `data/pipeline.csv`, `sequences/*.md`, `data/contacts.csv`,
`records/sent-log.md`, `profile/VOICE.md`.

---

## Step zero — run revocation-watch first

Before building anything, run the `revocation-watch` scan over inbound replies since
the last batch. A queue drafted before the opt-out scan is drafted against a stale
list. Anyone it tags is out of today's queue and every future one.

## Build the queue

For every row in `data/pipeline.csv`:

1. Is `next_action_date` today or earlier? `next_action_date` must be `YYYY-MM-DD`. If a
   row's value is blank or in any other format, do not guess — skip that row, add it to a
   "needs fixing" count reported to the agent, and do not include it in today's queue
   until the format is corrected. Otherwise: if the date is earlier than today, it is
   **overdue** — flag it as such and put it above everything on time. Overdue items are
   where deals die.
2. Is there an active sequence on this contact, and which touch number is next?
3. **Has the contact replied since the last touch?** If yes, the sequence stops and this
   becomes a human conversation, not a queued touch. Say so and move it to the top.
4. Is the contact tagged `optout: all`? Remove them entirely, permanently. If tagged
   `optout: text` or `optout: call` and this touch would use that exact channel, remove
   it for that channel only — re-route the touch to a channel the contact has not
   revoked, or exclude if no channel remains.
5. Is the consent tier below what the sequence requires? Exclude and report the count.

## Rank and cap

**Cap the daily queue at 10 items.** More than that and the agent stops reading it, which
means the whole system produces nothing.

Rank:

1. **Replies waiting on the agent.** Someone who answered and is being ignored is the most
   expensive item in the queue.
2. Overdue, by how overdue
3. Active clients mid-transaction
4. This-month leads
5. Everything else

**Tie within a tier:** break ties by how overdue the item is (most overdue first); if
`next_action_date` is identical, break by longest time since `last_touch` in
`data/contacts.csv`; if that is also blank or tied, break alphabetically by last name,
then first name. Apply the same tiebreak when deciding which 3 items get the call flag.

Report how many were held back. "9 today, 22 held" keeps the cap trustworthy.

## Draft each one against the real record

**Do not send the sequence file's copy verbatim.** That copy is a starting point. For each
contact, personalize it against what the record actually holds: what they said they
wanted, what the agent last sent them, how long it has been, what has changed in their
area since.

Call `sphere-message` for the drafting. Run `agent-voice`. Scan for banned words.

If a touch is supposed to carry a listing match or a market number, go get it — from the
MLS via `market-pull`, sourced and dated. If it cannot be sourced this session, change the
touch rather than shipping an unsourced number.

## Calls

Some touches should be calls, and the sequence says which. **Do not silently convert a
call into a text because a text is easier to draft.** Produce a talk track for the call
instead — the opening line, the one question, and the goal — and flag it clearly.

Cap calls at 3 a day. Agents will do three; they will not do eleven.

## Approval

One file, `daily/followups-<YYYY-MM-DD>.md`, numbered, with recipient, channel, why, and
the full copy for each.

**Nothing sends without an explicit go for this specific batch in this session.** Approval
does not carry to the next batch. "Looks good" is not approval — ask once and wait.

After sending, report what went and what did not, by count and by name.

## After the send

- Update `next_action` and `next_action_date` in `data/pipeline.csv` — every touched item
  exits with a new dated next action, or with the sequence marked complete
- Update `last_touch` in `data/contacts.csv`
- Append to `records/sent-log.md`
- Anything the agent rewrote goes into `profile/VOICE.md` under Corrections

## The honest monthly reading

Once a month report: items queued, items approved, items sent, replies received, and how
many pipeline rows are sitting with an overdue `next_action_date` nobody has touched. If
the queue is being generated and ignored, say so plainly rather than continuing to produce
lists nobody reads.

## Chains from / into

Called by `sphere-daily`. Reads `followup-sequence` and `lead-intake` output. Uses
`sphere-message`, `agent-voice`, `market-pull`, `source-check`.

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
