---
department: pipeline
name: followup-sequence
description: >
  Design a multi-touch follow-up cadence for one lead type or one situation — how many
  touches, on what days, on which channel, and what each one actually says — and write it
  as a reusable sequence file the daily queue reads. Trigger on "build a follow-up
  sequence", "what's my cadence for [lead type]", "nurture sequence", "drip campaign",
  "how often should I follow up", or as a step after lead-intake. Do NOT trigger to send
  today's touches — that is followup-queue.
---

# Follow-Up Sequence — the cadence, designed once

A sequence is a plan, not a send. This skill writes the plan; `followup-queue` runs it a
day at a time with the agent approving each message.

Writes `sequences/<sequence-name>.md`. Reads `profile/AGENT.md`, `profile/VOICE.md`.

---

## Design principles

**Front-load heavily.** Most of the value of a follow-up sequence is in the first 72
hours. A lead who called on Tuesday and hears back on Friday is usually gone. Touch 1 is
same day, touch 2 is next day, touch 3 is day 3.

**Then decay.** Days 1, 2, 3, 7, 14, 30, then monthly. Not because thirty touches are
better than eight, but because the long tail is where most agents quit and where the
transaction eventually happens.

**Every touch carries something.** A touch that only says "just checking in" trains the
recipient to ignore the agent. Each one should deliver a listing that matches what they
said they wanted, an MLS-sourced number about their area, an answer to a question they
asked, or a genuinely useful piece of process explanation.

**Vary the channel.** Text, call, email, video, mail. Five texts in a row reads as a
robot; the same five touches across three channels reads as a person who is paying
attention.

**Name the exit.** Every sequence needs a stop condition: they respond, they book, they
say no, they opt out, or the sequence completes. A lead who replied and is still receiving
sequence touches is the single most damaging failure mode here. Write the exit into the
file.

## Standard sequences worth having

Build the one the agent needs now, not all of them.

| Sequence | Shape |
|---|---|
| **New buyer lead** | Day 0 call + text, day 1 text, day 3 email with matches, day 7 call, day 14 value, then monthly |
| **New seller lead** | Day 0 call, day 1 email with the area's MLS numbers, day 3 call, day 7 offer a walkthrough, then bi-weekly |
| **Open house visitor** | Handled by `open-house-followup` — do not duplicate it here |
| **Past client** | Quarterly, plus birthday and home anniversary, driven by `sphere-daily` |
| **Referral received** | Day 0 call same day without exception, day 1 thank the referrer separately, then the matching lead sequence |
| **Went quiet** | One honest message naming the silence, then stop. Not a new sequence. |

## The file format

```
# Sequence: <name>
Applies to: <lead type / entry condition>
Exit on: <every stop condition>
Consent required: <minimum consent tier for this sequence>

## Touch 1 — Day 0 — call
Goal: ...
If no answer: ...
Copy / talk track: ...

## Touch 2 — Day 1 — text
...
```

Copy in the file is a **starting point, not the send.** `followup-queue` personalizes each
one against that contact's actual record before it is drafted for approval. A sequence
that sends its file copy verbatim is a mass mailer.

## Hard rules

- **Consent tier gates the sequence.** Anything requiring `unknown`-tier contacts is not
  built. Say so.
- **An opt-out stops every sequence for that contact, permanently, on every channel.**
  No skill in this library may remove an opt-out tag.
- **Reply stops the sequence immediately.** Build the check into touch generation, not
  just into the file.
- Bulk and automated texting carries its own legal requirements that vary by state and
  change over time. Tell the agent this needs their broker's confirmation; do not state a
  specific rule as settled law here.
- Every market number in any touch routes through `market-pull` and `source-check`.

## Realism check

Before writing the file, ask how many new leads the agent actually gets in a month. A
twelve-touch sequence across forty leads is 480 messages and it will not happen. Design
for what they will really do, then say what you designed for.

## Chains from / into

Called after `lead-intake`. Read by `followup-queue`. Uses `agent-voice`.

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
