---
department: open-house
name: open-house-signin
description: >
  Build the digital open house sign-in page and its QR code — a single self-contained HTML
  page in the agent's brand that captures name, phone, email, and buyer status on a
  visitor's phone, with the consent language that makes later follow-up legitimate.
  Trigger on "sign-in sheet", "QR code for the open house", "digital sign in", "capture
  page", "how do I collect visitor info", or as a step inside open-house-package. Do NOT
  trigger for a general lead form on the agent's website.
---

# Open House Sign-In — capture that holds up later

The paper clipboard loses half the visitors and produces handwriting nobody can read. A
QR code on the flyer and a card by the door converts better and produces clean data.

The part most agents get wrong is the consent language, and that is the part that decides
whether the follow-up sequence you build later is legitimate or a problem.

Reads `listings/<slug>/LISTING.md` and `profile/AGENT.md`.

---

## The page

**One self-contained HTML file.** All CSS inline, no external fonts, no CDN scripts, no
tracking pixels. It has to load instantly on a weak cell signal in someone's driveway,
which is exactly where it will be used.

Layout, in order:

1. Property hero photo and the address. The visitor should recognize where they are.
2. **Four fields, and only four:** first and last name, mobile phone, email, and one
   radio group: *just looking / actively looking / working with an agent / neighbor*.
   Every additional field costs completions. Resist adding more.
3. The consent block (below), as visible text with a checkbox — not buried in a link.
4. One submit button with a large tap target.
5. A short confirmation state after submit, with the agent's name and contact.
6. Footer: agent name, license number, brokerage, Equal Housing Opportunity.

**Mobile first.** 16px minimum input font size, or iOS zooms the page on focus. Tap
targets at least 44px tall. Test at 375px wide.

## The consent block (this is the whole point)

Written as plain text the visitor actually reads, with an **unchecked** box:

> I'd like [Agent Name] of [Brokerage] to follow up with me about this property and
> similar homes, by text, call, or email. I can stop at any time by replying STOP, or
> just by telling [Agent Name] to stop.

(The "or just by telling me" clause is load-bearing: under 47 CFR 64.1200, a consumer
may revoke by ANY reasonable method, and naming STOP as the only way is itself a
violation. The revocation-watch skill enforces the honor side.)

Rules that are not optional:

- **The box starts unchecked.** A pre-checked box is not consent.
- **No pre-checked box, no dark pattern, no "by submitting you agree" buried in fine
  print.** If a visitor did not affirmatively opt in, they go into the database as
  consent tier `existing-relationship` at best, and they do not go into any automated
  text or bulk email sequence.
- Automated or bulk texting to a mobile number has its own legal rules, and they change.
  Tell the agent plainly: **the written consent record is what protects them**, and they
  should have their broker confirm the current requirements in their state. Do not state
  a specific statute or a specific rule as settled law in this skill — say it needs their
  broker's confirmation.
- Record where the submit goes. If the agent has a CRM, post there. If not, the page
  writes to a local CSV and you tell them exactly where the file is.

## Where the data goes

Output rows into `data/open-house-<slug>-<date>.csv` with columns matching the
`contact-import` schema, including `source` (`open house <address> <date>`) and
`consent_tier` (`express-written` only if the box was checked, otherwise `unknown`).

That file is the input to `open-house-followup`. Contacts marked `unknown` are excluded
from any automated send by every downstream skill, automatically.

## The QR code

- Generate the QR pointing at wherever the page is actually reachable — a hosted URL if
  the agent has a site, or a local network address if the page runs on a laptop at the
  house. **A QR pointing at a `file://` path does not work from a visitor's phone.** If
  there is no hosting, say so and produce a paper fallback instead of shipping a dead QR.
- Minimum printed size 1 inch square; 1.5 inches is safer on a flyer.
- Quiet zone: leave at least four modules of blank margin around it. QR codes fail most
  often because someone put a border right against them.
- Put a short human-readable URL under the code, for people who will not scan.
- **Scan the printed QR with an actual phone before the open house.** Every time. Do not
  assume.

## Fallback

Bring a paper sheet too. Some visitors will not scan anything, and the two-minute
conversation while someone writes their name down is not worthless.

## Chains from / into

Called by `open-house-package`. Feeds `open-house-flyer` (the QR target) and
`open-house-followup` (the captured list).

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
