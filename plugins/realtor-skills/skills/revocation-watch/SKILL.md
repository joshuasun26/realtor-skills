---
department: foundation
name: revocation-watch
description: >
  Catch every opt-out, however it's phrased, and make it stick. Run on every batch of
  inbound replies before drafting any follow-up, and any time the agent asks "did anyone
  opt out", "check for stops", "clean my list", or "can I still text this person". Also
  runs automatically as the first step of followup-queue and sphere-daily. This is a
  compliance gate: its NO overrides every other skill's draft.
---

# Revocation Watch — the opt-out catcher

Consumers may revoke consent by **any reasonable method** (47 CFR 64.1200(a)(10)) —
not just by replying STOP. "Please don't text me," "take me off your list," "not
interested, stop reaching out," "who is this? don't contact me," a voicemail saying to
quit calling, or telling the agent face to face at an open house ALL count. A system
that only catches the literal word STOP is a system that keeps texting people who
revoked, and every message after a revocation is a separate violation that lands on
the agent's license and wallet.

## What a revocation looks like (classify by meaning, not keywords)

Read each inbound reply and judge intent:

- **Clear revocation** — any expression of "stop contacting me," whatever the words:
  STOP, unsubscribe, remove me, don't text me, wrong number + go away, "no more,"
  profanity + leave-me-alone, "I already have a lender/agent, please stop."
- **Channel-specific revocation** — "stop texting me, email is fine" revokes ONE
  channel. Honor the named channel; keep only what they said stays open, and record
  which is which.
- **Scope-specific** — "I'm not interested in this house" is not a revocation of all
  contact. When genuinely ambiguous, treat as full revocation OR ask exactly once for
  clarification with zero marketing content. When in doubt, out.
- **NOT a revocation** — a question, a "not right now, maybe in spring" (that's a
  deferral: pause the sequence, keep consent), a complaint about frequency ("so many
  texts!" → reduce cadence, confirm once).

## What happens on a revocation (all five, every time)

1. **Tag the contact immediately** in the CRM/contact file using the field every other
   sphere skill checks: `optout`. Set `optout: all` for a full revocation, or
   `optout: text` / `optout: email` / `optout: call` for a channel-specific one (the
   named channel only — other channels stay open). Also record the date and the
   verbatim message that revoked. The verbatim quote is the audit record. This exact
   field name and these exact values are what `birthday-watch`, `home-anniversary`,
   `followup-queue`, and `sphere-message` filter on — a different field name (e.g.
   `dnc`) is invisible to them and the revocation will not actually stop outreach.
2. **Kill every pending touch** for that contact in every sequence, queue, and
   scheduled batch — check followup-queue, sphere-daily drafts, and any open-house
   follow-up sequence. A revocation that stops one list and not the others is a
   violation with extra steps.
3. **One confirmation message maximum, only if the channel allows it, with ZERO
   marketing content:** "You're removed — you won't hear from me again. Sorry to have
   bothered you." Nothing else. No "if you change your mind." If the revocation was
   hostile, send nothing.
4. **Log it** in `revocations.md` next to the contact data: date received, date
   honored, method they used. The honor deadline is **10 business days** — but honor
   it the same day; the deadline is a ceiling, not a target.
5. **Report it to the agent** in the batch summary: who, verbatim what, what was
   cancelled. Never silently swallow a revocation — the agent needs to know the
   relationship's real state.

## The standing checks

- Before ANY outbound batch drafts: scan inbound replies since the last run for
  revocations FIRST. A batch drafted before the scan is a batch drafted against a
  stale list — re-draft after tagging.
- On "can I still text this person": check the tag, the log, and the last 90 days of
  their inbound messages before answering. If there's no consent record at all, the
  answer is about consent tier, not just revocation — route to the consent rules in
  open-house-signin and contact-import.
- Monthly (or when asked to "clean my list"): sweep for contacts with revocation-ish
  language in their history that never got tagged, and reconcile the log against the
  CRM tags.

## What this skill never does

- Never auto-sends anything, including the confirmation — it drafts; the agent
  approves (the agent owns every send).
- Never deletes the contact record. Revoked contacts stay in the database tagged `optout` —
  deleting them destroys the do-not-contact memory and the audit trail.
- Never argues, wins-back, or "one last value message." Revoked is revoked.

---

<!-- self-improvement-loop v1 -->

## Self-improvement loop

Before ending a run of this skill, review the run:

1. Did any step fail, stall, or need a workaround you had to invent?
2. Did the user correct, reject, or rewrite something meaningful in the output?
3. Did you discover something a future run would want to know (a path that moved, a
   tool that replaced another, a preference stated out loud)?

If yes to any, propose a specific edit to this SKILL.md in one or two lines and ask
whether to apply it. Propose only changes that would alter a future run's behavior --
skip cosmetic rewording, and never propose more than two edits at once.

Do not edit this file without the user's go-ahead. If they say no, drop it and do not
re-raise the same suggestion in a later run of the same session.
