---
department: listings
name: listing-intake
description: >
  Collect and verify every fact about one property in a single pass, then write it to a
  per-listing file that all downstream listing skills read — address, price, beds, baths,
  square footage, lot size, year built, HOA, status, photo inventory, and the distinctive
  feature that actually sells it. Trigger on "new listing", "set up [address]", "I just
  took a listing", "here's the property", or automatically as step 1 of listing-package
  and open-house-package. Do NOT trigger for a buyer lead or a market-wide question.
---

# Listing Intake — one pass, verified, written down

Every downstream piece (flyer, carousel, remarks, buydown, QR page, captions) reads this
file. Get it right once and nothing downstream has to re-ask or re-guess.

---

## Step 0 — Recover before you create

Check `listings/<address-slug>/LISTING.md`. If it exists, a prior session already made
decisions. **Those win** unless you have a stated reason they are wrong. Never silently
re-decide a chosen photo or an approved line of copy.

Slug format: `123-main-st-anytown` — number, street, city, lowercase, hyphens.

## Step 1 — Ask for everything in ONE message

Do not trickle-ask across five turns. An agent's patience for this is one message long.

**Required:**
- Full property address including city, state, ZIP
- List price
- Beds, full baths, partial baths
- Interior square footage, lot square footage
- Year built
- Property type
- MLS number and status
- Photos: a folder path, a shared-drive link, or the public listing URL

**Required if it is a co-listing or another agent's listing:**
- Listing agent name(s), brokerage, and license number
- Written permission to use their photos and market the property

**Required if there is an HOA:**
- HOA dues, frequency, and what the dues cover

**Ask once, then move on if they do not have it:**
- What the seller or the agent most wants highlighted
- Recent improvements with dates
- Parking, garage, pool, ADU, solar (owned or leased — this matters)
- Showing instructions

**If a Required field is still missing after your one message, that is the one
exception to "ask once."** Send a second, short message asking only for the specific
Required fields still missing (e.g. "just need the full address and lot size to pull the
MLS record"). Do not invent a placeholder and do not proceed to Step 2 until you have
either an answer or an explicit "the agent doesn't know" for every Required field — record
"agent doesn't know, needs confirmation" as the answer where that is the case, and carry
it into `## Not verified` in Step 4.

**Never ask them for the lender rate sheet.** `buydown-math` goes and gets a current
dated one itself, or it blocks.

## Step 2 — Verify against the MLS

Open the MLS record **this session** and confirm: beds, baths, interior sqft, lot size,
list price, year built, status, and HOA. The MLS is the source of record for a property's
facts.

**Do not** take property facts from the agent's message alone, from a prior session, or
from memory. Agents relay from other agents and everyone rounds. A flyer that says 2,400
sqft when the MLS says 2,180 is a real problem.

If MLS access is not available this session, the public listing page is an acceptable
fallback **for property facts only** — label it as such in the file. Aggregator pages are
never acceptable for market statistics; see `source-check`.

Record what you actually opened, and when.

## Step 3 — Inventory the photos

List every image file with a one-line description. Then pick and mark:

- **Hero** — the single best exterior or signature shot. This is slide one and the flyer
  cover. It is the house, never a logo and never the agent.
- **The distinctive feature** — the one thing about this property nobody else has. A
  mature fruit-bearing yard, an original 1920s stair, a workshop, a view. Find the
  sentence for it: *"you can renovate a kitchen, you cannot grow that."* Every property
  has one. Write the sentence into the file; every downstream skill reuses it.
- **Supporting set** — six to ten in the order a buyer would walk the house.
- **Do not use** — anything with people in it, a neighbor's property, a visible address
  on a package, a pet, or a mirror with the photographer in it.

Flag photo quality honestly. If the photos are phone snapshots in bad light, say so and
say that a professional shoot changes the result more than any graphic will.

## Step 4 — Write the file

`listings/<address-slug>/LISTING.md`, with sections:

```
## Property        (every verified fact, one per line)
## Sources         (what you opened, with the date)
## Photos          (file, role, one-line description)
## The one thing   (the distinctive feature and its sentence)
## Seller priorities
## Compliance notes (permissions, HOA disclosure, solar lease, known issues)
## Status log      (dated line per downstream piece produced)
```

Then a `## Not verified` list — anything the agent asserted that you could not confirm.
That list is what blocks downstream pieces, and it should be short and explicit.

## Guardrails

- **Fair housing starts here.** Describe the house and the lot. Nothing about the
  neighborhood's character, its schools, who lives there, or whether it is "safe" or
  "family-friendly". `compliance-check` will catch it, but do not write it in the first
  place.
- **No valuation opinion.** Not underpriced, not a deal, not what it is "really worth".
- **Solar leases, HOA special assessments, permit status on additions, and known material
  defects** get recorded in Compliance notes even if they never appear in marketing. The
  agent needs to see them in one place.

## Chains into

`listing-flyer`, `listing-carousel`, `listing-description`, `buydown-math`,
`open-house-flyer`, `open-house-signin`, `social-caption`.

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
