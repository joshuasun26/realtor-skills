---
department: listings
name: buydown-math
description: >
  Build the seller-credit and rate-buydown comparison for one property — what the same
  dollars do applied to price, to closing costs, or to a permanent rate buydown — with
  every payment traced to a dated lender rate sheet and a full assumptions disclaimer.
  Trigger on "buydown", "rate buydown", "seller credit math", "run the payment scenarios",
  "what would 2 points do", "buydown flyer", or as a step inside listing-package. Do NOT
  trigger without a lender partner and a current rate sheet — this skill blocks rather
  than estimates.
---

# Buydown Math — the highest-converting piece, and the one that can hurt you

This is the piece that reaches people who are not already following the agent, because it
answers a question buyers actually have. It is also the only piece in this library that
puts a dollar figure in front of a consumer, which makes it the one with real exposure.

**The rule that governs this entire skill: if a number cannot be sourced this session,
the piece does not ship.** Not hedged, not rounded, not "approximately". Blocked.

---

## The gate — check ALL of this before writing one number

1. **A dated rate sheet from the agent's lender partner, dated within 2 business days.**
   Not last week's. Not the one in the last listing folder. Not a rate from a website.
   The lender's own dated sheet, obtained this session.
2. **The pricing convention written down.** Rate sheets price in rebate and cost columns.
   State exactly which column you read and the rule you applied to pick the base rate.
   If the agent's lender has a house convention, it belongs in `profile/AGENT.md`.
3. **A dated mortgage insurance quote** from a named provider, if the scenario has MI.
4. **The full assumption set:** price, down payment, loan amount, term, product, credit
   score, DTI, occupancy, property type, impounds or not, and whether the buydown is
   permanent (discount points) or temporary (2-1, 3-2-1).
5. **The lender's NMLS ID** for the disclaimer.

**If any of the five is missing:** say the buydown piece is blocked, name which item is
missing, and produce the rest of the listing package without it. That is the correct
outcome, not a reason to estimate. Route the ask back to the agent as one line they can
forward to their lender.

## The math to present

Keep it to three scenarios. More than three and nobody reads it.

The comparison that lands is **same dollars, three destinations**:

| | Price reduction | Credit to closing costs | Permanent rate buydown |
|---|---|---|---|
| Seller gives up | $X | $X | $X |
| Buyer's payment | | | |
| Buyer's cash to close | | | |
| Saved over 5 years | | | |

The plain-English mechanic, which is the actual content:

> A price cut moves the payment a little. A credit at the closing table helps once, on
> one day. The same dollars applied to a permanent rate buydown lower the payment every
> single month for as long as they own the loan.

Then show the down-payment ladder if the product supports it — 5% / 10% / 20% down with
the payment and the monthly delta on each — and name the product. Many buyers do not know
they have options below 20%, and that is often the line that gets the piece shared.

## What you must NOT do

- **Do not state or imply that a seller credit has been offered or negotiated** on the
  property unless the listing agent has confirmed in writing that it has. Default
  language: *"No seller credit has been offered or negotiated on this property."*
- Do not present this as a loan offer, a pre-approval, a lock, or a commitment to lend.
- Do not quote an APR unless the lender supplied it — APR has its own calculation rules.
- Do not compare against a competitor lender's rate.
- Do not show a payment as the buyer's "total payment" if it excludes taxes, insurance,
  and HOA. Say explicitly what is excluded.
- Do not omit the disclaimer to make the graphic look cleaner. The disclaimer is the
  piece.

## The disclaimer block (mandatory, every date updated)

> Illustration only. Payment varies with loan amount, down payment, credit, and rate.
> No seller credit has been offered or negotiated on this property. Not a commitment to
> lend. Assumes [price], [term and product], [credit score], [DTI], [occupancy],
> impounds [waived/included], [permanent discount point buydown / temporary buydown].
> Payments shown are principal, interest and mortgage insurance only, and exclude
> property taxes, homeowners insurance, and HOA dues, so the actual payment is higher.
> MI estimated via [provider] on [date]. Rates from lender sheet dated [date], subject to
> change without notice. Not all applicants qualify. Equal Housing Opportunity.
> [Lender name], NMLS #[ID].

## Compliance

- The **agent's** brokerage and license appear on the piece, and the **lender's** name
  and NMLS ID appear on it. Both. See `compliance-check`.
- If a lender is paying any share of the cost of a co-marketed piece, the split is a
  broker-and-lender question with real legal weight. Route it, do not design it here.
- Run `source-check` on the finished piece before it ships. Every time.

## Output

Write `listings/<slug>/BUYDOWN.md` containing the scenario table, every assumption, the
rate sheet date and column read, the MI provider and date, and the disclaimer as it will
appear. Then note it in the listing's Status log.

## Chains from / into

Called by `listing-package`. Reads `listings/<slug>/LISTING.md` from `listing-intake` and
`profile/AGENT.md`. Feeds `listing-carousel` (buydown variant), `listing-flyer`, and
`social-caption`. Gated by `source-check` and `compliance-check`.

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
