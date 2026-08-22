---
department: foundation
name: compliance-check
description: >
  Review any public-facing real estate marketing for fair housing violations, missing
  license and brokerage disclosure, valuation claims, and unapproved lender or affiliate
  mentions, before it is printed, posted, or sent. Trigger on "compliance check", "is this
  fair housing safe", "can I say this", "review my listing copy", "check this flyer", or
  automatically before any flyer, carousel, listing remark, caption, or landing page ships.
  Do NOT trigger for internal notes, private messages to a single known client about their
  own transaction, or number verification — numbers are source-check.
---

# Compliance Check — the last read before it goes public

One AI-drafted fair housing mistake is the agent's license and their E&O policy. This
skill is a hard gate, not a suggestion.

**You are not the agent's attorney or their broker.** This skill catches the common,
well-documented failures. Anything ambiguous goes to their broker before it ships, and
you say so plainly rather than making the call yourself.

---

## 1. Fair housing

The protected classes under the federal Fair Housing Act: race, color, religion, national
origin, sex (including sexual orientation and gender identity), familial status, and
disability. Many states and cities add more — source, age, marital status, and others.
Check the agent's state, and if you cannot confirm the state's list this session, say so.

**Reject any language that describes the PEOPLE rather than the PROPERTY.**

Common failures to scan for, in listing copy, captions, flyers, market briefs, and
neighborhood descriptions:

- Anything about who lives in an area, or the demographic makeup of a neighborhood
- School quality or school ratings used as a selling point (a familial-status and
  often a racial proxy). Naming the assigned district factually is different from
  calling it "great schools."
- "Safe", "quiet", "family-friendly", "good area", "up-and-coming", "exclusive",
  "prestigious", "desirable neighborhood"
- "Perfect for a young family", "ideal for a couple", "great starter home for newlyweds",
  "empty nesters", "retirees"
- Proximity to specific churches, temples, or mosques as an amenity
- "Walking distance" or "must be able to climb stairs" (disability implications) — say
  what the property physically is instead
- "Master bedroom" is being phased out at many brokerages; use "primary bedroom"

**Never publish racial, ethnic, or demographic percentages for a neighborhood.** Not in a
carousel, not in a market brief, not as "just data". There is no compliant version of it.

The rewrite rule: **describe the house, the lot, and the verifiable physical facts.** A
four-bedroom with a large flat back yard is a fact. "Perfect for a growing family" is a
violation of the same sentence.

## 2. Advertising and license disclosure

Read the required fields from `profile/AGENT.md`:

- Is the agent's license number displayed where the state requires it?
- Is the brokerage's legal name displayed, at the size and prominence the brokerage
  requires?
- Is the Equal Housing Opportunity logo or statement present on the piece?
- If the agent is a team, is the team clearly identified as operating under the brokerage?
- If the piece names another agent's listing, is the listing brokerage credited?

If `profile/AGENT.md` has `TO CONFIRM WITH BROKER` in any disclosure field, **the piece is
blocked.** Say so and route them to their broker. Do not fill in a plausible-looking line.

## 3. Valuation and market claims

- Never imply a property is underpriced, overpriced, a steal, a deal, below market, or
  what it is "really worth". Mirror what the listing agent states the property offers.
- Never state or imply what a property will be worth in the future, or that values will
  rise. No appreciation projections in consumer marketing.
- Never guarantee a sale, a timeline, or a price.
- Any market statistic in the piece routes to `source-check`, MLS-sourced, with an
  as-of date.

## 4. Lender, affiliate, and referral mentions

- A lender, title, or escrow partner may be credited on a co-marketed piece, but the
  piece cannot read as a mortgage advertisement, and any lender who pays for a share of
  a co-marketed piece must pay their fair share of the actual cost. Cost splits are a
  real-money compliance question — route to the broker, do not design the split here.
- Do not print or imply any arrangement where referrals are exchanged for services or
  marketing.
- Any rate, APR, or payment figure shown triggers the lender's own advertising rules,
  including the lender's NMLS ID and a full assumptions disclaimer. See `buydown-math`.

## 5. Photos and copyright

- Listing photos belong to whoever commissioned them, usually the listing brokerage or
  the photographer, not to the agent sharing them. Confirm permission before reusing
  another brokerage's photography.
- Do not use MLS photos in marketing for a listing the agent does not represent without
  written permission.
- No stock photo of a house presented as the actual property.

## Output

Return a verdict per item:

| Item | Issue | Severity | Fix |
|---|---|---|---|

Severity is `BLOCK` (cannot ship), `BROKER` (needs their broker's call), or `NOTE`
(safe, but worth knowing).

**If anything is BLOCK, say the piece is blocked in the first line of your reply.** Do not
bury it under the rewrite. Then offer the compliant rewrite.

## Chains from

Called by `listing-description`, `listing-flyer`, `listing-carousel`, `social-caption`,
`buydown-math`, `listing-package`, `open-house-package`.

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
