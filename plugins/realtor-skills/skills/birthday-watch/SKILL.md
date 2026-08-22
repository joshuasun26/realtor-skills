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
