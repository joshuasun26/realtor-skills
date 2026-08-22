---
department: foundation
name: source-check
description: >
  Verify every number, date, statistic, price, rate, and credential in a piece of real
  estate marketing before it goes to another human — and enforce the rule that market
  statistics come from the MLS, never from a consumer aggregator. Trigger on "check these
  numbers", "is this accurate", "verify this", "sourcing", "before I send this", "fact
  check", or automatically whenever any skill in this library is about to hand over
  content that asserts a fact. Also use to audit something already published.
---

# Source Check — nothing ships with a number you cannot point at

One wrong number in a flyer, a market brief, or a caption costs an agent more credibility
than ten good pieces earn. This skill is the gate.

Run it before **anything** with a number in it leaves the machine.

---

## The MLS rule (hard, not negotiable)

**Every market statistic must come from the MLS.** Median price, days on market, months
of inventory, sale-to-list ratio, absorption rate, sold comps, active counts — MLS only.

**Never source a market statistic from a consumer aggregator.** Zillow, Redfin,
Realtor.com, Homes.com and similar sites publish numbers on a different basis than the
MLS does. The most common and most damaging example: an aggregator's "days on market"
usually reflects how long a listing has been **active on that site**, not how long a
**sold** property took to go under contract. Publishing that as "average days on market"
is simply a false claim, and it is the number agents get corrected on in public.

Aggregators are acceptable for exactly two things:
1. A public listing page's basic property facts (address, beds, baths, sqft, list price)
   when there is no MLS access in the session — and even then, label the source.
2. Confirming a property exists and is publicly marketed.

They are never acceptable for a statistic about a market.

If the agent has no MLS access this session and a market number is required, the correct
output is: **"this number cannot be sourced right now"** plus what you tried. Not an
estimate. Not a hedge.

## The rungs — work them before you say you cannot verify

"I can't check that" is a trigger, not an answer. In order:

1. The MLS the agent's profile names, using their login
2. A different search scope, date range, or report inside the same MLS
3. Local files: prior exports, saved CSVs, previous `market-pull` output in this repo
4. The primary source's own site (the lender's dated rate sheet, the county recorder,
   the city, the HOA, the tax assessor)
5. Only then: report that it could not be determined, and name which rungs you tried

## The check itself

For each factual claim in the draft, build a row:

| Claim | Source opened this session | As-of date | Verdict |
|---|---|---|---|

**Verdicts:** `VERIFIED` (you opened the source this session), `STALE` (sourced, but the
data is older than the claim implies), `UNSUBSTANTIATED` (no source found).

**What does NOT count as a source:**
- A previous session, a memory file, or a chat summary
- An earlier message in this conversation
- Your own recollection or general knowledge of the market
- What the agent told you, unless the agent IS the primary source (their own listing
  count, their own closing dates)

Those are leads. Only a file you read, a table you queried, or a page you fetched is
evidence.

## Rate and payment numbers

Any payment, rate, or buydown figure requires:
- A **dated lender rate sheet** from the agent's lender partner, dated within 2 business
  days of publication. Last week's sheet is not a source.
- A **dated mortgage insurance quote** if MI is in the payment.
- Every assumption written down: price, loan term, product, credit score, DTI,
  occupancy, down payment, whether impounds are included.
- The full disclaimer block (see `buydown-math`).

If any of those is missing, the piece with the payment in it is **blocked**. Ship the
piece without the payment, or ship nothing. This is not a judgment call.

## Rules for what happens next

- **Cannot source it? Remove it.** Do not soften it into "roughly" or "about". A hedged
  wrong number is still wrong. A defensible qualitative claim beats an unsourceable
  precise one.
- **Numbers shown side by side must share a basis.** Same report, same definition, same
  date range, same geography. Flag mixed sources even when each figure is individually
  correct.
- **Attach the as-of date and the source name** to every statistic that ships. On a
  graphic that means a footer line. In a brief it means a sources block.
- **Stale is a form of unverified.** If you are reading an export, check the file date
  and report the as-of date with the number.
- If the agent decides to ship an `UNSUBSTANTIATED` number anyway, that is their call and
  their license. Say the exposure once, plainly, then log it in the ledger as
  `UNVERIFIED — shipped at the agent's direction` so the record is honest.

## The ledger

Append every run to `records/source-ledger.md`: date, the piece, each claim, each source,
each verdict. When something later turns out wrong, that file is how you find every other
place the number went.

If a bad number already shipped, say so immediately and check every live surface carrying
it — posted graphics, printed flyers, scheduled emails, the listing remarks, the website.

## Chains from

Called by `listing-description`, `buydown-math`, `listing-flyer`, `listing-carousel`,
`market-brief`, `market-carousel`, `social-caption`, `listing-package`,
`open-house-package`, `market-update-package`.

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
